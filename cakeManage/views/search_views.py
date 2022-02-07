from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *
import math # 현재 위치 계산 위해 추가
from django.db.models import Count #리뷰 갯수 세기 위해서 (리뷰 많은 순 정렬)

#필터링 작업 일어났을 시
def filtering(request):
    if request.method == "GET":
        cakes=Cake.objects.none() 
        stores=Store.objects.none()

        print(request.GET)
        category= request.GET.get('flexRadioDefault')
        locationSi=request.GET.getlist('locationSi')
        locationGu=request.GET.getlist('licationGu')
        size=request.GET.getlist('size')
        price=request.GET.getlist('price')

        #카테고리 필터링 
        if category:
            if category=='cakes':
                    chkCategory=1 
            elif category=='stores' :
                    chkCategory=2
            
        #위치 필터링
        if locationSi:
            chkLocationSi=1
            stores |= Store.objects.filter(locationSi__in=locationSi).distinct()
            cakes |= Cake.objects.filter(referred_store__locationSi__in=locationSi).distinct()
        else : #만약 시 필터링 안됐음 stores, cakes는 모든 거 가리킴
            stores=Store.objects.all()
            cakes=Cake.objects.all()

        if chkCategory==1:#카테고리가 케이크라면
            filtered_product=cakes
        elif chkCategory==2:#카테고리가 가게라면
            filtered_product=stores

        print("filtered by locationSi:")
        print(filtered_product)

        if locationGu:
            storesbyGu=[]
            cakesbyGu=[]
            storesbyGu |= stores.filter(locationGu__in=locationGu).distinct()                
            cakesbyGu |= cakes.filter(referred_store__locationGu__in=locationGu).distinct()

            if chkCategory==1:
                cakes=cakesbyGu
                filtered_product=cakes
            else:
                stores=storesbyGu
                filtered_product=storesbyGu

        print("filtered by Gu:")
        print(filtered_product)

        #사이즈 필터링
        if size:
            chkSizes=1
            size_filtered_store=[]

            if chkCategory==1:#cake인 경우에는 바로 정참조로 사이즈 체크
                size_filtered_store=filtered_product.filter(size__in=size).distinct()
                filtered_product=size_filtered_store
                
                print("cakes라서 정참조로 모음")
                print(filtered_product)
                print(size)

            elif chkCategory==2:#가게인 경우에는 역참조로 사이즈 체크
                for i in stores:#location으로 걸러진 가게들 중에서
                    chkSize=0
                    CakesinStores=[] #가게마다 사이즈 체크해야되니깐, 한 가게 다 돌면 초기화
                    #print(i)
                    #i번째 가게가 가지는 케이크들 리스트 수집
                    CakesinStores+= i.cake.all() 
                    #가게를 참조하고 있는 케이크들 담을 리스트 (역참조)
                    print("i번째 가게의 케이크들:")
                    print(CakesinStores) #이 케이크 리스트들에서 size 체크, 있으면 chksize=1 설정
                    for cakes in CakesinStores:
                        print(cakes.size)
                        if(cakes.size in size):
                            #size는 리스트(검색자가 다중 선택 가능해서) => i번째 가게의 케이크들 중 
                            chkSize=1                 
                            #chksize=1이라면 해당 가게는 검색 사이즈의 케이크 포함하고 있는 것
                            break
                            #케이크 하나라도 사이즈 부합한다면 해당 가게는 검색 조건 충족 가능
                    if chkSize:
                        size_filtered_store.insert(-1,i) 
                        print(size_filtered_store)
                        #가게의 케이크 중 사이즈가 해당하는 애가 있으면 해당 가게는 따로 저장
                    
                filtered_product=size_filtered_store

        print("filtered by size:")
        print(filtered_product)

        #가격 필터링
        if price:
            chkPrices=1
            tmp_price=0
            tmp_list=[]
            
            print(filtered_product)
            for i in filtered_product:
                if (i.price < 10000):
                    tmp_price='9999'
                elif (i.price < 20000) :      
                    tmp_price='10000'
                elif(i.price <30000):
                    tmp_price='20000'
                elif(i.price<40000) :
                    tmp_price='30000'
                elif(i.price<50000):
                    tmp_price='40000'
                else:
                    tmp_price='50000'
                #가격이 price list에 존재한다면 필터링 수행ㅇ
                print(tmp_price)

                if ((tmp_price) in price):
                    tmp_list.insert(-1,i)
            
                    #print("filtered by price:")
                    #print(tmp_list)

            #print(filtered_product)
            filtered_product=tmp_list
            if(not(category) and not(locationSi) and not(locationGu) and not(size) and not(price)):
                if(chkCategory==1) :
                    filtered_product=Cake.objects.all()
                else:
                    filtered_product=Store.objects.all()
            print(filtered_product)
            #카테고리, 가격, 사이즈 필터링 거친 마무리 갯수 구하기
        num=0
            #기존 num 초기화하고 products 수 갱신
        for i in filtered_product:
            num+=1
    return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores,'product':filtered_product,'num':num})

def sorting(request):
    cakes= Cake.objects.order_by('-pub_date')
    stores= Store.objects.order_by('-pub_date')
    product1=Cake.objects.all() 
    product2=Store.objects.all()
    product=[product1,product2]
    productss=[]
    sort3 = request.GET.get('sorting',None)#name
    num=0
    if sort3 == 'latest':
        #products = 
        for i in product: 
            productss+=i.order_by('-pub_date')
    elif sort3 == 'review':
        for i in product:
                productss = product1.annotate(order_count=Count('order')).order_by('-order_count')#케이크 역참조
    elif sort3 == 'low':
            for i in product: 
                productss+=i.order_by('price')
    elif sort3 == 'high':
            for i in product: 
                productss+=i.order_by('-price')
    for i in productss:
        num+=1
    return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores,'product':productss,'num':num})

# def search(request):
#     # 빈 쿼리 오브젝트 생성 (결과를 담음)
#     store_result = Store.objects.none()
#     cake_result = Cake.objects.none()
#     if request.GET.get('q'):
#         # 입력을 제대로 했으면
#         # 'q' 값의 value를 가져와서 split으로 띄어쓰기대로 나눈다.
#         query_set= request.GET.get('q').split()
#         # 검색 예시 : 마포 도시락케이크, 마포 하므케이크
#         # 검색 기능: 가게 이름name, 가게 텍스트text, 가게 장소(OO구)location, 검색을 위한 본문meta_body
#         # 케이크 이름cakename, 케이크 설명body, 맛, 모양, 사이즈, 검색을 위한 본문meta_body 로 검색하도록
        
#         # 가게 검색결과와 케이크 검색결과를 나눈다.
#         for query in query_set:
#             question = Q(name__contains=query) | Q(location__startswith=query) | Q(text__icontains=query) | Q(meta_body__icontains=query)
#             store_result |= Store.objects.filter(question) #  계속 합연산
#             question = Q(cakename__contains=query) | Q(referred_store__location__startswith=query) | Q(body__contains=query) | Q(색__contains=query) | Q(meta_body__icontains=query)
#             cake_result |= Cake.objects.filter(question)        
#         return render(request, 'search.html', {'query_set':query_set, 'store_result':store_result, 'cake_result':cake_result})
#     else:
#         # 입력이 없으면 홈으로 돌림
#         return redirect('home')

def recommend(request):
    # 빈 쿼리 오브젝트 생성 (결과를 담음)
    recommend_result=[]
    stores=Store.objects.none()
    cakes=Cake.objects.none()
    recommend_number=0
    print(request.GET)
    if request.GET.get('recommend'):
        print("recom find")
        # 입력을 제대로 했으면
        # 'q' 값의 value를 가져와서 split으로 띄어쓰기대로 나눈다.
        recommendWord= request.GET.get('recommend')
        # 검색 예시 : 마포 도시락케이크, 마포 하므케이크
        # 검색 기능: 가게 이름name, 가게 텍스트text, 가게 장소(OO구)location, 검색을 위한 본문meta_body
        # 케이크 이름cakename, 케이크 설명body, 맛, 모양, 사이즈, 검색을 위한 본문meta_body 로 검색하도록
        print(recommendWord)
        # 가게 검색결과와 케이크 검색결과를 나눈다.
        recommend_word= Q(text__icontains=recommendWord) | Q(meta_body__icontains=recommendWord)
        stores |= Store.objects.filter(recommend_word) #  계속 합연산
        recommend_word= Q(body__contains=recommendWord) | Q(meta_body__icontains=recommendWord)
        cakes |= Cake.objects.filter(recommend_word)   
        print(stores)
        recommend_result_pre=[stores,cakes]
        recommend_result=[]
        print("result of pre")
        print(recommend_result_pre) 

        for i in recommend_result_pre:
            for j in i:
                recommend_number+=1
                print(j)
                recommend_result.insert(recommend_number-1,j)
        print(recommend_result)
        return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores, 'product':recommend_result, 'num' : recommend_number})
    else:
        print("no recom")
        cakes=Cake.objects.all()
        stores=Store.objects.all()
        products=[cakes,stores]
        return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores, 'product':products})


def search(request):
    # 빈 쿼리 오브젝트 생성 (결과를 담음)
    store_result = Store.objects.none()
    cake_result = Cake.objects.none()
    print(request.GET)
    if request.GET.get('q'):
        # 입력을 제대로 했으면
        # 'q' 값의 value를 가져와서 split으로 띄어쓰기대로 나눈다.
        query_set= request.GET.get('q').split()
        # 검색 예시 : 마포 도시락케이크, 마포 하므케이크
        # 검색 기능: 가게 이름name, 가게 텍스트text, 가게 장소(OO구)location, 검색을 위한 본문meta_body
        # 케이크 이름cakename, 케이크 설명body, 맛, 모양, 사이즈, 검색을 위한 본문meta_body 로 검색하도록
        print(query_set)
        # 가게 검색결과와 케이크 검색결과를 나눈다.
        for query in query_set:
            question = Q(name__contains=query) | Q(locationSi__startswith=query) | Q(text__icontains=query) | Q(meta_body__icontains=query)
            store_result |= Store.objects.filter(question) #  계속 합연산
            question = Q(cakename__contains=query) | Q(referred_store__locationSi__startswith=query) | Q(body__contains=query) | Q(color__contains=query) | Q(meta_body__icontains=query)
            cake_result |= Cake.objects.filter(question)   
        products=[]
        products+=cake_result
        products+=store_result  
        print("result of")
        print(products)  
        return render(request, 'search_all.html', {'cakes':cake_result, 'stores':store_result, 'product':products, 'search_word':query_set})
    else:
        print("empt")
        products=[cake_result,store_result]
        return render(request, 'search_all.html', {'cakes':cake_result, 'stores':store_result, 'product':products})

#(2) 원하는 장소만 검색
def search_location2(request):
    #HTML에서 폼 제출하면 사용자가 선택한 지역구들을 리스트에 받아서 델꼬온다
    searchWord=request.POST.getlist('locations[]')
    #post_list=[] #변수 미리 어떤 형태로든 지정해놔야지 지역변수로 인식을 안한다
    post_list=[]
    if searchWord :
        print(searchWord)
        for word in searchWord:
            post_list+=Store.objects.filter(Q(location__icontains=word)|Q(locationSi__icontains=word)).distinct()
            # '+' 붙여서 리스트에 요소를 추가추가해주는 방식으로 가야함
            # 안 붙여주면 구로구,노원구 두개 이상 선택시 둘 중에 한 구만 필터링됨
    context={}
    context['search_term']=searchWord
    context['objects_list']=post_list
    return render(request,'location_search2.html',context)

#거리 계산 함수
def latlng_calculator(lat, lng):
    # 2km 구간
    lat_change = 2 / 111.2 # 1도=111Km
    lng_change = abs(math.cos(lat * (math.pi / 180))) 
    # √ 경도거리제곱+위도거리제곱 
    bounds = { #범위 정해주는 것
        "lat_min": lat - lat_change,
        "lng_min": lng - lng_change,
        "lat_max": lat + lat_change,
        "lng_max": lng + lng_change
    }
    return bounds

def search_location3(request):
    list=[]
    return render(request, 'location_search3.html', {'list' : list,})

def nearby_stores(request):
    lat = request.COOKIES['latitude']
    lng = request.COOKIES['longitude']
    list=[]
    LC = latlng_calculator(float(lat), float(lng))
    list += Store.objects.filter(
        Q(lat__range=[LC['lat_min'], LC['lat_max']]) & Q(lon__range=[LC['lng_min'], LC['lng_max']])
    )
    return render(request, 'location_search3.html', {'list' : list,})
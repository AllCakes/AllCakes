from django.core import paginator
from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.resolvers import LocaleRegexDescriptor
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.http import JsonResponse
from users.urls import mypage
from .models import *
from .forms import *
from django.views.generic import FormView #formview 형 클래스형 제네릭 뷰 임포트 추가
from django.db.models import Q,F, Case, Value, When #시 별로 나오게 하는 구를 다르게 해주는 옵션 구현 위해 추가
from django.db import models # views에서 models.Char~ 기능 사용 위해
import math # 현재 위치 계산 위해 추가
from django.shortcuts import render
# import simplejson as json #제이쿼리 사용위해 추가
import datetime
from itertools import chain #쿼리셋 결합 위해 추가
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    #order_by -pub_date(최신순) pub_date(오래된순)
    cakes = Cake.objects.order_by('-pub_date')
    reviews = Review.objects.order_by('-pub_date')[:3]
    paginator = Paginator(cakes, 4)
    page = request.GET.get('page', 1)
    cakes = paginator.get_page(page)
    return render(request, 'index.html', {'cakes': cakes, 'reviews': reviews})

# 임시 템플릿 연결 뷰
def stores_all(request):
    stores= Store.objects.order_by('-pub_date')
    return render(request, 'stores_all.html', {'stores':stores})

def cakes_all(request):
    cakes= Cake.objects.order_by('-pub_date')
    return render(request, 'cakes_all.html', {'cakes':cakes})

def search_all(request):
    cakes= Cake.objects.order_by('-pub_date')
    stores= Store.objects.order_by('-pub_date')
    product1=Cake.objects.all() 
    product2=Store.objects.all()
    product=[product1,product2]
    products=list(chain(*product))
    #products=product1
    #products |= product2
    paginator = Paginator(products,6)
    #paginator |= Paginator(product2,4)
    page=request.GET.get('page',1)
    product_list=paginator.get_page(page)
    return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores,'product':product_list})
    #return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores,'product':products})

# 가게 등록 C (필요 없을 예정)
def store_new(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.author = request.user
            store.published_date = timezone.now()
            store.save()
            return redirect('home')
    else:
        form = StoreForm()
    return render(request, 'store_new.html', {'form': form})

# 가게 디테일 R
def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    cake_list = Cake.objects.filter(referred_store=store).order_by('-pub_date')[:3]
    review_list = Review.objects.select_related('order').filter(order__referred_store=store)
    num = 0
    # 최신순, 별점 낮은순, 높은순의 option을 post로 받아서 해당에 따라 정렬한다.
    if request.method == "POST":
        sort = request.POST.get('sort')
        num = 2
        if sort == 'highrate':
            review_list = Review.objects.filter(referred_store=store).order_by('-rate','-pub_date')
        elif sort == 'lowerate':
            review_list = Review.objects.filter(referred_store=store).order_by('rate','-pub_date')
        else :
            review_list = Review.objects.filter(referred_store=store).order_by('-pub_date')
    return render(request, 'store_detail.html', {'store': store, 'cakelist':cake_list, 'reviewlist':review_list, 'num':num})

# 가게 수정 U
def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            store.author = request.user
            # store.pub_date = timezone.now() # 게시일자(pub_date) 대신, 새로운 필드로 수정 일자를 넣는 것을 고려 
            store.save()
            return redirect('detail', pk= pk)
    else:
        form = StoreForm(instance=store)

    return render(request, 'store_edit.html', {'form': form})

# 가게 삭제 D (필요 없을 예정, 생성과 삭제는 관리자 측)
def store_delete(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.user != store.user:
        raise ValidationError("잘못된 접근입니다.")
    store.delete()
    return redirect('home')

# 케이크 등록 C (사장님측 UX, 관리자측이 사용할 수도..)
def cake_new(request, pk): #가게 pk값
    store = get_object_or_404(Store, pk=pk)
    store_menu = get_object_or_404(Store_Menu, store = store)
    # 가게별 요청 - 선택사항 콤마로 분리
    색 = store_menu.색.replace(" ","").split(',')
    크림종류 =  store_menu.크림종류.replace(" ","").split(',')
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        # getlist로 가져오기
        color = request.POST.getlist('색')
        colorPrice = request.POST.getlist('색price')
        cream = request.POST.getlist('크림종류')
        creamPrice = request.POST.getlist('크림종류price')
        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            cake.pub_date = timezone.now()
            cake.referred_store = store
            # 케이크 메뉴 저장
            cake.색 = ','.join(color)
            cake.색가격 = ','.join(colorPrice)
            cake.크림종류 = ','.join(cream)
            cake.크림종류가격 = ','.join(creamPrice)
            cake.save()
            return redirect('store_detail', pk=pk)
    else:
        form = CakeForm()
    return render(request, 'cake_new.html', {'form': form, '색':색, '크림종류':크림종류})

# 케이크 상세 R
def cake_detail(request, pk): #cake의 pk값
    cake = Cake.objects.get(pk=pk)    
    review = Review.objects.select_related('order').filter(order__referred_cake=cake).order_by('-pub_date')[:3]
    return render(request, 'cake_detail.html',{'cake':cake, 'review':review})




# 케이크 수정 U
def cake_edit(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    if request.user != cake.user:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        form = CakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            # store.pub_date = timezone.now() # 게시일자(pub_date) 대신, 새로운 필드로 수정 일자를 넣는 것을 고려 
            cake.save()
            # 현재 케이크 역참조를 위해 모델에 related_name 추가 (reverse lookup of foreign keys)
            # The related_name is what we use for the reverse lookup. In general, it is a good practice to provide a related_name for all the foreign keys rather than using Django’s default-related name.
            store_pk = cake.referred_store.pk
            return redirect('store_detail', pk= store_pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현
    else:
        form = StoreForm(instance=cake)

    return render(request, 'cake_edit.html', {'form': form})

# 케이크 삭제 D
def cake_delete(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    if request.user != cake.user:
        raise ValidationError("잘못된 접근입니다.")
    store_pk = cake.referred_store.pk
    cake.delete()
    return redirect('store_detail', pk= store_pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현


# 주문 C (RUD 구현 필요!)
def order_new(request, cake_pk): #cake의 pk값
    if not request.user.is_authenticated:
        return redirect('login_home')
    cake = get_object_or_404(Cake, pk=cake_pk)
    store = get_object_or_404(Store, pk=cake.referred_store_id)
    # 가게별 요청 - 선택사항 콤마로 분리
    a_coupons = AmountCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    p_coupons = PercentCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    # 가게별 요청 - 선택사항 콤마로 분리
    색 = cake.색.replace(" ","").split(',')
    크림종류 =  cake.크림종류.replace(" ","").split(',')
    색가격 = cake.색가격.replace(" ","").split(',')
    크림종류가격 = cake.크림종류가격.replace(" ","").split(',')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.pub_date = timezone.now()
            order.referred_cake = cake
            order.referred_store = cake.referred_store
            order.pay_price = cake.price
            s = request.POST.get('coupon').split("_")
            if request.POST.get('coupon') != "a_0":
                # 쿠폰 있다 한 경우 (쿠폰이 적용 안된 경우 아무런 조치 X)
                if s[0] == 'a':
                    # 금액쿠폰
                    try:
                        coupon = AmountCoupon.objects.get(pk=int(s[1]))
                    except AmountCoupon.DoesNotExist:
                        raise ValidationError("해당 쿠폰이 없습니다.")
                    if coupon.user != request.user:
                        #유저의 것인지 확인
                        raise ValidationError("해당 쿠폰을 사용할 수 없습니다.")
                    else:
                        order.amount_coupon = coupon
                        order.pay_price = cake.price - coupon.amount
                else:
                    # 비율쿠폰
                    try:
                        coupon = PercentCoupon.objects.get(pk=int(s[1]))
                    except PercentCoupon.DoesNotExist:
                        raise ValidationError("해당 쿠폰이 없습니다.")
                    if coupon.user != request.user:
                        #유저의 것인지 확인
                        raise ValidationError("해당 쿠폰을 사용할 수 없습니다.")
                    else:
                        order.percent_coupon = coupon
                        order.pay_price = cake.price * (float(100 - coupon.percent) / 100)
                    #유저의 것인지 확인 해야 함.
            # get 방식으로 가져와 저장
            order.색 = request.POST.get('색')
            order.크림종류 = request.POST.get('크림종류')
            order.save()
            # 주문 결과 페이지로 가도록 수정하기!
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'order.html', {'form': form, 'cake':cake, '색':색, '색가격':색가격,'크림종류':크림종류, '크림종류가격':크림종류가격, 'a_coupons':a_coupons, 'p_coupons':p_coupons})

# 주문 상세 R
def order_detail(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    return render(request, 'order_detail.html',{'order':order})

# 주문 전체 R
def order_all(request, user_pk):
    if request.user.pk != user_pk:
        raise ValidationError("잘못된 접근입니다.")
    orders = Order.objects.get(user=user_pk)
    return render(request, 'order_all.html', {'orders':orders})

# 주문 수정 U (고칠 예정)
def order_edit(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        raise ValidationError("잘못된 접근입니다.")
    cake = order.referred_cake
    # 가게별 요청 - 선택사항 콤마로 분리
    색 = cake.색.replace(" ","").split(',')
    크림종류 = cake.크림종류.replace(" ","").split(',')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # get 방식으로 가져와 저장
            order.색 = request.POST.get('색')
            order.크림종류 = request.POST.get('크림종류')
            order.pub_date = timezone.now()
            # 케이크선택과 가게 선택은 못 바꿈. 삭제하고 다시 주문 필요.
            order.save()
            # 주문 결과 페이지로 가도록 수정하기!
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'cake':cake, '색':색, '크림종류':크림종류})

# 주문 삭제 D
def order_delete(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        raise ValidationError("잘못된 접근입니다.")    
    order.delete()
    return redirect('mypage', pk=request.user.pk)


# 리뷰 페이지 C (R- 더보기 U - 수정 D- 삭제 구현 필요)
def review_page(request, pk, orderpk):
    cake = get_object_or_404(Cake, pk=pk)
    store = get_object_or_404(Store, pk=cake.referred_store_id)
    order =  get_object_or_404(Order, pk=orderpk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.order = order
            review.pub_date = timezone.now()
            review.rate = request.POST.get('rate')
            review.save()
            return redirect('mypage', user_pk=order.user_id)
    else :
        form = ReviewForm()
    return render(request, 'review_page.html', {'form': form, 'cake' : cake, 'store' : store, 'order':order })

# 리뷰 삭제 D
def review_delete(request, pk):
    order = get_object_or_404(Order,pk = pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    review = Review.objects.filter(order_id=pk)
    review.delete()
    return redirect('mypage',user_pk=order.user_id)

# 리뷰 수정 페이지 - U
def review_edit(request, pk):
    review = get_object_or_404(Review, order_id=pk)
    if request.user != review.user:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.rate = request.POST.get('rate')
            review.save()
            return redirect('mypage', user_pk=review.user_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_edit.html', {'form': form, 'review' : review})


# 찜 기능 구현 필요 (유저 경험: 아마.. 케이크, 케잌집 상세페이지에서 찜하기 -> 케이크, 케잌집 모델에 필드 추가 필요)

# 검색 - 검색어 분리, 모든 쿼리 한번에!
def search(request):
    # 빈 쿼리 오브젝트 생성 (결과를 담음)
    store_result = Store.objects.none()
    cake_result = Cake.objects.none()
    if request.GET.get('q'):
        # 입력을 제대로 했으면
        # 'q' 값의 value를 가져와서 split으로 띄어쓰기대로 나눈다.
        query_set= request.GET.get('q').split()
        # 검색 예시 : 마포 도시락케이크, 마포 하므케이크
        # 검색 기능: 가게 이름name, 가게 텍스트text, 가게 장소(OO구)location, 검색을 위한 본문meta_body
        # 케이크 이름cakename, 케이크 설명body, 맛, 모양, 사이즈, 검색을 위한 본문meta_body 로 검색하도록
        
        # 가게 검색결과와 케이크 검색결과를 나눈다.
        for query in query_set:
            question = Q(name__contains=query) | Q(location__startswith=query) | Q(text__icontains=query) | Q(meta_body__icontains=query)
            store_result |= Store.objects.filter(question) #  계속 합연산
            question = Q(cakename__contains=query) | Q(referred_store__location__startswith=query) | Q(body__contains=query) | Q(색__contains=query) | Q(meta_body__icontains=query)
            cake_result |= Cake.objects.filter(question)        
        return render(request, 'search.html', {'query_set':query_set, 'store_result':store_result, 'cake_result':cake_result})
    else:
        # 입력이 없으면 홈으로 돌림
        return redirect('home')

        return render(self.request, self.template_name,context)
#(2) 원하는 장소만 검색
def search_location2(request):
    #HTML에서 폼 제출하면 사용자가 선택한 지역구들을 리스트에 받아서 델꼬온다
    searchWord=request.POST.getlist('locations[]')
    #post_list=[] #변수 미리 어떤 형태로든 지정해놔야지 지역변수로 인식을 안한다
    post_list=[]
    if searchWord :
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


def order_complete(request):
    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)
    if order.user != request.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        return render(request, 'order_complete.html', {'order':order})
    else:
        raise ValidationError("잘못된 접근입니다.")



class OrderTransactionAjaxView(View):
    def post(self, request, *args, **kawargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        amount = order.pay_price
        try:
            merchant_uid = OrderTransaction.objects.create_new(order = order, amount = amount)
        except:
            merchant_uid = None
        
        if merchant_uid is not None:
            data = {
                "works" : True,
                "merchant_uid" : merchant_uid
            }
            # Json 응답으로 생성여부 및 생성 내용을 반환
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class OrderImpAjaxView(View):

    # 결제한 결과에서 주문번호, 가격을 가져와 이전의 거래 객체와 비교해주고, 그러한 객체가 있으면(일치하면)
    # 통과 및 Order 객체의 결제 여부 True로 만들어주기
    # 다만 이렇게 DB와 비교하고 True로 만들어주는 것보다, 거래번호를 저장한 후에
    # 나중에 import 서버 통신을 통한 검증 후에 True로 바꿔주는 것이 더 나을듯..

    # 서버를 통한 검증 + DB의 pay_price 확인

    # 통과 X시 결제정보 위변조 가능성이 있으므로 오류발생시키고, 관리자 문의하도록 유도
    def post(self, request, *args, **karags):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_uid = request.POST.get('merchant_uid')
        imp_uid = request.POST.get('imp_uid')
        amount = request.POST.get('amount')
        try:
            trans = OrderTransaction.objects.get(order=order,merchant_uid=merchant_uid, amount=amount)
        except:
            trans = None
        if order.pay_price != amount:
            return JsonResponse({}, status=402)
        if trans is not None:
            trans.transaction_id = imp_uid
            trans.success = True
            trans.save()
            order.is_paid = True
            order.save()
            data = {
                "works": True
            }
            return JsonResponse(data)

        else:
            return JsonResponse({}, status=401)
def test(request):
    return render(request, 'test.html')

def character(request):
    post_list=[]
    searchWord="캐릭터"
    if searchWord :
        for word in searchWord:
            post_list+=Cake.objects.filter(Q(meta_body__icontains=word)).distinct()
            # '+' 붙여서 리스트에 요소를 추가추가해주는 방식으로 가야함
            # 안 붙여주면 구로구,노원구 두개 이상 선택시 둘 중에 한 구만 필터링됨
    context={}
    context['search_term']=searchWord
    context['objects_list']=post_list
    return render(request, 'character.html',context)
# 검색 - 검색어 분리, 모든 쿼리 한번에!
def storemenu(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        color = request.POST.getlist('색')
        cream = request.POST.getlist('크림종류')
        if(len(color) > 0 | len(cream) > 0):
            Store_Menu(store = store, 색 = ','.join(color), 크림종류 = ','.join(cream)).save()
            return redirect('store_detail', pk=store_pk)
    return render(request, 'storemenu.html')

def storemenu_edit(request, store_pk):
    store_menu = get_object_or_404(Store_Menu, store=store_pk)
    색 = store_menu.색.replace(" ","").split(',')
    크림종류 =  store_menu.크림종류.replace(" ","").split(',')
    if request.user != store_menu.store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        form = StoreMenuForm(request.POST, instance=store_menu)
        if form.is_valid():
            color = request.POST.getlist('색')
            cream = request.POST.getlist('크림종류')
            menu = form.save(commit=False)
            menu.색 =','.join(color)
            menu.크림종류 = ','.join(cream)
            menu.save()
            return redirect('store_detail', pk=store_pk)
    else:
        form = StoreMenuForm(instance=store_menu)
    return render(request, 'storemenu.html', {'색' : 색, '크림종류':크림종류})

# json 파일에 menu 없을시 추가
@csrf_exempt
def add_menu(request):
    file_path = './allcake/static/data/menu.json'
    if request.method == "POST":
        ty = request.POST['ty']
        val = request.POST['value']
        with open(file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            json_data['menu'][0][ty][val] = request.POST['img']
        with open(file_path, 'w', encoding="utf-8") as outfile:
            json.dump(json_data, outfile ,ensure_ascii=False, indent=4)
    return redirect('storemenu.html')

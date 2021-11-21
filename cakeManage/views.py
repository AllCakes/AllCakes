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
from django.db.models import Count #리뷰 갯수 세기 위해서 (리뷰 많은 순 정렬)

def home(request):
    #order_by -pub_date(최신순) pub_date(오래된순)
    cakes = Cake.objects.order_by('-pub_date')
    reviews = Review.objects.order_by('-pub_date')[:3]
    recentReviews = Review.objects.order_by('-pub_date')[:5]
    paginator = Paginator(cakes, 4)
    page = request.GET.get('page', 1)
    cakes = paginator.get_page(page)
    return render(request, 'index.html', {'cakes': cakes, 'reviews': reviews, 'recentReviews': recentReviews})

# 임시 템플릿 연결 뷰
def stores_all(request):
    stores= Store.objects.order_by('-pub_date')
    return render(request, 'stores_all.html', {'stores':stores})

def cakes_all(request):
    cakes= Cake.objects.order_by('-pub_date')
    return render(request, 'cakes_all.html', {'cakes':cakes})

# 처음 검색창 불러왔을 때 
def search_all(request):
    cakes=Cake.objects.all() 
    stores=Store.objects.all()
    products=[cakes,stores]
    products=list(chain(*products))
    num1=Cake.objects.all().count()
    num2=Store.objects.all().count()
    num=num1+num2
    return render(request, 'search_all.html', {'cakes':cakes, 'stores':stores,'product':products,'num':num})

#필터링 작업 일어났을 시
def filtering(request):

    if request.method == "GET":
        chkLocationSi=0
        chkLocationGu=0
        chkPrices=0
        chkSizes=0

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
        print("가격필터테스트")
        if price:
            chkPrices=1
            tmp_price=0
            tmp_list=[]
            print(filtered_product)
            for i in filtered_product:

                if (i.price < 10000):
                    tmp_price=9999
                elif (i.price < 20000) :      
                    tmp_price=10000
                elif(i.price <30000):
                    tmp_price=20000
                elif(i.price<40000) :
                    tmp_price=30000
                elif(i.price<50000):
                    tmp_price=40000
                else:
                    tmp_price=50000
                #가격이 price list에 존재한다면 필터링 수행ㅇ
                if (str(tmp_price) in price):
                    tmp_list.insert(-1,i)
        print("filtered by price:")
        print(filtered_product)

        if(not(category)):
            if(not(locationSi)):
                if(not(locationGu)):
                    if(not(size)):
                        if(not(price)):
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
            review_list = Review.objects.select_related('order').filter(order__referred_store=store).order_by('-rate','-pub_date')
        elif sort == 'lowerate':
            review_list = Review.objects.select_related('order').filter(order__referred_store=store).order_by('rate','-pub_date')
        else :
            review_list = Review.objects.select_related('order').filter(order__referred_store=store).order_by('-pub_date')
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
    store_col = store_menu.색.replace(" ","").split(',')
    store_cream = store_menu.크림종류.replace(" ","").split(',')
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
    return render(request, 'cake_new.html', {'form': form, 'store_col':store_col, 'store_cream': store_cream})

# 케이크 상세 R
def cake_detail(request, pk): #cake의 pk값
    cake = Cake.objects.get(pk=pk)    
    review = Review.objects.select_related('order').filter(order__referred_cake=cake).order_by('-pub_date')[:3]
    return render(request, 'cake_detail.html',{'cake':cake, 'review':review})




# 케이크 수정 U
def cake_edit(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    store = get_object_or_404(Store, pk = cake.referred_store_id)
    store_menu = get_object_or_404(Store_Menu, store = store)
    # 가게별 요청 - 선택사항 콤마로 분리
    store_col = store_menu.색.replace(" ","").split(',')
    store_cream =  store_menu.크림종류.replace(" ","").split(',')
    color = cake.색.replace(" ","").split(',')
    cream =  cake.크림종류.replace(" ","").split(',')
    col_price =  cake.색가격.replace(" ","").split(',')
    cream_price =  cake.크림종류가격.replace(" ","").split(',')
    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        color = request.POST.getlist('색')
        colorPrice = request.POST.getlist('색price')
        cream = request.POST.getlist('크림종류')
        creamPrice = request.POST.getlist('크림종류price')
        form = CakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            cake = form.save(commit=False)
            # store.pub_date = timezone.now() # 게시일자(pub_date) 대신, 새로운 필드로 수정 일자를 넣는 것을 고려 
            # 케이크 메뉴 저장
            cake.색 = ','.join(color)
            cake.색가격 = ','.join(colorPrice)
            cake.크림종류 = ','.join(cream)
            cake.크림종류가격 = ','.join(creamPrice)
            cake.save()
            return redirect('store_detail', pk= store.pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현
    else:
        form = CakeForm(instance=cake)
    return render(request, 'cake_edit.html', {'form': form,  'store_col':store_col, 'store_cream': store_cream, '색':color, '크림종류':cream, '크림종류가격': cream_price, '색가격':col_price})

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
    # 가게별 요청 - 선택사항 콤마로 분리
    a_coupons = AmountCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    p_coupons = PercentCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
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
            order.색 = request.POST.get('색')
            order.크림종류 = request.POST.get('크림종류')
            idx_col = 색.index(order.색)
            idx_crm = 크림종류.index(order.크림종류)
            order.prev_price = (int(cake.price) + int(색가격[idx_col]) + int(크림종류가격[idx_crm]))
            order.pay_price = order.prev_price
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
                        order.prev_price = (int(cake.price) + int(색가격[idx_col]) + int(크림종류가격[idx_crm]))
                        order.pay_price = int(order.prev_price) - coupon.amount
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
                        order.prev_price = (int(cake.price) + int(색가격[idx_col]) + int(크림종류가격[idx_crm]))
                        order.pay_price = int(order.prev_price) * (float(100 - coupon.percent) / 100)
                    #유저의 것인지 확인 해야 함.
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
    orders = Order.objects.filter(user=user_pk)
    return render(request, 'order_all.html', {'orders':orders})

# 주문 수정 U (고칠 예정)
def order_edit(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    cake = get_object_or_404(Cake, pk=order.referred_cake.pk)
    if request.user != order.user:
        raise ValidationError("잘못된 접근입니다.")
    if order.is_paid:
        raise ValidationError("잘못된 접근입니다.")
    # 가게별 요청 - 선택사항 콤마로 분리
    a_coupons = AmountCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    p_coupons = PercentCoupon.objects.filter(user=request.user).filter(is_active=True).filter(use_to__date__gt=datetime.date.today())
    색 = cake.색.replace(" ","").split(',')
    크림종류 =  cake.크림종류.replace(" ","").split(',')
    색가격 = cake.색가격.replace(" ","").split(',')
    크림종류가격 = cake.크림종류가격.replace(" ","").split(',')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.색 = request.POST.get('색')
            order.크림종류 = request.POST.get('크림종류')
            idx_col = 색.index(order.색)
            idx_crm = 크림종류.index(order.크림종류)
            s = request.POST.get('coupon').split("_")
            order.prev_price = (int(cake.price) + int(색가격[idx_col]) + int(크림종류가격[idx_crm]))
            order.pay_price = order.prev_price
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
                        order.prev_price = (int(cake.price) + int(색가격[idx_col]) + int(크림종류가격[idx_crm]))
                        order.pay_price = int(order.prev_price) - coupon.amount
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
                        order.prev_price = (int(cake.price) + int(색가격[idx_col]) + int(크림종류가격[idx_crm]))
                        order.pay_price = int(order.prev_price) * (float(100 - coupon.percent) / 100)
                    #유저의 것인지 확인 해야 함.
            # get 방식으로 가져와 저장
            order.save()
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'order':order, 'cake':cake, '색':색, '색가격':색가격,'크림종류':크림종류, '크림종류가격':크림종류가격, 'a_coupons':a_coupons, 'p_coupons':p_coupons})

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
    review = get_object_or_404(Review, pk = pk)
    if request.user != review.user:
        raise ValidationError("잘못된 접근입니다.")
    review.delete()
    return redirect('mypage', user_pk=request.user.pk)

# 리뷰 수정 페이지 - U
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user != review.user:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            rate = request.POST.get('rate')
            if(rate != None):
                review.rate = rate
            review.save()
            return redirect('review_detail', review_pk=pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_edit.html', {'form': form, 'review' : review})


# 찜 기능 구현 필요 (유저 경험: 아마.. 케이크, 케잌집 상세페이지에서 찜하기 -> 케이크, 케잌집 모델에 필드 추가 필요)

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
        print("hihihi")
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
            question = Q(cakename__contains=query) | Q(referred_store__locationSi__startswith=query) | Q(body__contains=query) | Q(색__contains=query) | Q(meta_body__icontains=query)
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

def like_it(request):
    type = request.POST.get("type")
    type = int(type)
    obj_id = request.POST.get("obj_id")
    obj_id = int(obj_id)
    print(type)
    print(obj_id)
    if type == 1:
        try:
            obj = get_object_or_404(Cake, id=obj_id)
        except Cake.DoesNotExist:
            return JsonResponse({}, status=402)
    elif type == 2:
        obj = get_object_or_404(Store, id=obj_id)
    else:
        return JsonResponse({}, status=401)     #오류 상황


    if obj.users_liked.filter(id=request.user.id).exists():
        obj.users_liked.remove(request.user)
        data = {
            "like" : False
        }
    else:
        obj.users_liked.add(request.user)
        data = {
            "like": True
        }

    # Json 응답으로 생성여부 및 생성 내용을 반환
    return JsonResponse(data)
    

def test(request):
    return render(request, 'test.html')
def chkbox(request):
    return render(request, 'chkbox.html')
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
        if(len(color) == 0 | len(cream) == 0):
            return render(request, 'storemenu.html')
        Store_Menu(store = store, 색 = ','.join(color), 크림종류 = ','.join(cream)).save()
        return redirect('store_detail', pk=store_pk)
    return render(request, 'storemenu.html')

def storemenu_edit(request, store_pk):
    store_menu = get_object_or_404(Store_Menu, store=store_pk)
    color = set(store_menu.색.replace(" ","").split(','))
    cream = set(store_menu.크림종류.replace(" ","").split(','))
    print(color)
    print(cream)
    if request.user != store_menu.store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == "POST":
        form = StoreMenuForm(request.POST, instance=store_menu)
        if form.is_valid():
            color.update(request.POST.getlist('색'))
            cream.update(request.POST.getlist('크림종류'))
            menu = form.save(commit=False)
            menu.색 =','.join(list(color))
            menu.크림종류 = ','.join(list(cream))
            menu.save()
            return redirect('store_detail', pk=store_pk)
    else:
        form = StoreMenuForm(instance=store_menu)
    return render(request, 'storemenu.html', {'색' : list(color), '크림종류':list(cream)})

# json 파일에 menu 없을시 추가
@csrf_exempt
def add_menu(request):
    file_path = './allcake/static/data/menu.json'
    if request.method == "POST":
        print("Ddd")
        ty = request.POST['ty']
        val = request.POST['value']
        with open(file_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            json_data['menu'][0][ty][val] = request.POST['img']
        with open(file_path, 'w', encoding="utf-8") as outfile:
            json.dump(json_data, outfile ,ensure_ascii=False, indent=4)
    return redirect('storemenu.html')

def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    return render(request, 'review_detail.html', {'review':review})

def likedcake_delete(request, user_pk, cake_pk):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    cake = get_object_or_404(Cake, pk=cake_pk)
    if cake.users_liked.filter(id=request.user.id).exists():
        cake.users_liked.remove(request.user)
    else:
        return JsonResponse({}, status=401)

    return redirect('likedcakes_all', user_pk=request.user.pk)

def likedstore_delete(request, user_pk, store_pk):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    store = get_object_or_404(Store, pk=store_pk)
    if store.users_liked.filter(id=request.user.id).exists():
        store.users_liked.remove(request.user)
    else:
        return JsonResponse({}, status=401)

    return redirect('likedstores_all', user_pk=request.user.pk)

def review_all(request, user_pk):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    reviews = Review.objects.filter(user=user_pk)
    return render(request, 'review_all.html', {'reviews':reviews})

def likedcakes_all(request, user_pk):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    liked_cakes = Cake.objects.filter(users_liked=user_pk)
    return render(request, 'likedcakes_all.html', {'liked_cakes':liked_cakes})

def likedstores_all(request, user_pk):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    liked_stores = Store.objects.filter(users_liked=user_pk)
    return render(request, 'likedstores_all.html', {'liked_stores':liked_stores})
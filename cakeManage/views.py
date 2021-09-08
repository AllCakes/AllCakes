from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.resolvers import LocaleRegexDescriptor
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic.base import View
from users.urls import mypage
from .models import Menu, Store, Cake, Order, Review
from .forms import ReviewForm, StoreForm, CakeForm, OrderForm
from django.views.generic import FormView #formview 형 클래스형 제네릭 뷰 임포트 추가
from django.db.models import Q,F, Case, Value, When #시 별로 나오게 하는 구를 다르게 해주는 옵션 구현 위해 추가
from django.db import models # views에서 models.Char~ 기능 사용 위해
import math # 현재 위치 계산 위해 추가
from django.shortcuts import render
import simplejson as json #제이쿼리 사용위해 추가

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
    cake_list = Cake.objects.filter(referred_store=store)
    review_list = Review.objects.filter(referred_store=store)
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
    if request.user != store.user:
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
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            cake.pub_date = timezone.now()
            cake.referred_store = store
            cake.save()
            return redirect('store_detail', pk=pk)
    else:
        form = CakeForm()

    return render(request, 'cake_new.html', {'form': form})

# 케이크 상세 R
def cake_detail(request, pk): #cake의 pk값
    cake = Cake.objects.get(pk=pk)
    return render(request, 'cake_detail.html',{'cake':cake})

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
    cake = get_object_or_404(Cake, pk=cake_pk)
    # 가게별 요청 - 선택사항 콤마로 분리
    맛 = cake.맛.replace(" ","").split(',')
    모양 = cake.모양.replace(" ","").split(',')
    사이즈 = cake.사이즈.replace(" ","").split(',')
    크림종류 = cake.크림종류.replace(" ","").split(',')
    레터링색 = cake.레터링색.replace(" ","").split(',')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # get 방식으로 가져와 저장
            order.맛 = request.POST.get('맛')
            order.모양 = request.POST.get('모양')
            order.사이즈 = request.POST.get('사이즈')
            order.크림종류 = request.POST.get('크림종류')
            order.레터링색 = request.POST.get('레터링색')
            order.pub_date = timezone.now()
            order.referred_cake = cake
            order.referred_store = cake.referred_store
            order.save()
            # 주문 결과 페이지로 가도록 수정하기!
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'order.html', {'form': form, 'cake':cake, '맛':맛, '모양':모양, '사이즈':사이즈, '크림종류':크림종류, '레터링색':레터링색})

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
    cake = order.referred_cake
    # 가게별 요청 - 선택사항 콤마로 분리
    맛 = cake.맛.replace(" ","").split(',')
    모양 = cake.모양.replace(" ","").split(',')
    사이즈 = cake.사이즈.replace(" ","").split(',')
    크림종류 = cake.크림종류.replace(" ","").split(',')
    레터링색 = cake.레터링색.replace(" ","").split(',')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # get 방식으로 가져와 저장
            order.맛 = request.POST.get('맛')
            order.모양 = request.POST.get('모양')
            order.사이즈 = request.POST.get('사이즈')
            order.크림종류 = request.POST.get('크림종류')
            order.레터링색 = request.POST.get('레터링색')
            order.pub_date = timezone.now()
            # 케이크선택과 가게 선택은 못 바꿈. 삭제하고 다시 주문 필요.
            order.save()
            # 주문 결과 페이지로 가도록 수정하기!
            return redirect('order_detail', order_pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'cake':cake, '맛':맛, '모양':모양, '사이즈':사이즈, '크림종류':크림종류, '레터링색':레터링색})

# 주문 삭제 D
def order_delete(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.user != order.user:
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
            review.referred_store = store
            review.referred_cake = cake
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
            question = Q(cakename__contains=query) | Q(referred_store__location__startswith=query) | Q(body__contains=query) | Q(맛__contains=query) | Q(모양__contains=query) | Q(사이즈__contains=query) | Q(meta_body__icontains=query)
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
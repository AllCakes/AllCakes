from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Store, CakeImage, Cake, Order, Review
from .forms import StoreForm, CakeForm, OrderForm, ReviewForm

def home(request):
    #order_by -pub_date(최신순) pub_date(오래된순)
    posts = Store.objects.order_by('-pub_date')
    paginator = Paginator(posts, 4) 
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'posts_list': posts})


# 가게 등록
def new(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = StoreForm()
    return render(request, 'new.html', {'form': form})

# 가게 디테일
def detail(request, pk):
    post = get_object_or_404(Store, pk=pk)
    cake_list = Cake.objects.filter(referred_store=post)
    review_list = Review.objects.filter(referred_store=post)
    return render(request, 'detail.html', {'post': post, 'cakelist':cake_list, 'reviewlist':review_list})

# 가게 수정
def edit(request, pk):
    post = get_object_or_404(Store, pk=pk)
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('detail', pk= pk)
    else:
        form = StoreForm(instance=post)

    return render(request, 'edit.html', {'form': form})

# 가게 삭제
def delete(request, pk):
    post = get_object_or_404(Store, pk=pk)
    post.delete()
    return redirect('home')

# 가게의 새 케이크 등록
def newcake(request, pk):
    post = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.published_date = timezone.now()
            content.referred_store = post
            content.save()
            for img in request.FILES.getlist('imgs'):
                image = CakeImage()
                image.referred_cake = content
                image.cake_image = img
                image.save()
            return redirect('detail', pk=pk)
    else:
        form = CakeForm()

    return render(request, 'newcake.html', {'form': form})

# 케이크 이미지 수정
def image_edit(request, pk):
    post = get_object_or_404(Cake, pk=pk)
    if request.method == "POST":
        for img in request.FILES.getlist('imgs'):
            image = CakeImage()
            image.referred_cake = post
            image.cake_image = img
            image.save()
        return redirect('detail', pk= post.pk)
    else:
        return render(request, 'image_edit.html',{'post':post})

# 케이크 등록 이미지 삭제
def image_delete(request, pk, image_pk):
    image = get_object_or_404(CakeImage, pk=image_pk)
    image.delete()
    return redirect('image_edit', pk=pk)

# 케이크 주문
def order(request, pk):
    cake = get_object_or_404(Cake, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.published_date = timezone.now()
            content.referred_cake = cake
            content.referred_store = cake.referred_store
            content.save()
            return redirect('detail', pk=cake.referred_store_id)
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form, 'cake':cake})

# 추후 회원가입 추가시, 회원번호로 주문내역을 확인할 수 있도록 수정
def mypage(request):
    orders = Order.objects.all()
    return render(request, 'mypage.html', {'order_list':orders})

# 리뷰 작성하기
# 현재 별점추가 진행중 .. 
def review(request, pk):
    cake = get_object_or_404(Cake, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.published_date = timezone.now()
            content.referred_store = cake.referred_store
            content.referred_cake = cake
            content.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})
from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *

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

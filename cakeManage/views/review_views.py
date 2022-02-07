from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *

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

def review_all(request, user_pk):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    reviews = Review.objects.filter(user=user_pk)
    return render(request, 'review_all.html', {'reviews':reviews})

def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    return render(request, 'review_detail.html', {'review':review})
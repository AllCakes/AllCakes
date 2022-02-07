from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *

# 케이크 등록 C (사장님측 UX, 관리자측이 사용할 수도..)
def cake_new(request, pk): #가게 pk값
    store = get_object_or_404(Store, pk=pk)
    # 가게별 재료 
    color = store.color.all()
    cream = store.cream.all()
    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        # getlist로 가져오기
        color = request.POST.getlist('color')
        colorPrice = request.POST.getlist('colprice')
        cream = request.POST.getlist('cream')
        creamPrice = request.POST.getlist('crmprice')
        # 조작된 경우
        if len(color) != len(colorPrice):
            raise ValidationError("잘못된 접근입니다.")
        if len(cream) != len(creamPrice):
            raise ValidationError("잘못된 접근입니다.")
        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            cake.pub_date = timezone.now()
            cake.referred_store = store
            # 케이크 메뉴 저장
            for i in range(0,len(color)):
                print(color[i])
                print(colorPrice[i])
                cake.save_color_menu(color[i], colorPrice[i])
            for i in range(0,len(cream)):
                cake.save_cream_menu(cream[i], creamPrice[i])
            e = cake.print_color_menu()
            print(e)
            cake.save()
            return redirect('store_detail', pk=pk)
    else:
        form = CakeForm()
    context = {
        'form': form,
        'color': color,
        'cream': cream
    }
    return render(request, 'cake_new.html', context)

# 케이크 상세 R
def cake_detail(request, pk): #cake의 pk값
    cake = Cake.objects.get(pk=pk)    
    review = Review.objects.select_related('order').filter(order__referred_cake=cake).order_by('-pub_date')[:3]
    return render(request, 'cake_detail.html',{'cake':cake, 'review':review})


# 케이크 수정 U
def cake_edit(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    store = get_object_or_404(Store, pk = cake.referred_store_id)
    # 가게별 재료 
    color = store.color.all()
    cream = store.cream.all()
    # 이미 입력된 재료들
    havecolor = cake.print_color_menu()
    havecream = cake.print_cream_menu()

    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES, instance=cake)
        # getlist로 가져오기
        color = request.POST.getlist('color')
        colorPrice = request.POST.getlist('colprice')
        cream = request.POST.getlist('cream')
        creamPrice = request.POST.getlist('crmprice')
        # 조작된 경우
        if len(color) != len(colorPrice):
            raise ValidationError("잘못된 접근입니다.")
        if len(cream) != len(creamPrice):
            raise ValidationError("잘못된 접근입니다.")

        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            cake.pub_date = timezone.now()
            cake.referred_store = store
            # 케이크 메뉴 저장
            cake.re_color_menu()
            cake.re_cream_menu()
            for i in range(0,len(color)):
                cake.save_color_menu(color[i], colorPrice[i])
            for i in range(0,len(cream)):
                cake.save_cream_menu(cream[i], creamPrice[i])
            cake.save()
            return redirect('store_detail', pk= store.pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현
    else:
        form = CakeForm(instance = cake)
    context = {
        'form': form,
        'color': color,
        'cream': cream,
        'havecolor':havecolor,
        'havecream':havecream
    }
    return render(request, 'cake_edit.html', context)

# 케이크 삭제 D
def cake_delete(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    if request.user != cake.user:
        raise ValidationError("잘못된 접근입니다.")
    store_pk = cake.referred_store.pk
    cake.delete()
    return redirect('store_detail', pk= store_pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현
from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *
import json

# 가게별 메뉴 선정
def menu_new(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    color = Menu_Color.objects.all()
    cream = Menu_Cream.objects.all()

    # 메뉴 이름
    col_name = [c.to_string_name() for c in color]
    crm_name = [c.to_string_name() for c in cream]

    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")

    if request.method == "POST":
        cols = request.POST.getlist('색')
        crms = request.POST.getlist('크림종류')
        for i in cols:
            store.color.add(get_object_or_404(Menu_Color, pk=int(i)))
        for i in crms:
            store.cream.add(get_object_or_404(Menu_Cream, pk=int(i)))
        return redirect('store_detail', pk=store_pk)
    context = {
        'color':color,
        'cream':cream,
        'pk':store_pk,
        'col_name':col_name,
        'crm_name':crm_name
    }
    return render(request, 'store_menu.html', context)

# 가게별 메뉴 수정
def menu_edit(request, store_pk):
    store = get_object_or_404(Store, pk = store_pk)

    # 이미 등록한 메뉴
    havecolor = store.color.all()
    havecream = store.cream.all()
    havecolorlist = store.color.values_list('pk', flat = True)
    havecreamlist = store.cream.values_list('pk', flat = True)
    # 아직 등록안한 메뉴
    color = Menu_Color.objects.exclude(id__in=havecolorlist)
    cream = Menu_Cream.objects.exclude(id__in=havecreamlist)
    # 메뉴 이름
    cr = Menu_Color.objects.all()
    cm = Menu_Cream.objects.all()
    col_name = [c.to_string_name() for c in color]
    crm_name = [c.to_string_name() for c in cream]

    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")

    if request.method == "POST":
        cols = request.POST.getlist('색')
        crms = request.POST.getlist('크림종류')
        for i in cols:
            store.color.add(get_object_or_404(Menu_Color, pk=int(i)))
        for i in crms:
            store.cream.add(get_object_or_404(Menu_Cream, pk=int(i)))
        return redirect('store_detail', pk=store_pk)
    context = {
        'color':color,
        'cream':cream,
        'havecolor': havecolor,
        'havecream':havecream,
        'pk':store_pk,
        'col_name':col_name,
        'crm_name':crm_name
    }
    return render(request, 'store_menu.html', context)

# menu 없을시 추가
def menu_add(request,store_pk):
    store = get_object_or_404(Store, pk = store_pk)
    if request.user != store.owner:
        raise ValidationError("잘못된 접근입니다.")

    if request.is_ajax():
        color = request.GET['newcolor']
        cream = request.GET['newcream']
        if (len(color) > 0):
            c = Menu_Color()
            c.img = "img/noimg.png"
            c.name = color
            c.save()
        if (len(cream) > 0):
            c = Menu_Cream()
            c.img = "img/noimg.png"
            c.name = cream
            c.save()
        message = "완료되었습니다."
        return HttpResponse(json.dumps(message), content_type='application/json')

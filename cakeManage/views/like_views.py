from django.shortcuts import *
from django.core.exceptions import ValidationError
from ..models import *
from ..forms import *
from django.http import JsonResponse
from django.urls import reverse

def like_it(request):
    type = request.POST.get("type")
    type = int(type)
    obj_id = request.POST.get("obj_id")
    obj_id = int(obj_id)
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
    
def likedcake_delete(request, user_pk, cake_pk, state):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    cake = get_object_or_404(Cake, pk=cake_pk)
    if cake.users_liked.filter(id=request.user.id).exists():
        cake.users_liked.remove(request.user)
    else:
        return JsonResponse({}, status=401)
    
    state = int(state)

    if state == 1:
        return redirect(reverse('mypage', kwargs={'user_pk':request.user.pk}) + '#cake-info-header')
    else:
        return redirect('likedcakes_all', user_pk=request.user.pk)

def likedstore_delete(request, user_pk, store_pk, state):
    if (request.user.pk != user_pk):
        raise ValidationError("잘못된 접근입니다.")
    store = get_object_or_404(Store, pk=store_pk)
    if store.users_liked.filter(id=request.user.id).exists():
        store.users_liked.remove(request.user)
    else:
        return JsonResponse({}, status=401)

    state = int(state)

    if state == 1:
        return redirect(reverse('mypage', kwargs={'user_pk':request.user.pk}) + '#store-info-header')
    else:
        return redirect('likedstores_all', user_pk=request.user.pk)

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
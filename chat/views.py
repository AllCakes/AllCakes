from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ValidationError
from .models import *

# Create your views here.
def room(request,store_pk, user_pk):
    # 로그인 되지 않은 경우
    if not request.user.is_authenticated:
        raise ValidationError("잘못된 접근입니다.")
    store = get_object_or_404(Store, pk = int(store_pk))
    user = get_object_or_404(User, pk = int(user_pk))
    # 가게 주인 혹은 사용자만 입장가능
    if request.user != store.owner and request.user.pk != user_pk:
        raise ValidationError("잘못된 접근입니다.")
    context = {
        'room_name': user_pk,
        'store_name': store_pk,
        'name' : request.user
    }
    return render(request, 'room.html', context)


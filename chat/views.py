from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ValidationError

from .helper import convert_datetime_to_different_timezone, UTC_TIMEZONE, SEOUL_TIMEZONE, get_str_from_datetime, \
    DATE_TIME_FORMAT
from allcake.settings import CLIENT
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

    # 이전 대화내용 있으면 불러오기
    filters = {'chat_room':str(store_pk+"_"+user_pk)}
    sort_fields = [('timestamp',-1)]
    previous_messages = []
    for chat in CLIENT['chat_message']['account_1'].find(filters).sort(sort_fields).limit(20):
        chat['_id'] = str(chat['_id'])
        time = convert_datetime_to_different_timezone(chat['timestamp'], UTC_TIMEZONE, SEOUL_TIMEZONE)
        chat['timestamp'] = get_str_from_datetime(time, DATE_TIME_FORMAT)
        print(chat['timestamp'])
        chat['message'] = chat['message']['text']
        previous_messages.append(chat)
    previous_messages = sorted(previous_messages, key=lambda s: s['timestamp'])
    print("find prev chat=====>",previous_messages)
    context = {
        'guest': user,
        'store': store,
        'user_name' : request.user,
        'user_id' : request.user.pk,
        'prev_messages' : previous_messages
    }
    return render(request, 'room.html', context)


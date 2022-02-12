from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<store_pk>\w+)/(?P<user_pk>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
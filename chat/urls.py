from django.urls import path
from .views import room 

urlpatterns = [
    path('<str:store_pk>/<str:user_pk>/', room, name='room'),
]
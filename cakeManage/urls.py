#kdy : url을 앱별로 분리
from django.urls import path
from cakeManage import views as cakemanage
from .views import *
urlpatterns = [
    path('', cakemanage.home, name="home"),
    path('new/', cakemanage.new, name="new"),
    path('detail/<int:pk>', cakemanage.detail, name="detail"),
    path('edit/<int:pk>', cakemanage.edit, name="edit"),
    path('edit/<int:pk>/images', cakemanage.image_edit, name="image_edit"),
    path('detail/<int:pk>/delete', cakemanage.delete, name="delete"),
    path('edit/<int:pk>/images/<int:image_pk>/delete', cakemanage.image_delete, name="image_delete"),
    path('newcake/<int:pk>', cakemanage.newcake, name="newcake"),
    path('order/<int:pk>', cakemanage.order, name="order"),
    path('mypage/', cakemanage.mypage, name="mypage"),
    path('review/<int:pk>', cakemanage.review, name="review"),
]
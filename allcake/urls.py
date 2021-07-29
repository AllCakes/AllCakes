"""allcake URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cakeManage import views as cakemanage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
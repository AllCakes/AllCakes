from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
# Create your models here.


class Store(models.Model):
    # 순서대로 가게이름, 대표이미지, 설명, 게시일자, 연락처, 가게위치(OO구)
    name = models.CharField(max_length=20)
    store_image = models.ImageField(upload_to='storeimages/', blank=False)
    text = models.TextField(default='', blank=True)
    pub_date = models.DateTimeField(default=timezone.now)
    contact = models.CharField(max_length=15)
    location_choices =[
        ('종로구','종로구'),
        ('중구','중구'),
        ('용산구','용산구'),
        ('성동구','성동구'),
        ('광진구','광진구'),
        ('동대문구','동대문구'),
        ('중랑구','중랑구'),
        ('성북구','성북구'),
        ('강북구','강북구'),
        ('도봉구','도봉구'),
        ('노원구','노원구'),
        ('은평구','은평구'),
        ('서대문구','서대문구'),
        ('마포구','마포구'),
        ('양천구','양천구'),
        ('강서구','강서구'),
        ('구로구','구로구'),
        ('금천구','금천구'),
        ('영등포구','영등포구'),
        ('동작구','동작구'),
        ('관악구','관악구'),
        ('서초구','서초구'),
        ('강남구','강남구'),
        ('송파구','송파구'),
        ('강동구','강동구'),
]
    location = models.CharField(
        max_length = 10,
        choices = location_choices,
        default = '마포구',
    )
    def __str__(self):
        return self.name

class CakeImage(models.Model):
    referred_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    cake_image = models.ImageField(upload_to='cakeimages/', blank=True, null=True)
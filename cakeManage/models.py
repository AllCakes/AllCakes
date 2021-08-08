from __future__ import unicode_literals
from account import models, views
from django.utils import timezone
from django.db import models
import datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL

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


class Cake(models.Model):
    cakename = models.CharField(default='',max_length=200)
    referred_store = models.ForeignKey(Store ,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default = timezone.now)
    body = models.TextField(default='')

class CakeImage(models.Model):
    referred_cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    cake_image = models.ImageField(upload_to='cakeimages/', blank=True, null=True)

# 주문 관련 정보
# 글씨체, 데코레이션 추가 필요
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    referred_store = models.ForeignKey(Store,on_delete=models.CASCADE)
    referred_cake = models.ForeignKey(Cake,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default = timezone.now)
    reviewing = models.IntegerField(default=1)
    희망픽업일= models.CharField(null=True,max_length=30,default=datetime.date.today)
    TIME_CHOICES=[
        ('10:00','10:00'),
        ('10:30','10:30'),
        ('11:00','11:00'),
        ('11:30','11:30'),
        ('12:00','12:00'),
        ('12:30','12:30'),
        ('13:00','13:00'),
        ('14:30','14:30'),
        ('15:00','15:00'),
        ('15:30','15:30'),
        ('16:00','16:00'),
        ('16:30','16:30'),
        ('17:00','17:00'),
        ('17:30','17:30'),
        ('18:00','18:00'),
        ('18:30','18:30'),
        
    ]
    FLAVOR_CHOICES=[
    ('초콜릿','초콜릿'),
    ('딸기','딸기'),
    ('바닐라','바닐라'),
    ('레드벨벳','레드벨벳'),
    ]
    SHAPE_CHOICES=[
        ('원형','원형'),
        ('하트','하트'),
        ('사각형','사각형'),
    ]
    SIZE_CHOICES=[
        ('도시락케이크(1~2인)','도시락케이크(1~2인)'),
        ('1호(2~3인)','1호(2~3인)'),
        ('2호(3~4인)','2호(3~4인)'),
        ('3호(4~5인)','2호(4~5인)'),
    ]
    CREAM=[
        ('버터','버터'),
        ('생크림','생크림'),
        ('크림치즈','크림치즈'),
    ]
    LETTER_POS=[
        ('판 위에 레터링','판 위에 레터링'),
        ('케이크에 직접 레터링','케이크에 직접 레터링'),
    ]
    LETTER_COLOR=[
        ('RED','RED'),
        ('PINK','PINK'),
        ('YELLOW','YELLOW'),
        ('BLUE','BLUE'),
    ]
    희망픽업시간=models.CharField(
        null=True,
        max_length=30,
        choices=TIME_CHOICES,
        default='10:00')
    맛=models.CharField(
        null=True,
        max_length=4,
        choices=FLAVOR_CHOICES,
        default='초콜릿')
    모양=models.CharField(
        null=True,
        max_length=5,
        choices=SHAPE_CHOICES,
        default="원형"
    )
    사이즈=models.CharField(
        null=True,
        max_length=30,
        choices=SIZE_CHOICES,
        default="도시락케이크"
    )
    크림종류=models.CharField(
        null=True,
        max_length=30,
        choices=CREAM,
        default="버터"
    )
    레터링위치=models.CharField(
        null=True,
        max_length=30,
        choices=LETTER_POS,
        default="케이크에 직접 레터링"
    )
    레터링색=models.CharField(
        null=True,
        max_length=30,
        choices=LETTER_COLOR,
        default="RED"
    )
    원하시는도안사진첨부 = models.ImageField(null=True,upload_to='images/',blank=True)

# 리뷰 관련 정보
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, unique = True, on_delete=models.CASCADE)
    referred_store = models.ForeignKey(Store,on_delete=models.CASCADE)
    referred_cake = models.ForeignKey(Cake,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default = timezone.now)
    comment = models.TextField(default='', blank=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

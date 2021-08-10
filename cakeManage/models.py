from __future__ import unicode_literals
from users.models import User
from django.utils import timezone
from django.db import models
import datetime

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
    # 가게 사장 user는 관리자에서 설정하도록 할 것, 이후 그 가게의 사장이면
    # Store 수정(U), Cake 등록과 수정 (CRUD) 가능하도록!
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) # ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField값을 null로 바꾼다. (null=True일 때만 가능)

    # 유저 모델이 아닌 다른 모델에서 필드를 추가하는 게 바람직함. (유저모델은 여러 곳에서 참조되기 때문)
    # related_name을 설정하지 않으면 위의 owner필드와 충돌이 나므로, 꼭 써줘야 됨. (두 번 이상 유저를 가리키기 때문)
    # 유저에서 이 모델을 가리킬 때의 문제인듯
    # 기본 설명: https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    # 역참조 확인: https://www.delftstack.com/howto/django/django-reverse-foreign-key/
    # related_query_name?: https://stackoverflow.com/questions/43132872/difference-between-related-name-and-related-query-name-attributes-in-django/43133136
    # ... Two fields of the Student model are referencing the Teacher model. In Django, when referencing the same model more than once, we have to provide a related_name for all the fields because Django’s default related_name for a single referencing field clashes with other referencing fields. Otherwise, Django will throw an exception. The related_name is what we use for the reverse lookup. In general, it is a good practice to provide a related_name for all the foreign keys rather than using Django’s default-related name.
    users_liked = models.ManyToManyField(User, blank=True, related_query_name="users_liked_store", related_name="users_liked_store")
    # 같이 알면 좋을 것 같아서 주석 많이 달았음! 찜 구현할 때 필드랑 내용 다 삭제 해도 괜찮! 

    def __str__(self):
        return self.name


class Cake(models.Model):
    cakename = models.CharField(default='',max_length=200)
    referred_store = models.ForeignKey(Store ,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default = timezone.now)
    body = models.TextField(default='')
    cake_image = models.ImageField(upload_to='cakeimages/', blank=False, null=True)
    
    # 찜을 위한 필드 (임시)
    users_liked = models.ManyToManyField(User, blank=True, related_query_name="users_liked_cake", related_name="users_liked_cake")
    
    def __str__(self):
        return self.cakename

# Cake와 cake_image 하나만 넣는 식으로 바꿈. CakeImage 모델 삭제
# 이후 복수 업로드가 필요한 경우 코드 다시 돌리기.

# 주문 관련 정보
# 글씨체, 데코레이션 추가 필요
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="주문자")
    referred_store = models.ForeignKey(Store,on_delete=models.CASCADE, verbose_name="가게")
    referred_cake = models.ForeignKey(Cake,on_delete=models.CASCADE, verbose_name="선택 케이크")
    pub_date = models.DateTimeField(default = timezone.now, verbose_name="주문 날짜")
    reviewing = models.IntegerField(default=1, verbose_name="(평점)")
    희망픽업일 = models.CharField(null=True, max_length=30, default=datetime.date.today)
    # 주문 상태 확인을 위해 승인 상태, 진행 상태(픽업 완료, 미완료), 결제 상태를 DB 저장 및 업데이트해야 함.
    # 각각 승인 : is_accepted, 진행 상태: is_active, 결제 상태: is_paid로 설정. 이후 더 필요하면 추가.
    # 관리자가 보기 편하도록 verbose_name='이름' 추가 verbose_name 추가해주세용.
    is_accepted = models.BooleanField(verbose_name="가게 승인", default=False)
    is_active = models.BooleanField(verbose_name="진행중",default=True)
    is_paid = models.BooleanField(verbose_name="결제완료",default=False)
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
    원하시는도안사진첨부 = models.ImageField(null=True,upload_to='images/',blank=True, verbose_name="사진 첨부(도시락케이크 선택시)")

    def __str__(self):
        return str(self.pk)

# 리뷰 관련 정보
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # An order object can have one and only one review on each order.
    # https://stackoverflow.com/questions/5870537/whats-the-difference-between-django-onetoonefield-and-foreignkey
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    referred_store = models.ForeignKey(Store,on_delete=models.CASCADE)
    referred_cake = models.ForeignKey(Cake,on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default = timezone.now)
    comment = models.TextField(default='', blank=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

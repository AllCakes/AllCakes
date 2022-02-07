from __future__ import unicode_literals
from email.policy import default
from users.models import User
from django.utils import timezone
from django.db import models
import datetime
import hashlib
from django.db.models import Q,F, Case, Value, When #시 별로 나오게 하는 구를 다르게 핸주는 옵션
from django.core.validators import MinValueValidator, MaxValueValidator

class Search(models.Model):
    검색단어 = models.CharField(max_length=30)

class Menu_Color(models.Model):
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)
    
    def to_string_name(self):
        return str(self.name)

class Menu_Cream(models.Model):
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)

    def to_string_name(self):
        return str(self.name)

class Store(models.Model):
    # 순서대로 가게이름, 대표이미지, 설명, 게시일자, 연락처, 가게위치(OO구)
    name = models.CharField(max_length=15)
    store_image = models.ImageField(upload_to='storeimages/', blank=False)
    text = models.TextField(default='', blank=True)
    meta_body = models.CharField(max_length=100, default='', verbose_name="검색을 위한 키워드(100자 이내)") # 검색을 위한 필드
    pub_date = models.DateTimeField(default=timezone.now)
    contact = models.CharField(max_length=15)

    # Menu
    color = models.ManyToManyField(Menu_Color, related_name='menu_color', blank=True)
    cream = models.ManyToManyField(Menu_Cream, related_name='menu_color', blank=True)

    # kdy : 가격 0원으로 건드렸음
    price = models.IntegerField(default=0, validators=[MinValueValidator(0, MaxValueValidator(100000))],verbose_name="메뉴 평균 금액")
    si_choices=[
        ('서울', '서울'),
        ('경기', '경기'),
        ('인천', '인천'),
        ('강원', '강원'),
        ('대전', '대전'),
        ('세종', '세종'),
        ('충남', '충남'),
        ('충북', '충북'),
        ('부산', '부산'),
        ('울산', '울산'),
        ('경남', '경남'),
        ('경북', '경북'),
        ('대구', '대구'),
        ('광주', '광주'),
        ('전남', '전남'),
        ('전북', '전북'),
        ('제주', '제주'),
    ]

    locationSi = models.CharField(
        max_length=10,
        choices=si_choices,
        default='서울',
        verbose_name="시"
    )
    locationGu=models.CharField(max_length=10, default='00구/00시', verbose_name="지역(구/시)") 


    # 가게 사장 user는 관리자에서 설정하도록 할 것, 이후 그 가게의 사장이면
    # Store 수정(U), Cake 등록과 수정 (CRUD) 가능하도록!
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
    # ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField값을 null로 바꾼다. (null=True일 때만 가능)

    # 유저 모델이 아닌 다른 모델에서 필드를 추가하는 게 바람직함. (유저모델은 여러 곳에서 참조되기 때문)
    # related_name을 설정하지 않으면 위의 owner필드와 충돌이 나므로, 꼭 써줘야 됨. (두 번 이상 유저를 가리키기 때문)
    # 유저에서 이 모델을 가리킬 때의 문제인듯
    # 기본 설명: https://stackoverflow.com/questions/2642613/what-is-related-name-used-for-in-django
    # 역참조 확인: https://www.delftstack.com/howto/django/django-reverse-foreign-key/
    # related_query_name?: https://stackoverflow.com/questions/43132872/difference-between-related-name-and-related-query-name-attributes-in-django/43133136
    # ... Two fields of the Student model are referencing the Teacher model. In Django, when referencing the same model more than once, we have to provide a related_name for all the fields because Django’s default related_name for a single referencing field clashes with other referencing fields. Otherwise, Django will throw an exception. The related_name is what we use for the reverse lookup. In general, it is a good practice to provide a related_name for all the foreign keys rather than using Django’s default-related name.
    users_liked = models.ManyToManyField(User, blank=True, related_query_name="users_liked_store", related_name="users_liked_store")
    # 같이 알면 좋을 것 같아서 주석 많이 달았음! 찜 구현할 때 필드랑 내용 다 삭제 해도 괜찮! 

    lat = models.CharField(max_length=20, verbose_name="위도", default= 37.2, )
    lon = models.CharField(max_length=20, verbose_name="경도", default= 125.3, )

    def __str__(self):
        return self.name

class Cake(models.Model):
    cakename = models.CharField(default='',max_length=200)
    referred_store = models.ForeignKey(Store ,on_delete=models.CASCADE, related_name="cake")
    #kdy : 역참조 prefetch_related 써서 가게 안의 케이크 가게들을 데려와야 해서 related_name을 cake로 추가적으로 설정
    #참고 : https://leemoney93.tistory.com/24
    #참고2 : https://velog.io/@hwang-eunji/backend-django-%EC%97%AD%EC%B0%B8%EC%A1%B0-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0
    pub_date = models.DateTimeField(default = timezone.now)
    body = models.TextField(default='')  # 케이크 소개
    meta_body = models.CharField(max_length=100, default='', verbose_name="검색을 위한 키워드(100자 이내)") # 검색을 위한 필드
    cake_image = models.ImageField(upload_to='cakeimages/', blank=False, null=True)
    ####kdy 1112 에 추가함 (size)
    size_choices=[
        ('보틀케이크', '보틀케이크'),
        ('도시락케이크', '도시락케이크'),
        ('1~2인분', '1~2인분'),
        ('3~4인분', '3~4인분'),
        ('5인분 이상', '5인분 이상'),
    ]

    size= models.CharField(
        max_length=10,
        choices=size_choices,
        default='보틀케이크',
    )
    # 케이크 추가할 선택사항
    #kdy : 가격 0원으로 바꿈
    price=models.CharField(default='0원',max_length=100)

    color = models.JSONField(default=dict)
    cream = models.JSONField(default=dict)

    # 찜을 위한 필드 (임시)
    users_liked = models.ManyToManyField(User, blank=True, related_query_name="users_liked_cake", related_name="users_liked_cake")
    
    #결제를 위한 가격 정보
    price = models.IntegerField(default=0, validators=[MinValueValidator(0, MaxValueValidator(100000))])
    def __str__(self):
        return self.cakename

    #재료 정보를 json 형식으로 저장
    def save_color_menu(self, id, price):
        self.color[str(id)] = price
        self.save()

    def save_cream_menu(self, id, price):
        self.cream[str(id)] = price
        self.save()

    # checking
    def print_color_menu(self):
        return self.color

    def print_cream_menu(self):
        return self.cream
    
    def re_color_menu(self):
        self.color = {}
        self.save()
    
    def re_cream_menu(self):
        self.cream = {}
        self.save()

# Cake와 cake_image 하나만 넣는 식으로 바꿈. CakeImage 모델 삭제
# 이후 복수 업로드가 필요한 경우 코드 다시 돌리기.
# 쿠폰 클래스 금액할인, 비율할인의 두 방식
class AmountCoupon(models.Model):
    name = models.CharField(max_length=30)
    use_from = models.DateTimeField(auto_now_add=True) # 사용시작시간
    use_to = models.DateTimeField() # 사용기한
    # 할인 양은 0부터 100000까지만 가능
    amount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100000)])
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + str(self.pk)

class PercentCoupon(models.Model):
    name = models.CharField(max_length=30)
    use_from = models.DateTimeField(auto_now_add=True) # 사용시작시간
    use_to = models.DateTimeField() # 사용기한
    # 할인 비율은 0부터 100까지만 가능
    percent = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + str(self.pk)

# 주문 관련 정보 : 글씨체, 데코레이션 추가 필요
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="주문자")
    referred_store = models.ForeignKey(Store,on_delete=models.CASCADE, verbose_name="가게")
    referred_cake = models.ForeignKey(Cake,on_delete=models.CASCADE, verbose_name="선택 케이크")
    pub_date = models.DateTimeField(default = timezone.now, verbose_name="주문 날짜")
    pickup_date = models.CharField(null=True, max_length=30, default=datetime.date.today,verbose_name="희망 픽업일")
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
    LETTER_POS=[
        ('판 위에 레터링','판 위에 레터링'),
        ('케이크에 직접 레터링','케이크에 직접 레터링'),
    ]
    pickup_time=models.CharField(
        null=True,
        max_length=30,
        choices=TIME_CHOICES,
        default='10:00',
        verbose_name="희망 시간"
        )
    lettering_position=models.CharField(
        null=True,
        max_length=30,
        choices=LETTER_POS,
        default="케이크에 직접 레터링",
        verbose_name="레터링 위치"
    )

    # 주문 상태 확인을 위해 승인 상태, 진행 상태(픽업 완료, 미완료), 결제 상태를 DB 저장 및 업데이트해야 함.
    # 각각 승인 : is_accepted, 진행 상태: is_active, 결제 상태: is_paid로 설정. 이후 더 필요하면 추가.
    is_accepted = models.BooleanField(verbose_name="가게 승인", default=False)
    is_active = models.BooleanField(verbose_name="진행중",default=True)
    is_paid = models.BooleanField(verbose_name="결제완료",default=False)
    
    # 결제금액 관련
    prev_price = models.IntegerField(default= 0,validators=[MinValueValidator(0),MaxValueValidator(100000)])
    pay_price = models.IntegerField(default= 0,validators=[MinValueValidator(0),MaxValueValidator(100000)])
    amount_coupon = models.ForeignKey(AmountCoupon, on_delete=models.SET_NULL, null=True, blank=True)
    percent_coupon = models.ForeignKey(PercentCoupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    # 주문 재료 선택
    ingredient = models.JSONField(default=dict)
    원하시는도안사진첨부 = models.ImageField(null=True,upload_to='orderimages/',blank=True, verbose_name="사진 첨부(도시락케이크 선택시)")

    # 쿠폰 적용 전 금액, 적용 쿠폰, 최종금액
    # original_price = models.IntegerField(default=referred_cake.price)
    # amount_coupon = models.ForeignKey(AmountCoupon, on_delete=models.PROTECT, related_name='amount_coupon', null=True, blank=True)
    # percent_coupon = models.ForeignKey(PercentCoupon, on_delete=models.PROTECT, related_name='percent_coupon', null=True, blank=True)
    # total_price = models.IntegerField()

    def __str__(self):
        return str(self.pk)

    # 재료 관련 def
    def save_menu(self, type, id, price):
        self.ingredient[type] = {str(id) : str(price)}
        self.save()

    def print_menu(self):
        return self.ingredient
    
    def reset_menu(self):
        self.ingredient = {}
        self.save()

class OrderTransactionManager(models.Manager):
    # 주문거래 클래스 생성용 함수
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문의 오류")
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        user_hash = str(order.user.nickname)
        final_hash = hashlib.sha1((order_hash + user_hash).encode('utf-8')).hexdigest()[:10]
        merchant_uid = "%s"%(final_hash)

        # payments_prepare(merchant_order_id, amount) # 이 주문번호로 이 가격을 지불받으라고 전달

        # transaction 모델 객체 생성
        transaction = self.model(
            order = order,
            merchant_uid = merchant_uid,
            amount = amount
        )

        # 성공 시에는
        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status
        
        try:
            transaction.save()
        except Exception as e:
            # 저장 안될 시 에러 표출
            print("save error", e)
        
        # 거래모델을 저장하고 주문번호를 돌려줌.
        return transaction.merchant_uid
    
    # def get_transaction(self, merchant_order_id):
    #     result = check_transaction(merchant_order_id)
    #     if result['status'] == 'paid':
    #         return result
    #     else:
    #         print("결제가 되지 않았습니다. from get_transaction")
    #         return None

# 거래 정보 모델
class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_uid = models.CharField(max_length=120, null=True, blank=True) # hashed order_id originated from our server
    transaction_id = models.CharField(max_length=120, null=True, blank=True) # imp_uid와 같은 결제 후의 고유 결제번호
    amount = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    success = models.BooleanField(default=False)
    transaction_status = models.CharField(max_length=220,null=True, blank=True)
    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id) # Order의 id번호로 이름 설정
    
    class Meta:
        ordering= ['-created']

# 리뷰 관련 정보
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # An order object can have one and only one review on each order.
    # https://stackoverflow.com/questions/5870537/whats-the-difference-between-django-onetoonefield-and-foreignkey
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default = timezone.now)
    comment = models.TextField(default='', blank=True)
    rate = models.IntegerField(default=0)
    review_img = models.ImageField(null=True,upload_to='reviewimages/',blank=True, verbose_name="사진 첨부")

    def __str__(self):
        return str(self.id)
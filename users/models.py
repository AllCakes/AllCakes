from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings

# AbstractUser 말고  AbstractBaseUser를 extend

#  You must create the custom User model before you apply your first migration.

#  (create_user를 커스터마이징하기 위해서 UserManager를 새로 만듦.)
#  The UserManager subclasses the BaseUserManager and overrides the methods create_user and create_superuser. 
#  These custom methods are needed because the default methods expect a username to be provided.
#  The admin app and manage.py will call these methods.


# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#manager-methods 
# 커스텀된 유저 모델에 필요한 유저매니저 클래스를 직접 만들음.
class UserManager(BaseUserManager):
    # 카카오면 이메일 없이 생성, 카카오가 아니면 이메일 없이는 에러 출력
    # email -> empty string(''), password -> None on kakao user creation
    # nickname 중복가능 is_는 모두 Boolean Field

    # 그런 유저가 존재하지 않음을 확인한 후에, 
    # 이 함수를 불러와야 함. 아니면 에러남.
    def _create_user(self, email, password, is_staff, is_superuser, is_kakao, is_owner, gender, age_range, birthday, nickname, kakao_id):
        if not nickname:
            raise ValueError('Users must have a unique nickname')
        # 소셜 로그인이 아니고
        if not is_kakao:
            # 이메일이 없으면(null on DB, '' on python code) 에러 출력
            if not email:
                raise ValueError('Users must have an email address')
            now = timezone.now()
            # 이메일 규격화 내장함수 사용
            email = self.normalize_email(email)
            # 이메일 인증과정을 넣게 되면 False로 해주고 이후 인증 받고 True로 수정 
            user = self.model(
                email = email,
                is_staff = is_staff,
                is_active = True,
                is_superuser = is_superuser,
                last_login = now,
                date_joined = now,
                is_owner= is_owner,
                is_kakao = is_kakao,
                kakao_id = None,
                nickname = nickname,
            )
            user.set_password(password)
            user.save(using=self._db)
            # 유저 저장 완료
            return user
        else:
            # 카카오 로그인일 경우의 가입
            # 이메일은 빈 칸으로 둔다.
            now = timezone.now()

            # None 객체를 줘서 DB에서 null이 되도록 만들어보자.
            user = self.model(
                email = None,
                is_staff = is_staff,
                is_active = True,
                is_superuser = is_superuser,
                last_login = now,
                date_joined = now,
                is_kakao = is_kakao,
                kakao_id = kakao_id,
                is_owner= is_owner,
                # 카카오 선택 항목 동의 시 정보 기본 ""값 (빈 문자열)
                gender = gender,
                age_range = age_range,
                birthday = birthday,
                # -----
                nickname = nickname,
            )
            # 패스워드 없이 저장, 이 메소드로 생성되면 비밀번호 체크 안먹힘
            user.set_unusable_password()
            user.save(using=self._db)
            # 유저 저장 완료
            return user

    # 인자를 받아와 _create_user를 실행하도록 함. 위의 함수 인자 참고! (카카오와 그냥 로그인 변수 조심해야 함!)
    def create_user(self, email, password, is_kakao, gender, age_range, birthday, nickname, kakao_id):
        #                        이메일, 패스워드, 직원, 관리자,  카카오, 사장님,  성별,   나이대,     생일,     닉네임,   카카오 id
        return self._create_user(email, password, False, False, is_kakao, False, gender, age_range, birthday, nickname, kakao_id)
    
    def create_superuser(self,email, password, nickname):
        #                        이메일, 패스워드, 직원, 관리자,카카오,사장님,성별,나이대,생일, 닉네임, 카카오id
        return self._create_user(email, password, True, True, False, False, '', '', '',  nickname, '')

    # class Meta:
    #     app_label = 'default'
    #     managed = False

class User(AbstractBaseUser, PermissionsMixin):
    # Null : DB와 관련되어 있다. (database-related) 주어진 데이터베이스 컬럼이 null(빈 상태) 값을 가질 것인지 아닌지를 정의한다.
    # Blank : 유효성과 관련되어 있다. (validation-related) form.is_valid()가 호출될 때 폼 유효성 검사에 사용된다.
    # 기본회원가입 시 email을 꼭 입력하게 조정하고
    # 이메일 인증과정을 넣게 되면 is_active를 False로 해주고 이후 인증 받고 True로 수정

    # email should be null value(None on python) when you save kakao social_signin_user
    # null on django : https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-options

    # 이메일 -> 폼에서 저장할때는 반드시 입력, unique한 값, null=True를 주는 이유는 unique=True일 때 빈 문자열들이 충돌나기 때문.
    email = models.EmailField(verbose_name='email address', max_length=254, unique=True, blank=False, null=True)
    is_staff = models.BooleanField(default=False) # admin 사이트에 필요해서 들어간 값, 사업할 시 필요할 수 있음
    is_superuser = models.BooleanField(default=False) # used by the PermissionsMixin to grant all permissions.
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_kakao = models.BooleanField(default=False) #카카오가 아님(False)이 기본
    kakao_id = models.CharField(max_length=15, default='', unique=True, blank=False, null=True)
    # 소셜로그인이건 간편로그인이건 nickname을 무조건 받도록 nickname을 유저네임으로 하고 
    # 로그인 인증(authenticate backend)을 커스터마이징 해서 
    # 기본 유저 : email and password로 로그인시킴.
    # 카카오 : 카카오의 사용자 id으로 백에서 로그인 시킴. 
    # (소셜로그인으로 토큰을 받아오면 -> 이미 인증된 유저라 생각할 수 있음.)

    # 사장님: admin에서 직접 만들도록 할 것(위의 create_user 안 씀), store와 사장user는 1:1 관계
    # store DB에 저장되는 게 바람직하므로 related_store 삭제.
    is_owner = models.BooleanField(default=False)
    # related_store = models.ForeignKey(Store, on_delete=None, default=None)
    

    # 카카오에서 들어오는 추가정보
    gender = models.CharField(max_length=6, blank=True, default="") # female or male
    age_range = models.CharField(max_length=7, blank=True, default="") # e.g) 20~29 , 30~39
    birthday = models.CharField(max_length=4, blank=True, default="") # MMDD

    # 반드시 필요한 닉네임
    nickname = models.CharField(verbose_name='', max_length=15, unique=True, blank=False, null=True)

    # 유저네임 필드(must be unique)
    USERNAME_FIELD = 'nickname'
    EMAIL_FIELD = 'email'
    
    # 이하 REQUIRED_FIELDS는 createsuperuser 할때 필요한 필드를 지칭함. 다른 DB영역에는 관여 X
    # 이 모델에서는 kakao 유저가 아닌 경우에 email이 꼭 필요하니까 써줘야 함.
    REQUIRED_FIELDS = ['email']
    # use customed UserManager()
    objects = UserManager()

    def __str__(self):
        return self.nickname
    
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

# 위 코드의 장고 짧은 예시 https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example
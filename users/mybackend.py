from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

# 카카오 계정 backend = 첫 로그인 시 가입시킨 내용으로 비교! 
# 카카오는 첫 로그인인지 확인하는 방법이 있다. 바로 user를 user = User.objects.get(kakao_id=)
# 일반 계정 backend는 원래대로 이메일과 패스워드 비교 (kakao_id = None)

class MyBackend(BaseBackend):
    # authenticate() should check the credentials it gets and return a user object that matches those credentials if the credentials are valid. 
    # If they’re not valid, it should return None.
    def authenticate(self, request=None, kakao_id=None, email=None, password=None):
        # Check the kakao_id and return pre-registered user. 
        # Check the email&password and return a user. 
        # 카카오 아이디가 주어졌으면 그 방식 먼저 진행

        # 카카오 아이디 인증 시도이면
        if kakao_id is not None:
            # 찾아보고 있으면 해당 유저를 가져다 줌.
            try:
                user = User.objects.get(kakao_id=kakao_id) # 그러한 유저가 없으면 오류남
                return user
            # 없는 경우에는 
            except User.DoesNotExist:
                return None
        
        # 일반 인증이면 아이디 찾아보고 패스워드 체크하고 해당 유저를 돌려줌. 없으면 None
        else:
            try:
                user = User.objects.get(email=email) #없으면 오류, 있으면 계속 진행
                if password is None:
                    # 이미 있는 이메일로 가입 시도 시 들어오는 루트임 (가입 시 이메일 존재하는지 체크하는 방식으로 이메일 인자만 보내는 것.)
                    return user

                try:
                    validate_password(password, user)
                    # 패스워드가 틀리면 에러 발생시킴
                    return user
                except ValidationError:
                    # 이메일은 있는데 패스워드가 틀리면 None 반환
                    return None
            except User.DoesNotExist: 
                return None

    # 아래의 get_user를 위해 가져온 메소드
    # https://github.com/django/django/blob/main/django/contrib/auth/backends.py#L51
    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    # id값으로 유저 찾기 authentication backend가 되려면 이 함수도 만들어야 함.
    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        # 유저가 활성화 되어 있으면 user 반환, 아니면 None 반환
        return user if self.user_can_authenticate(user) else None

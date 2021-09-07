from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.forms.models import ModelForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# 가입 시 사용되는 폼 
# 폼도 커스터마이징 해야 됐음.
# 유저크레이션 폼 오류남... 패스워드도 잘 받지 못함. 그래서 UserCreationForm의 원리를 확인하고 직접 썼음.
# UserCreationForm has three fields: username (from the user model), password1, and password2. It verifies that password1 and password2 match, validates the password using validate_password(), and sets the user’s password using set_password().

# 회원가입 폼, 입력 에러 핸들링하고, 유저 저장하고, 패스워드 확인하고, 이메일 확인하고, 닉네임 확인하고 저장.
# 패스워드 valiation은 이미 있는 장고의 기능을 사용했음.
# 이메일 인증 메일 보내서 유저 활성화시키는 기능은 카카오 로그인 구현 이후 구현할 예정.
# 이후 패스워드 변경도 구현해야 할 듯, 패스워드 내용은 이 링크 참조 https://docs.djangoproject.com/en/3.2/topics/auth/passwords/ 
class UserSignupForm(forms.Form):
    email = forms.EmailField(label="이메일", required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Password for check", widget=forms.PasswordInput, required=True)
    nickname = forms.CharField(label="닉네임", required=True, max_length=15)
    # class Meta:
    #     model = User
    #     fields = ['email', 'password1', 'password2', 'nickname']
    # .. 닉네임은 중복 확인 안 해도 되는지?
    
    def clean_email(self):
        # email만 인자로 보내서 있는 유저인지 체크 실제로 user가 리턴되면 에러 발생시키기.
        email = self.cleaned_data['email']
        existing_user = authenticate(email=email, backend='users.mybackend.MyBackend')
        if existing_user is not None:
            raise ValidationError("Existing Email")
        # 문제 없으면 에러 없이 리턴
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try: User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            # 닉네임이 중복되는 유저가 없다면 , 중복이 체크되면
            return nickname
        # 유저가 존재하는 경우에는 에러 발생시키기.
        raise ValidationError("Existing Nickname")

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Your passwords do not match")
        try: validate_password(password2, user=User)
            # password validation 실패하면 자체적으로 에러 발생시킴 성공하면 return None
        except ValidationError: 
            raise ValidationError("Your password is not adequate")
        return password2

    def save(self):
        # 이메일, 패스워드 확인 후 저장.
        email = self.clean_email()
        nickname = self.clean_nickname()
        password = self.clean_password2()
        # 실제 유저 저장에 create_user 사용
        # 이메일, 패스워드, 카카오,성별,나이대,생일,닉네임,카카오id
        user = User.objects.create_user(email, password, False, '', '', '', nickname, -1)
        return user



# 로그인 시 사용되는 폼
# AuthenticationForm 을 그대로 이용하면 많은 문제가 발생, subclass도 힘듦.
# 인증 폼을 직접 만들면 된다. 폼 만들고 authenticate 하면 됨.
#

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Login Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    # class Meta:
    #     model = User
    #     fields = ['email', 'password']

    def check_is_active(self, user):
        # 활성화 되어있으면 True, 아니면 False 반환
        return user.is_active

    def authenticate_login(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValueError("Email or Password is not exact.")
            else:
                # 인증되었고, 추가로 active할 시에 True 반환
                if self.check_is_active(user):
                    return True
                # 인증되었지만, inactivated user면 False 반환 
                else:
                    return False
        else:
            raise ValueError("Email and Password should be filled(not empty).")

# 카카오 첫 로그인 시 닉네임으로 가입하기 위한 폼
class NicknameForm(ModelForm):
    class Meta:
        model = User
        fields = ['nickname']

    # def clean_nickname(self):
    #     nickname = self.cleaned_data['nickname']
    #     try: User.objects.get(nickname=nickname)
    #     except User.DoesNotExist:
    #         # 닉네임이 중복되는 유저가 없다면 , 중복이 체크되면
    #         return nickname
    #     # 유저가 존재하는 경우에는 에러 발생시키기.
    #     raise ValidationError("Existing Nickname")




# 이하 두 개는 관리자를 위한 폼임. 가입 시 폼은 UserSignupForm을 만들어서 이용함.
# 사장님 유저 생성 시 이용할 예정
# admin에서 user 추가 시 입력받을 때의 form은 이걸 사용한다.
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example
class AdminUserAddForm(forms.ModelForm):
    # A form for creating new users in admin site. Includes all the required
    # fields, plus a repeated password.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        # User 모델에 정의된 다른 필드를 받고 싶으면 fields 수정 
        # (그냥 유저 생성 하고 싶을 시에는 사장님 관련 필드 제외: 'is_owner', 'related_store')
        fields = ('is_owner', 'nickname', 'email')

    def clean_password2(self):
        # form 유효성 검사 시(form.is_valid())에 사용되는 듯
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # commit = Fasle 식으로 인자가 오지 않으면 저장하고 돌려줌. False는 완전히 저장하는게 아닌 방식. 기본값은 저장.
        if commit:
            user.save()
        return user

# admin에서 유저 수정 시 사용되는 폼
class AdminUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_staff', 'is_active', 'is_kakao', 'is_owner', 'nickname')
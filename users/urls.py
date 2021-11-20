from django.urls import path
from .views import *


urlpatterns= [
    # 로그인 홈 화면, 이메일 가입, 로그인
    path('login/home/', login_home, name="login_home"), # 로그인 홈
    path('signup/email/', signup_email, name="signup_email"), # view에서 .create_user(...) 사용해야 함.
    path('login/email/', email_login, name="email_login"), # 이메일로 authenticate()

    # 카카오 로그인, 통합 로그아웃, 마이페이지
    path('login/kakao/', kakao_login, name="kakao_login"),
    path('kakao/login/callback/', kakao_login_callback, name="kakao_login_callback"), # 사용자가 로그인하고 로그인한 결과로 인증코드가 서버로 들어오는 곳, 인증 코드로 요청한 액세스 토큰이 들어오늘 곳(카카오 나의 앱에서 설정 가능)
    path('kakao/submit/nickname', submit_nickname, name="submit_nickname"),
    path('logout/', logout_view, name="logout"), # user logout 시키기 (view에서 카카오 유저 구분)
    path('logout/with/kakao', logout_with_kakao, name="logout_with_kakao"),
    path('mypage/<int:user_pk>', mypage, name="mypage"),

    # 쿠폰 내역, 정보 변경(닉네임), 회원 탈퇴
    path('mypage/<int:user_pk>/coupons', view_coupon, name='view_coupon'),
    path('mypage/edit/nickname', edit_nickname, name='edit_nickname'),
    path('mypage/delete/user/<int:user_pk>', delete_user, name='delete_user'),
]
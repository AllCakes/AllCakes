from logging import raiseExceptions
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from cakeManage.models import *
from .models import User
from .forms import NicknameForm, UserSignupForm, EmailAuthenticationForm
# for kakao login
from django.conf import settings
import requests
import random
from django.utils import timezone
from datetime import datetime
# Create your views here.

# 커스텀 백엔드 이름 : 'users.mybackend.MyBackend'
# 그 커스텀백엔드에 정의된 authenticate(request=None, kakao_id=None, email=None, password=None)가 authenticate에서 호출됨.

# .cleaned_data 이해 필요하면 참고 : https://docs.djangoproject.com/en/3.2/ref/forms/api/#accessing-clean-data

# authenticate(email=email, password= password) 여기에서 keyword arguments 사용이 익숙치 않다면 아래 링크 참조
# https://www.geeksforgeeks.org/default-arguments-in-python/

# 즉 수퍼 유저 빼고는 모두 custom된 authenticate를 써야 하므로,
# authenticate(필요한 파라미터= 변수, ,... backend='users.mybackend.MyBackend')
# 이런식으로 해야 한다.


#로그인 홈
def login_home(request):
    return render(request, 'login_home.html')

# 이메일 회원가입
def signup_email(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 생성, 저장 완료 # 이메일이 중복되었는지는 폼에서 따로 체크하도록 구현(현재 유저네임필드는 닉네임이라 인증을 따로 만들었음.)
            login(request, user, backend='users.mybackend.MyBackend') # https://docs.djangoproject.com/en/3.2/topics/auth/default/#how-to-log-a-user-in
            return redirect('login_home')
    else:
        form = UserSignupForm()
    return render(request, 'signup_email.html', {'form':form})

# 이메일로 로그인
def email_login(request):
    if request.method=="POST":
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            # form 에서 인증 한번, 오류input 잡아주기 위해서!
            if form.authenticate_login():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                # 실제 로그인 전 인증
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user, backend='users.mybackend.MyBackend') # https://docs.djangoproject.com/en/3.2/topics/auth/default/#how-to-log-a-user-in
                    request.user.last_login= timezone.now()
                    return redirect('home')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'email_login.html', {'form':form})


# 이전 뷰에서 이미 유저를 저장하고 로그인 했기 때문에, request속 유저의 닉네임만 바꿔주면됨.
# 즉 닉네임을 변경하고 설정해줌.
def submit_nickname(request):
    if not request.user.is_authenticated:
        raise ValidationError("잘못된 접근입니다.")
    if request.method=="POST":
        form = NicknameForm(request.POST, instance=request.user)
        if form.is_valid():
            # 닉네임 중복 체크는 이미 되어 있겠지만, 다시 확인.
            # form.clean_nickname() user모델과 엮여 있는 form이라 확인 필요 없음.
            form.save()
            # 유저 생성 완료
            # 로그인 시키고 home으로 돌아가기, 이후 state를 활용하여 유저를 가게 상세로 돌릴 수 있음.
            return redirect('home')
    else:
        form = NicknameForm()
    return render(request, 'submit_nickname.html', {'form':form})



# 카카오 로그인 (코드 요청하기)
# 1. 로그인화면 호출하고 사용자 동의를 거쳐서 
# 2. 인가 코드를 redirect_uri로 보내줌.
# 3. 즉, 로그인 창을 부르며 redirect uri로 인가 코드 요청하는 api

# 카카오 동의항목 철회, 동의내역 조회, 추가항목 동의받기 등 구현해야할 것들 아직 남음.
# 실제 서비스 시 추가로 카카오로부터 연결끊기 알림도 구현. -> XX 연결 끊기는 선택임.
# 서비스 회원 가입 및 탈퇴: 서비스 회원 가입은 각 서비스 회원 정보에 카카오계정 사용자 정보를 회원으로 저장하는 일입니다.
#  이는 연결과 별개의 처리입니다. 카카오계정으로 로그인한 사용자 정보를 서비스 서버에 회원 가입 처리하지 않으면 
# 정상적인 가입 처리가 완료되지 않습니다.서비스 회원 탈퇴 또한 서비스가 자체적으로 구현해야 합니다. 연결 끊기는 카카오계정과 앱의 관계만 끊을 뿐, 서비스 서버에 저장된 회원 정보까지 지우지 않기 때문입니다
# https://developers.kakao.com/docs/latest/ko/kakaologin/common#link-and-unlink

# django-environment 라이브러리를 설치하고 이용하여 .env에서 키 값을 가져옴.
# https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f 참고
def kakao_login(request):
    # 이미 로그인한 상태면 카카오 로그인 안 되도록
    if request.user.is_authenticated:
        raise Exception("User already logged in")
        



    rest_api_key = settings.KAKAO_REST_API_KEY
    # "main_domain"/앱이름과 관련된 url연결
    redirect_uri = "http://127.0.0.1:8000/users/kakao/login/callback/"

    # 전달되어야 할 문자열 "(string)" "none"상태를 계속 전달하여 이후 로그인 홈으로 갈지 "store pk값"을 전달하여 이후 상세페이지로 돌아갈지 구현해야 함.
    state = "none"
    # 카카오가 인증 수행 후 redirect_uri로 인가 코드(request)를 보내준다. 그래서 urls.py에 kakao_login_callback이 실행되도록 잘 등록해놔야 함.
    # get 방식으로 전달해야 하는 Parameter: client_id, redirect_uri, response_type=code (code로 고정)
    # 선택적 Parameter: state -> 로그인 요청과 콜백 간에 상태를 유지하기 위해 사용되는 임의의 문자열(정해진 형식 없음) Cross-Site Request Forgery(CSRF) 공격으로부터 보호하기 위해 해당 파라미터 사용을 권장함
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code&state={state}")

# redirect_uri에 들어오는 카카오api 응답: 인가 코드 요청의 응답은 redirect_uri로 HTTP 302 Redirect되며,
# Location에 인가 코드가 담긴 쿼리 스트링(Query String) 또는 에러 메시지를 포함합니다. 
# 사용자가 [취소] 버튼을 클릭한 경우에는 에러 메시지를 담은 쿼리 스트링이 redirect_uri로 전송됩니다.
# 서비스 서버는 redirect_uri로 받은 요청을 처리해 인가 코드를 얻거나 상황에 맞는 페이지를 보여주도록 처리해야 합니다.
# 받은 인가 코드는 토큰 받기에 사용합니다.



# 카카오 로그인 토큰 받기
# requests module 사용법: https://dgkim5360.tistory.com/entry/python-requests
# 카카오 REST_API url request 형식, 데이터 형식 https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api
# 파이썬의 REST_API 다루는 방법: requests 이용하기!
# The clear, simple syntax of Python makes it an ideal language to interact with REST APIs, and in typical Python fashion, there’s a library made specifically to provide that functionality: Requests. from: https://www.nylas.com/blog/use-python-requests-module-rest-apis/

# 사용자의 access token 받기
def kakao_login_callback(request):
    # 성공적으로 인가 코드가 온 경우와, 에러메세지가 온 경우를 나눠야 함. (즉, 필수동의항목에 동의하고 로그인한 경우 or 사용자가 카카오로그인 창에서 취소를 누른 경우)
    # 인가 코드가 온 경우 카카오 서버에 request(POST)를 전달하여 토큰을 받는 것까지 구현하도록 함.
    # 인가코드 받기 성공 시 응답: {REDIRECT_URI}?code={AUTHORIZE_CODE} 실패 시 응답: {REDIRECT_URI}?error=access_denied&error_description=User%20denied%20access
    # try:
    code = request.GET.get("code")
    if code is None:
        raise Exception("code is none")
    state = request.GET.get("state") # state는 보냈던 그대로 담겨서 옴. 이후 상세한 state처리는 나중에
    
    # 카카오 서버로 POST request 보내기, 관련 내용-> POST HTTP/1.1 Content-type: application/x-www-form-urlencoded;charset=utf-8
    # 토큰 요청할 url: /oauth/token Host: kauth.kakao.com 

    # requests.POST 방법: https://docs.python-requests.org/en/master/user/quickstart/
    # post request, 커스텀header 등 많은 정보가 있다. content-type 헤더 없어서 요청 안되면 고치기!

    token_url = "https://kauth.kakao.com/oauth/token"
    rest_api_key = settings.KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/kakao/login/callback/"
    # Response Object called res 
    res = requests.post(token_url, data={'grant_type':'authorization_code', 'client_id':rest_api_key, 'redirect_uri':redirect_uri, 'code':code}) 
    
    token_response = res.json()
    access_token = token_response.get('access_token')
    # 토큰 요청 및 저장 완료 (카카오 서버 상 로그인 완료된 것)

    # 이하 부분 카카오 REST API 사용자 정보 가져오기 참조 -> 요청을 거쳐 사용자 정보를 info에 담음.
    info_url = "https://kapi.kakao.com/v2/user/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'secure_resource': True}
    info_res = requests.get(info_url, headers=headers, params=params)
#응답 예시 {
#   "id": {int값},
#   "connected_at": "2021-08-02T11:52:31Z",
#   "properties": {
#     "nickname": {string값}
#   },
#   "kakao_account": {
#     "profile_needs_agreement": false,
#     "profile": {
#       "nickname": {string값},
#       "thumbnail_image_url": {url string값},
#       "profile_image_url": {url string값},
#       "is_default_image": true
#     },
#     "has_email": true,
#     "email_needs_agreement": false,
#     "is_email_valid": true,
#     "is_email_verified": true,
#     "email": {string값},
#     "has_age_range": true,
#     "age_range_needs_agreement": false,
#     "age_range": "20~29",
#     "has_birthday": true,
#     "birthday_needs_agreement": false,
#     "birthday": {string값},
#     "birthday_type": "SOLAR",
#     "has_gender": true,
#     "gender_needs_agreement": false,
#     "gender": "male"
#   }
# }
    try:
        info = info_res.json()
        print(info)
    except:
        print("error from here")
        info = None

    kakao_id = info.get("id")
    # 인증과 저장을 위해 string으로 바꿔줌
    kakao_id = str(kakao_id)


    # id를 이용해서 첫 가입인지 먼저 확인
    # 유저를 인증시켜보고 첫 가입과 로그인을 나눔.
    try :
        test = User.objects.get(kakao_id=kakao_id)
    except User.DoesNotExist:
        test = None
    print(test)
    # 첫 가입이라면 정보를 받아오고 닉네임 입력을 받아야 함.
    if test is None:
        # kakao_account 부분에서 미리 설정한 동의항목의 내용을 조회함.
        # 세 가지 정보를 받아야 함. gender, age_range, birthday
        personal_info = info.get("kakao_account")

        agree_on_birthday = personal_info.get("birthday_needs_agreement")
        if not agree_on_birthday: # 동의가 필요없으면, 즉 동의를 이미 했으면
            birthday = personal_info.get("birthday")
        else:
            birthday = ''
        agree_on_gender = personal_info.get("gender_needs_agreement")
        if not agree_on_gender: # 동의가 필요없으면, 즉 동의를 이미 했으면
            gender = personal_info.get("gender")
        else:
            gender=''
        agree_on_age_range = personal_info.get("age_range_needs_agreement")
        if not agree_on_age_range: # 동의가 필요없으면, 즉 동의를 이미 했으면
            age_range = personal_info.get("age_range")
        else:
            age_range=''

        print(kakao_id)
        print(birthday)
        print(gender)
        print(age_range)

        # 첫 가입이면 닉네임 입력으로 이동함. 
        # 유저를 디비에 올리고 pk값 전달해서 모델폼으로 닉네임만 바꿔주도록 한다. 
        # 유저가 나가버리면 랜덤닉네임 그대로 갖도록 함.
        rand_nickname = "ALLcaker" + str(random.randrange(1,99999))
        print(rand_nickname)

        # 랜덤 닉네임이 중복되는지 확인
        while True:
            try: user = User.objects.get(nickname=rand_nickname)
            except User.DoesNotExist: user = None 
            if user is not None:
                #유저가 있으면 랜덤닉네임 새로 생성
                rand_nickname ="ALLcaker" + str(random.randrange(1,99999))
            else:
                break

        # 유효한 랜덤 닉네임 완료. 반복문 오류 생기는데 왜..?
        # User.Doesnotexist Exception이 일어나기 때문
        # 결국 try로 해결함
        
        
        # 유저 DB에 저장(가입) 및 로그인시키기 email, password, is_kakao, gender, age_range, birthday, nickname, kakao_id
        user = User.objects.create_user(None, None, True, gender, age_range, birthday, rand_nickname, kakao_id)
        login(request, user, backend='users.mybackend.MyBackend')

        # 쿠폰 생성 시도
        coupon = AmountCoupon()
        coupon.amount = 2000
        coupon.name = "신규 회원가입 쿠폰"
        coupon.use_from = timezone.now
        d = datetime.strptime('2025-12-31', '%Y-%m-%d')
        coupon.use_to = d
        coupon.is_active = True
        coupon.user = user
        coupon.save()

        form = NicknameForm()
        return render(request, 'submit_nickname.html', {'form':form})

    # 첫 가입이 아니라면
    else:
        login(request, test, backend='users.mybackend.MyBackend')
        # 카카오 로그인에 들어온 상황이 none이면 홈으로, 아니면 가게 pk값으로 보내주기
        request.user.last_login= timezone.now()
        if state=="none":
            return redirect('home')
        else:
            return redirect('home')

    # except:
    #     # 인가코드가 오지 않고 에러메세지가 온 경우임. 이후 로그인 실패 설명 배너가 필요하면 상세히 구현하도록 함.
    #     error = request.GET.get("error")
    #     print(error)
    #     print("why here?")
    #     # 토큰 발급 요청 POST를 보낸 경우에도 이곳으로 오는데, ...?
    #     state = request.GET.get("state") # state는 보냈던 그대로 담겨서 옴.
    #     if state == "none":
    #         return redirect('login_page')
    #     # store pk값을 state에 받아온 경우에는 나중에 구현 (탬플릿과 연결되는 내용이기 때문), 이하 else문 삭제 가능.
    #     else:
    #         return redirect('home')


# 유저를 로그아웃 시키기 전에 카카오 유저이면 발급받은 토큰을 만료시키는 카카오 로그아웃을 먼저 진행
# 카카오 로그아웃은 어드민 키와 유저 id(from kakao and saved in our DB) 이용해서 로그아웃시킴.
# 이 함수는 카카오 계정과 함께 구현 시 로그아웃 콜백함수가 됨. 
# logout redirect uri : http://127.0.0.1:8000/users/logout/
# 즉, 이 뷰로 오게 하면 됨. 
def logout_view(request):
    # 카카오 유저이면
    if request.user.is_kakao:
        # 카카오 id와 어드민키를 통해 먼저 로그아웃 시키고, 이후 우리 서버에서도 로그아웃 시키기.
        kakao_admin_key = settings.KAKAO_ADNIN_KEY 
        logout_url = "https://kapi.kakao.com/v1/user/logout"
        # KakaoAK 에서 앞의 K와 뒤의 K는 대문자 
        target_id = request.user.kakao_id
        target_id = int(target_id)
        headers = {'Authorization': f'KakaoAK {kakao_admin_key}'}
        data = {'target_id_type':'user_id','target_id':target_id}
        logout_res = requests.post(logout_url, headers=headers, data=data)
        
        logout_res = logout_res.json()
        response = logout_res.get("id")
        if target_id != response:
            # 로그아웃 실패
            return Exception('Kakao Logout failed')
        else:
            print(str(response) + "카카오 로그아웃 성공")
    # 유저에 따라 카카오 로그아웃 먼저 진행 후 서버 로그아웃이 진행됨.
    # logout: Remove the authenticated user's ID from the request and flush their session data.
    logout(request)
    # 이전 state를 그대로 get에 담아 전달해줄 수 있기 때문에, 여기서 state정보를 확인하고
    # redirect를 어디로 할지 정할 수 있음
    # 구현 예시: if request.GET.get("state") is not None: return redirect('detail', state에 담긴 pk값)
    return redirect('home')

# 카카오 계정과 함께 로그아웃 선택 페이지로 가게 함.
# 사용자의 편의를 위해 state를 넘겨 보냄. 이후 구현 필요.
def logout_with_kakao(request):
    # GET 요청 정보들
    kakao_rest_api_key = settings.KAKAO_REST_API_KEY
    logout_redirect_uri = "http://127.0.0.1:8000/users/logout/" # 서비스 로그아웃을 수행하도록 함 이 때, state로 전달된 값을 참고해 볼 수 있음.
    state = "none" # 필요한대로 수정 가능. Logout 클릭 시 특정 pk값을 받아와 state에 담는 게 가장 좋은 활용방안.
    kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"
    
    # params = {'client_id':kakao_rest_api_key,'logout_redirect_uri':logout_redirect_uri,'state':state}
    # 이하 GET방식 요청
    return redirect(f"{kakao_service_logout_url}?client_id={kakao_rest_api_key}&logout_redirect_uri={logout_redirect_uri}&state={state}")

# **제가 구현할 때는 먼저 토큰만료 방식의 카카오 로그아웃을 logout_view에 구현했는데, 처음부터 카함로(세션만료 방식 카카오 로그아웃)를 구현할 예정이라면, 굳이 토큰 만료 방식의 내용을 구현하지 않아도 됩니다. 즉, 아래의 logout_view의 첫 if 부분이 사라져도 영향이 없습니다. **




def mypage(request, user_pk):
    reviews = Review.objects.filter(user=user_pk).order_by('-pub_date')[:4] # 최근 것 4개
    orders = Order.objects.filter(is_active=True)[:4] #진행 중 주문 최근걸로 최대 2개
    liked_cakes = Cake.objects.filter(users_liked=user_pk)[:5]
    liked_stores = Store.objects.filter(users_liked=user_pk)[:5]
    return render(request, 'mypage.html', {'user_pk': user_pk,'reviews':reviews, 'orders':orders,'liked_cakes':liked_cakes, 'liked_stores':liked_stores})


def edit_nickname(request):
    if not request.user.is_authenticated:
        raise ValidationError("잘못된 접근입니다.")

    if request.method=="POST":
        form = NicknameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            user_pk = request.user.pk
            return redirect('mypage', user_pk=user_pk)
    else:
        form = NicknameForm(instance=request.user)
    return render(request, 'edit_nickname.html', {'form':form})

def delete_user(request, user_pk):
    # 본인과 삭제 요청 대상이 일치하면, 그리고 카카오면 카카오 연결까지 끊고 나서 삭제
    user =request.user
    if user.pk == user_pk:
        if user.is_kakao:
            # kakao 연결 끊기
            kakao_admin_key = settings.KAKAO_ADNIN_KEY
            user_kakao_id = int(user.kakao_id) # 형변환 필요
            url = "https://kapi.kakao.com/v1/user/unlink"
            headers = {'Authorization':f'KakaoAK {kakao_admin_key}'}   #대소문자 주의
            data = {'target_id_type':'user_id','target_id': user_kakao_id}

            res = requests.post(url, headers=headers, data=data)
            # 성공시 응답은 회원번호로 받음
            deleted_user_id = res.json().get("id")
            if deleted_user_id == user_kakao_id:
                print("연결 끊기 성공")
            else:
                print("연결끊기 실패")
        
        # 카카오 체크가 마무리 됐으면 세션 로그아웃, 유저 삭제 진행
        logout(request)
        user.delete()
        return redirect('home')
    else:
        raise ValidationError("잘못된 접근입니다.")
        
def view_coupon(request, user_pk):
    if request.user.pk != user_pk:
        raise ValidationError("잘못된 접근입니다.")
    AmountCoupons = AmountCoupon.objects.filter(user=user_pk)
    PercentCoupons = PercentCoupon.objects.filter(user=user_pk)

    return render(request, 'view_coupon.html', {'AmountCoupons': AmountCoupons, 'PercentCoupons':PercentCoupons})
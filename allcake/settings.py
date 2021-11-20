#kdy : superuser : milkcream qpqpqp0614
"""
Django settings for allcake project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv      
# python-dotenv : API, AWS서버 연결 등등에 필요한 시크릿 키값을 저장할 때 쓰기 좋음.
import os
# .env에 있는 내용을 os environment에 불러오고, 이후 os.getenv로 가져오면 된다.
load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY") # 대문자로 적어줘야 함.
KAKAO_ADNIN_KEY = os.getenv("KAKAO_ADMIN_KEY")
KAKAO_MAP_API_KEY = os.getenv("KAKAO_MAP_API_KEY")






# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6_oy(3h3pwtnk&(i&r0u9krlp@p&=a917iqt72emcn&ek*-dl2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # folllowing apps for social login and user management
    'users',

    # following apps for our project
    'cakeManage',

    # isotope effect
    'isotope',

    # ...followed by defalult
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
]

CKEDITOR_UPLOAD_PATH = "uploads/"

# to use a model users.User for authentication, replacing the default django.contrib.auth.models.User
AUTH_USER_MODEL = 'users.User'

# custom user referring: use the get_user_model() method from django.contrib.auth
# The method is preferred — certain for code that you intend to re-use — as it deals with both the default and custom user models.

# following setting for django login, social login 
# 로그인에서 사용할 인증 방식을 정함.
# authenticate 함수는 명시된 백엔드 순서대로 인증을 시도함.
# 'django.contrib.auth.backends.ModelBackend'는 기본 모델인데, 관리자 계정 인증을 위해 필요함. allauth는 사용 안 했음.
AUTHENTICATION_BACKENDS =(
    'users.mybackend.MyBackend',
    'django.contrib.auth.backends.ModelBackend',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'allcake.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'cakeManage' / 'templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'allcake.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# media_root, dir, url

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'





# STATICFILES_DIRS = ( os.path.join('static'), )
# STATIC_URL = '/static/' 
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ( 
#    os.path.join(BASE_DIR, "static"),
    BASE_DIR / 'allcake' / 'static',

)
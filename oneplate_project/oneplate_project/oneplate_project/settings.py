"""
Django settings for oneplate_project project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--2%j_#^(mnu_$z9vh0aseicw$*)qr^ot6o$f3!cjaz2$s)v+vo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    'rest_framework',
    # 'rest_framework.authtoken',
    'dj_rest_auth',
    'drf_yasg',
    'oneplate',

]
# django-allauth에서 필수로 사용하는 Site ID 설정
SITE_ID = 1

REST_AUTH = {
    'USE_JWT': False,  # JWT 사용을 비활성화 (토큰 기반 인증 사용 안함)
    'TOKEN_MODEL': None,  # 토큰 기능을 비활성화하려면 이 설정을 추가
    'SESSION_LOGIN': True,
    'USER_DETAILS_SERIALIZER': 'oneplate.serializers.UserSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'UNICODE_JSON': True,  # 이 줄을 추가
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Django 기본 인증 백엔드
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth 인증 백엔드
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF 미들웨어 포함
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'oneplate_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'oneplate_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
from decouple import config


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oneplate_db',
        'USER': 'oneplate',
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }

}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'  # UTC 대신 한국 시간대로 변경

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Auth settings
AUTH_USER_MODEL = 'oneplate.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # 이메일 인증 필수
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
'''
이 두가지 설정이 이메일 인증 후 리다이렉션에 힌트가 될듯
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/?verification=1'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/?verification=1'
'''
'''
이후 로그인 페이지 작성시 참고
# 이메일 인증 여부
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # "none", "optional", "mandatory"
ACCOUNT_EMAIL_REQUIRED = True  # 이메일 필수 여부
ACCOUNT_USERNAME_REQUIRED = False  # 사용자 이름을 사용하지 않을 경우 False

# 로그인 후 리다이렉트 URL 설정
LOGIN_REDIRECT_URL = '/'  # 로그인 후 리다이렉트할 경로
LOGOUT_REDIRECT_URL = '/accounts/login/'  # 로그아웃 후 리다이렉트할 경로

# 회원가입 시 이메일 인증을 사용하려면 이 옵션도 추가
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 로그인 시도 제한 시간 (초)
'''
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/uploads/'

FILE_CHARSET = 'utf-8'
DEFAULT_CHARSET = 'utf-8'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from drf_yasg import openapi
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,  # 세션 기반 인증 사용 여부
    'SECURITY_DEFINITIONS': {
        'csrfToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-CSRFToken'
        }
    },
    'DEFAULT_INFO': openapi.Info(
        title="API Documentation",
        default_version='v1.1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="skskfl5786@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    'CHARSET': 'utf-8',
    # 'LOGIN_URL': 'account_login',  # 로그인 URL 네임스페이스
    # 'LOGOUT_URL': 'account_logout',  # 로그아웃 URL 네임스페이스
    # 기타 Swagger 설정...
}
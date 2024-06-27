"""
Django settings for Streetsuite project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ze!xanmdw6x-z25g9sye)0=v!5j2&(^otowa24-u^_1)3b*lti'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',
                 'abdulrahman.onrender.com',
                 'localhost:8000',
                 'localhost:3000',              
]


# Application definition

INSTALLED_APPS = [
    'UserApp',
    'BlogApp',
    'Payment',
    'QuizApp',
    'vacancies',
    'contactus',
    'change_log',
    'CourseApp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'django.contrib.sites',
    'stripe',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'corsheaders',    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Streetsuite.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Streetsuite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
],

}
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
    # 'twitter': {
    #     'SCOPE': [
    #         'email',
    #     ],
    # },
    # 'apple': {
    #     'SCOPE': [
    #         'name',
    #         'email',
    #     ],
    #     'AUTH_PARAMS': {
    #         'access_type': 'online',
    #     },
    # },
}
AUTHENTICATION_BACKENDS = [
    
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
    'drf_social_oauth2.backends.DjangoOAuth2'
    
]

# Google Configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
LOGIN_REDIRECT_URL = '/blogs/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'


STRIPE_SECRET_KEY = 'sk_test_51PNAn4Bizf1bE4kFXqRaCarCuQUQGju0c6QVbxcpCK0dWLveCd05FaNtLZ2Vh6mwns6dOhbvLZVsgDUz7TTN38HF00IbVQx9Ov'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51PNAn4Bizf1bE4kF5t6GuaMhTbT9nU02TJD0Sw0ANJBD8BFfjiVamDKYXDPsS8YIpNTlLddW2MmM88gxwZ6AmMTG00nOn5E1kP'

MEDIA_ROOT =  BASE_DIR / "Media"

MEDIA_URL = "Media/"

#### for gmail verification ####
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Port for SMTP
EMAIL_USE_TLS = True  # Transport Layer Security is required by Gmail
EMAIL_HOST_USER = 'streetsuits0@gmail.com'  # Your Gmail address
EMAIL_FROM = 'streetsuits@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'tbwhhfcgckolpiim'
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER") # Your Gmail address
# EMAIL_FROM = os.getenv("EMAIL_FROM")  # Your Gmail address
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Your Gmail password or app-specific password
# DEFAULT_FROM_EMAIL = 'streetsuits@gmail.com'  # Default sender email address
PASSWORD_RESET_TIMEOUT = 14400


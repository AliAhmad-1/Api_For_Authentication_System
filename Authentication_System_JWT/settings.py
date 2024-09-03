

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

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
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'app',
    #new for social oauth2
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Authentication_System_JWT.urls'

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

WSGI_APPLICATION = 'Authentication_System_JWT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'drf_social_oauth2.authentication.SocialAuthentication',
    ),
}
AUTHENTICATION_BACKENDS = (

    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =str(os.getenv('GOOGLE_OAUTH2_KEY'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET =str(os.getenv('GOOGLE_OAUTH2_SECRET'))
SOCIAL_AUTH_GITHUB_KEY =str(os.getenv('GITHUB_KEY'))
SOCIAL_AUTH_GITHUB_SECRET =str(os.getenv('GITHUB_SECRET'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti"

    }


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

PASSWORD_RESET_TIMEOUT=900   #900 SEC ---> 15 MINUTE


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER =str(os.getenv('EMAIL_USER'))
EMAIL_HOST_PASSWORD =str(os.getenv('EMAIL_PASSWORD'))






# curl -X POST -d "grant_type=convert_token&client_id=tpxYXmzgVdJNk6bcmFW5YkrWG0TH2RALBbxZpWOf&backend=google-oauth2&token=ya29.a0AcM612x6pxi-IElHkntWBgNUUwIkpdLMwj8UFA__FZUCKnMyEMonwKlcyLLrzLQWwvljYOXNhVSQc_tYpYi4ed-RX5DFjmmsCuTHwXxCxLfXtY1zr--aCtNEcIZnJIQaYu3MsYAwunGtdqffDZVEowAdMnvmZfe8TgaCgYKAQESARISFQHGX2Mip_jk4ZMnbgcwLV6bnkR5QA0169" http://localhost:8000/auth/convert-token

# curl -X POST -d "client_id=tpxYXmzgVdJNk6bcmFW5YkrWG0TH2RALBbxZpWOf&client_secret=Rk0ILj2ML3i97xPmAZUdetPaGWsrdmY0B7CxWAmMKupyzfi7OImx1QhOj8UsYgydWqGYwbYyD0EcCBmmRAU6pwWT4EJa3khIHAtouKa2wZftwxZj0rAdsDkOVf8bQZR5&grant_type=password&username=asus@gmail.com&password=asus" http://localhost:8000/auth/token


# 4605b7b25d270561d1ca
# https://github.com/login/oauth/access_token?client_id=Ov23lisNOOUseR88CGdI&client_secret=122ed14bcef93411fa64475084fd2f1afa45a992&code=4605b7b25d270561d1ca
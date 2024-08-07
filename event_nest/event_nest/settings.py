import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=os.environ['DEBUG']
ALLOWED_HOSTS = []


# time zone
TIME_ZONE = 'Asia/Karachi'
USE_TZ = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #apps
     'organizer',
     'attendee',
     'authentication',
     # JWT
     'rest_framework_simplejwt',
     #drf
      'rest_framework',
     # oauth2
     'allauth',
     'allauth.account',
     'allauth.socialaccount',
     'allauth.socialaccount.providers.google',
      # API documentation-swagger
      'drf_spectacular',
      # Coverage
      'coverage',

]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # oauth
     'allauth.account.middleware.AccountMiddleware',

]
INTERNAL_IPS = [
    '127.0.0.1',
]
ROOT_URLCONF = 'event_nest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'organizer/templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #oauth2
            ],
        },
    },
]

WSGI_APPLICATION = 'event_nest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD':os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'], 
        'PORT':  os.environ['DB_PORT'],
        'TEST':{
            'NAME': 'test_event_nest'
        }
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

MEDIA_ROOT = BASE_DIR / 'media/'

# drf
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #JWT
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Oauth
        'allauth.account.auth_backends.AuthenticationBackend',

    ),
    # Spectacular-swagger
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'organizer.serializer.OrganizerSerializer',
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': True,
}
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', 
    # Oauth2 google backends
]



# auth user models and auth social model
AUTH_USER_MODEL = 'organizer.EventNestUsers'

# email settings
EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# Spectacular (swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Event Nest',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'defaultModelsExpandDepth': -1,
        'persistAuthorization':True
    },
    'SECURITY':[
        {'Bearer':[]}
    ],
    'SECURITY_DEFINITIONS':{
        'Bearer':{
            'type': 'apiKey',
            'in':'header',
            'name': 'Authorization',
        }
    }
}


# oauth2
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google':{
        'SCOPE':[
            'profile',
            'email',
        ],
        'AUTH_PARAMS':{
            'access_type': 'online'
        }
    }
}
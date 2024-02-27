"""
Django settings for E_commerce project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import dj_database_url
from pathlib import Path
import os
from django.contrib import messages
from dotenv import load_dotenv, find_dotenv
import mimetypes

DEBUG = False

mimetypes.add_type("text/css", ".css", True)
load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
if DEBUG:
    MEDIA_URL = '/media/'

# environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING  : keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!


# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['summit-shop.up.railway.app']
CSRF_TRUSTED_ORIGINS=['https://summit-shop.up.railway.app']

# Application definition

INSTALLED_APPS = [

        # My Apps
    'Accounts',
    'store',
    'phonenumber_field',
    'django_countries',
    "paystack.frameworks.django",
    'storages',
    'collectfast',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
]

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'E_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'libraries': {
                'paystack': 'paystack.frameworks.django.templatetags.paystack',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processor.website_content',
                # 'store.context_processor.wishlist_counts',
            ],
        },
    },
]

# TEMPLATE_DIRS = (
#     'templates\base.html',
# )

WSGI_APPLICATION = 'E_commerce.wsgi.application'

if not DEBUG:
    # AWS S3 SETTINGS
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400'
    }

    AWS_LOCATION = 'static'
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Access-Control-Allow-Origin': '*',
    }

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    DEBUG_PROPAGATE_EXCEPTIONS = True


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=f"postgresql://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@{os.environ.get('PGHOST')}:{os.environ.get('PGPORT')}/{os.environ.get('PGDATABASE')}", conn_max_age=600)
}
    
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': 'e_commerce',
#     'USER': 'postgres',
#     'PASSWORD': 'test123',
#     'HOST': 'localhost',
#     'PORT': '5432',
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',    #causes verbose duplicate notifications in django 1.9
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

if DEBUG:
    STATIC_URL = '/static/'



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = 'https://d1q43jnb3s7abw.cloudfront.net/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# PHONWNUMBERFIELD
PHONENUMBER_DB_FORMAT = 'INTERNATIONAL'


# LOGIN_REDIRECT_URL = 'checkout'
# LOGOUT_REDIRECT_URL = 'venlogin'

AUTH_USER_MODEL = 'Accounts.User'

# PAYSTACK
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'Summit Team <noreply@summit.com>'
# SERVER_EMAIL = os.environ.get('EMAIL_HOST_USER')


CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_HTTPONLY = False
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# if not DEBUG:
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'formatters': {
    'verbose': {
        'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        'datefmt' : "%d/%b/%Y %H:%M:%S"
    },
    'simple': {
        'format': '%(levelname)s %(message)s'
    },
},
'handlers': {
    'file': {
        'level': 'DEBUG',
        'class': 'logging.FileHandler',
        'filename': 'mysite.log',
        'formatter': 'verbose'
    },
},
'loggers': {
    'django': {
        'handlers':['file'],
        'propagate': True,
        'level':'DEBUG',
    },
    'MYAPP': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
}

# STATIC_HOST = "d1q43jnb3s7abw.cloudfront.net"
# STATIC_URL = STATIC_HOST + "/static/"
# del DATABASES['default']['OPTIONS']['sslmode']
"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 4.0.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str),
    ALLOWED_HOSTS=(str, '*'),

    # Used same database for all schema,
    # But we have different users per schema with different permissions
    DB_NAME=(str, 'postgres'),

    # Django default schema for auth and django stuffs, we have all access in production
    DJANGO_DB_USER=(str, 'postgres'),
    DJANGO_DB_PASSWROD=(str, 'postgres'),
    DJANGO_DB_HOST=(str, 'db'),
    DJANGO_DB_PORT=(int, 5432),

    # Visualiztion schema we have read only permission in production
    VISUALIZATION_DB_USER=(str, 'postgres'),
    VISUALIZATION_DB_PASSWROD=(str, 'postgres'),
    VISUALIZATION_DB_HOST=(str, 'db'),
    VISUALIZATION_DB_PORT=(int, 5432),

    # Production schema, we have read write acess in few tables only,
    # Used for csv migrate from django to production database
    PRODUCTION_DB_USER=(str, 'postgres'),
    PRODUCTION_DB_PASSWROD=(str, 'postgres'),
    PRODUCTION_DB_HOST=(str, 'db'),
    PRODUCTION_DB_PORT=(int, 5432),

    # Schama names
    # NOTE: For visualization schema is default public
    DJANGO_SCHEMA_NAME=(str, 'django'),
    RCCE_PRODUCTION_SCHEMA_NAME=(str, 'data'),
    RCCE_VISUALIZATION_SCHEMA_NAME=(str, 'default'),

    TIME_ZONE=(str, 'Asia/Kathmandu'),
    CORS_ALLOWED_ORIGINS=(list, ['http://localhost:3050']),
    # Static, Media configs
    DJANGO_STATIC_URL=(str, '/static/'),
    DJANGO_MEDIA_URL=(str, '/media/'),
    DJANGO_STATIC_ROOT=(str, os.path.join(BASE_DIR, "staticfiles")),
    DJANGO_MEDIA_ROOT=(str, os.path.join(BASE_DIR, "media")),
    USE_LOCAL_STORAGE=(bool, True)
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'apps.visualization',
    'corsheaders',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DJANGO_SCHEMA_NAME = env('DJANGO_SCHEMA_NAME')
RCCE_PRODUCTION_SCHEMA_NAME = env('RCCE_PRODUCTION_SCHEMA_NAME')
RCCE_VISUALIZATION_SCHEMA_NAME = env('RCCE_VISUALIZATION_SCHEMA_NAME')

DATABASES = {
    RCCE_VISUALIZATION_SCHEMA_NAME: {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('VISUALIZATION_DB_USER'),
        'PASSWORD': env('VISUALIZATION_DB_PASSWROD'),
        'HOST': env('VISUALIZATION_DB_HOST'),
        'PORT': env('VISUALIZATION_DB_PORT'),
    },
    DJANGO_SCHEMA_NAME: {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DJANGO_DB_USER'),
        'PASSWORD': env('DJANGO_DB_PASSWROD'),
        'HOST': env('DJANGO_DB_HOST'),
        'PORT': env('DJANGO_DB_PORT'),
        'OPTIONS': {
            'options': f'-c search_path={DJANGO_SCHEMA_NAME}'
        },
    },
    RCCE_PRODUCTION_SCHEMA_NAME: {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('PRODUCTION_DB_USER'),
        'PASSWORD': env('PRODUCTION_DB_PASSWROD'),
        'HOST': env('PRODUCTION_DB_HOST'),
        'PORT': env('PRODUCTION_DB_PORT'),
        'OPTIONS': {
            'options': f'-c search_path={RCCE_PRODUCTION_SCHEMA_NAME}'
        },
    },
}

# Database router this auto detects database based on request
DATABASE_ROUTERS = [
    'config.database_router.DjangoRouter',
    'config.database_router.RcceProductionRouter',
    'config.database_router.RcceVisualizationRouter',
]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

if DEBUG or env('USE_LOCAL_STORATE'):
    STATIC_URL = env('DJANGO_STATIC_URL')
    MEDIA_URL = env('DJANGO_MEDIA_URL')
    STATIC_ROOT = env('DJANGO_STATIC_ROOT')
    MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cors settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'accept-language',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'sentry-trace',
)
CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS')

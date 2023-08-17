"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json

try:
    ZEROFROMLIGHT_DIR = '/var/www/secret'
    ZEROFROMLIGHT_PATH = os.path.join(ZEROFROMLIGHT_DIR, 'secret_key.json')

    with open(ZEROFROMLIGHT_PATH, 'r') as secret_file:
        ZEROFROMLIGHT_KEYS = json.load(secret_file)

except FileNotFoundError:
    ZEROFROMLIGHT_DIR = '/home/kenno/pylist/website/secret'
    ZEROFROMLIGHT_PATH = os.path.join(ZEROFROMLIGHT_DIR, 'secret_key.json')

    with open(ZEROFROMLIGHT_PATH, 'r') as secret_file:
        ZEROFROMLIGHT_KEYS = json.load(secret_file)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'curf2pw&*k&=4p=vwfzu5u&ld(ihs&*f^a4%86f_clhrb2-*of'

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
    'django.forms',
    'django_cleanup',
    'markdownx',
    'blogs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blogs.context.common',
            ],
            'libraries': {
                'mark': 'blogs.templatetags.mark',
            }
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# django-markdownx settings
# テキストに貼り付けた画像のサイズとクオリティ
# アップロードする画像のバイトサイズ
# アップロードする画像の種類

MARKDOWNX_IMAGE_MAX_SIZE = {'size': (800, 500), 'quality': 100}

MARKDOWNX_UPLOAD_MAX_SIZE = 1000 * 1024 # 最大1MBまで可能

MARKDOWNX_UPLOAD_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/gif']

MARKDOWNX_MARKDOWN_EXTENSIONS = [
        'extra',
        'admonition', # 訓戒・忠告
        'sane_lists', # 正常なリスト
        'toc',    # 目次
        'nl2br',  # 改行
]

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
        'toc': {
            'title': '目次',
            'permalink': True
        }
}

# GIF画像ファイルの設定

"""
$ python3 -c "import markdownx; print(markdownx.__path__)" # ソースコードの在り処
$ vim .../markdownx/forms.py
    _SVG_TYPE = 'image/svg+xml'
    _SKIP_PROCESS = ('image/gif', _SVG_TYPE)
    ...
    # if content_type.lower() != self._SVG_TYPE:
    if content_type.lower() not in self._SKIP_PROCESS:
        ...
"""

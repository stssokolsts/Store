# -*- coding: utf-8 -*-
"""
Django settings for Store project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&y+f*upg5ig(o)$srm5!za^n1p!)^(sehtt8gx^bqx&#9y6%@@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.gis',
    'django.contrib.sites',
    'catalog',
    'cart',
    'checkout',
    'djangosphinx',
    'search',
    'caching',
    'utils',
    'django.contrib.flatpages',
    'accounts',
    #'south',
    'social_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'Store.urls'

WSGI_APPLICATION = 'Store.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Store',
        'USER': 'root',
        'PASSWORD': '9CfynfAt9',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

SPHINX_API_VERSION = 0x116
SPHINX_PORT = 9312
SPHINX_SERVER = '127.0.0.1'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_TIMEOUT = 60 * 60

SITE_NAME = 'Вкусный праздник'
META_KEYWORDS = 'Music, instruments, music accessories, musician supplies'
META_DESCRIPTION = 'Modern Musician is an online supplier of instruments'

import django.conf.global_settings as DEFAULT_SETTINGS

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'utils.context_processors.Store',
    'social_auth.context_processors.social_auth_by_name_backends',
)

YANDEX_MAPS_API_KEY = ''

GEOS_LIBRARY_PATH = "Z:\usr\local\python\DLLs\geos_c.dll"

SITE_ID = 1

LOGIN_REDIRECT_URL = '/accounts/my_account/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:8000/accounts/my_account/'


AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailAuthBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.yandex.YandexOAuth2Backend',
    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
)

FACEBOOK_APP_ID = '741873782564323'
FACEBOOK_API_SECRET = 'd2b6c656c5a72d4aebf805d082d36009'


SOCIAL_AUTH_UID_LENGTH = 150
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 150
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 135
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 125


VK_APP_ID = '4672895'
VKONTAKTE_APP_ID = VK_APP_ID
VK_API_SECRET = 'Gz7CVFry1E5winbNc09x'
VKONTAKTE_APP_SECRET = VK_API_SECRET


SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_PIPELINE = (
    # Получает по backend и uid инстансы social_user и user
    'social_auth.backends.pipeline.social.social_auth_user',
    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
    'social_auth.backends.pipeline.associate.associate_by_email',
    # Пытается собрать правильный username, на основе уже имеющихся данных
    'social_auth.backends.pipeline.user.get_username',
    # Создает нового пользователя, если такого еще нет
    'social_auth.backends.pipeline.user.create_user',
    # Пытается связать аккаунты
    'social_auth.backends.pipeline.social.associate_user',
    # Получает и обновляет social_user.extra_data
    'social_auth.backends.pipeline.social.load_extra_data',
    # Обновляет инстанс user дополнительными данными с бекенда
    'social_auth.backends.pipeline.user.update_user_details',
    'accounts.pipeline.get_name',
)


GITHUB_APP_ID = '1e285522c37dfefc907c'
GITHUB_API_SECRET = '51320333c176f0d2cbe1584d52c6e909b82ba7d8'

YANDEX_APP_ID = '615ebb1b22c94b42bdbb65f9579e7f9c'
YANDEX_API_SECRET = 'fc05e7acd7a243958b4b7b23ebba71ea'


ODNOKLASSNIKI_OAUTH2_CLIENT_KEY = '1112708608'
ODNOKLASSNIKI_OAUTH2_APP_KEY = 'CBAHJDFDEBABABABA'
ODNOKLASSNIKI_OAUTH2_CLIENT_SECRET = '0B7557BFE554E0DE9254B0A1'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'stssokolsts@yandex.ru'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'stssokolsts@yandex.ru'
EMAIL_HOST_PASSWORD = 'CfynfAt'
EMAIL_PORT = 25

FROM_EMAIL = 'stssokolsts@yandex.ru'
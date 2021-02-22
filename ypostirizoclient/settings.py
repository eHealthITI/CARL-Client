import os
from .config import cnf

# Basic Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'g2)#&+&eu(b_^q#!llw1^ccmtl7)(7nbvn6@c3@7d1sn#-=j0b'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'fibaro',
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
]
ROOT_URLCONF = 'ypostirizoclient.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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
WSGI_APPLICATION = 'ypostirizoclient.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',

    }
}
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Athens'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
# Project Specific params.
# Change inside .env file
SUBJECT_ID = cnf.SUBJECT_ID
CLOUD_TOKEN = cnf.CLOUD_TOKEN
#  HC_TOKEN = cnf.HC_TOKEN
HC_PASSWORD = cnf.HC_PASSWORD
HC_URL = cnf.HC_URL
HC_USER = cnf.HC_USER
CLOUD_URL = cnf.CLOUD_URL
# CLOUD_USER = cnf.CLOUD_USER
DEBUG = cnf.DEBUG
IGNORED_DEVICES = ["HC_user", "com.fibaro.yrWeather", "com.fibaro.zwavePrimaryController",
                   "com.fibaro.niceEngine", "com.fibaro.zwaveDevice","master"]
HC_API_EVENT_INTERVAL = cnf.HC_INTERVAL
CLOUD_DEVICES_INTERVAL = cnf.CLOUD_DEVICES_INTERVAL
CLOUD_EVENTS_INTERVAL = cnf.CLOUD_EVENTS_INTERVAL
TYPE_OF_CHOICES = {
                   'com.fibaro.FGMS001': 2,
                   'com.fibaro.multilevelSensor': 2,
                   'com.fibaro.sensor': 2,
                   'com.fibaro.doorWindowSensor': 3,
                   'com.fibaro.lifeDangerSensor': 3,
                   'com.fibaro.floodSensor': 4,
                   'com.fibaro.remoteSceneController': 5
                   }


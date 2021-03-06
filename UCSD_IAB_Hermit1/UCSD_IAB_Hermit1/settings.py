"""
Django settings for UCSD_IAB_Hermit1 project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c$@ydho2yxs-!mqmcko=s^8gng)tj2@e@!6=*k!q-gbu1xp#aa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ '127.0.0.1', 'crybed2017.pythonanywhere.com' ]


### UCSD IAB Hermit1 System ###

UCSD_IAB_DB_DIR = os.path.join(BASE_DIR, "UCSD_IAB_DB")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# Caution: This often appears at the end of configuration file.

STATIC_URL = '/UCSD_IAB_Static/'

# STATIC_ROOT = os.path.join(BASE_DIR, "UCSD_IAB_Static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "UCSD_IAB_Static"), # "S" upper case
]

UCSD_IAB_WORKDIR = os.path.join(BASE_DIR, "UCSD_IAB_Workspace")

# https://docs.djangoproject.com/en/1.9/howto/static-files/
# http://www.bogotobogo.com/python/Django/Python_Django_Image_Files_Uploading_Example.php
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home2/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(UCSD_IAB_WORKDIR, 'Media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/UCSD_IAB_media/' # <-- Configure httpd.conf!!


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
TIME_ZONE_THISSERVER = "Asia/Tokyo" # 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "AccAuth_TZ", # UCSD IAB Hermit1 System #
    "appNichoAnu", # UCSD IAB Hermit1 System #
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

ROOT_URLCONF = 'UCSD_IAB_Hermit1.urls'

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

WSGI_APPLICATION = 'UCSD_IAB_Hermit1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(UCSD_IAB_DB_DIR, 'db.sqlite3'), # UCSD IAB Hermit1 System #
    },

    "nichoanu": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(UCSD_IAB_DB_DIR, 'db_nichoanu.sqlite3'), # UCSD IAB Hermit1 System #
    },

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









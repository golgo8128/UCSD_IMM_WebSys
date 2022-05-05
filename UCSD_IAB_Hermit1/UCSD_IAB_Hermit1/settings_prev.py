"""
Django settings for UCSD_IMM_hermit1 project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


""" UCSD IMM System-specific settings """
# Notice:
# You must install https://github.com/ottoyiu/django-cors-headers
# The folder or file name "Media" should not appear more than once in a path.

APACHE_USERNAME = "apache" # This is intended for CentOS.

# UCSD IMM System URL path

import getpass

if getpass.getuser() == APACHE_USERNAME:
    UCSD_IMM_URL_PATH = "/HERMIT1"
    DEBUG = False
    ALLOWED_HOSTS = ['*']   
else:
    UCSD_IMM_URL_PATH = ""
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = []   

 

RS_HOME = {
    "darwin" : os.path.join(os.sep, "Users", "rsaito"),
    "linux"  : os.path.join(os.sep, "home", "rsaito"),
    "win32"  : os.path.join(os.sep, "Users", "Rin"),
           }[ sys.platform ]

# os.environ["RS_CONFIG_DIR"]   = os.path.join(RS_HOME, "Work", "Config")
os.environ["RS_DESKTOP_DIR"]  = os.path.join(RS_HOME, "Desktop")
os.environ["RS_INTERMED_DIR"] = os.path.join(RS_HOME, "Work", "InterMed")
os.environ["RS_LOG_DIR"]      = os.path.join(RS_HOME, "Work", "Log")
os.environ["RS_PROG_DIR"]     = os.path.join(RS_HOME, "rs_Progs")
os.environ["RS_PROJ_DIR"]     = os.path.join(RS_HOME, "Work", "Project")
os.environ["RS_PUBDATA_DIR"]  = os.path.join(RS_HOME, "PubData")
os.environ["RS_TMP_DIR"]      = os.path.join(RS_HOME, "Desktop", "TMPArea")
os.environ["RS_TRUNK_DIR"]    = os.path.join(RS_HOME, "Documents", "WORK_trunk2_4")

for ipath in [ os.path.join(os.environ["RS_PROG_DIR"],
                            ipath_sub)
               for ipath_sub in (os.path.join("rs_Python"),
                                 os.path.join("rs_Python",
                                              "rs_Python_Pack3"),
                                 os.path.join("rs_Python",
                                              "rs_Python_Pack3",
                                              "General_Packages"),) ]:
    if ipath not in sys.path:
        sys.path.insert(1, ipath) # Insert as a second element.


# UCSD IMM database folder

UCSD_IMM_DB = "UCSD_IMM_DB"
    
# UCSD IMM System Authentication

LOGIN_URL = UCSD_IMM_URL_PATH + "/login/"

# UCSD IMM System-specific. Variable name must be capital letters.

UCSD_IMM_WORKDIR = os.path.join(BASE_DIR, "UCSD_IMM_WorkSpace")


# UCSD IMM System-specific. Variable name must be capital letters.
UCSD_IMM_INFOTRANSFDIR = os.path.join(UCSD_IMM_WORKDIR, "InfoTransf")

# UCSD IMM System-specific. Variable name must be capital letters.

UCSD_IMM_LOGDIR = os.path.join(BASE_DIR, "UCSD_IMM_Log")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# Caution: This often appears at the end of configuration file.

STATIC_URL = "/UCSD_IMM_static/" # "s" lower case

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "UCSD_IMM_Static"), # "S" upper case
]

# https://docs.djangoproject.com/en/1.9/howto/static-files/
# http://www.bogotobogo.com/python/Django/Python_Django_Image_Files_Uploading_Example.php
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home2/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(UCSD_IMM_WORKDIR, 'Media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/UCSD_IMM_media/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+_(^ztw9o8#qu#ls+ktrpg2nty*x40ojtu9jb_u=&&@o-lrijm'




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders', # https://github.com/ottoyiu/django-cors-headers
    "AccAuth_TZ",           # UCSD IMM System
    "appWorkChunkPlanner2", # UCSD IMM System
    'appNichoAnu', # UCSD IMM System
    "appPubMedler", # UCSD IMM System
    "appTest1",    # UCSD IMM System
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', # https://github.com/ottoyiu/django-cors-headers
    'django.middleware.common.CommonMiddleware', # https://github.com/ottoyiu/django-cors-headers
]

ROOT_URLCONF = 'UCSD_IMM_hermit1.urls'

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
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = 'UCSD_IMM_hermit1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, UCSD_IMM_DB, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
TIME_ZONE_THISSERVER = "US/Pacific"

USE_I18N = True

USE_L10N = True

USE_TZ = True
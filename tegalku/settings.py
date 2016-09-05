"""
Django settings for tegalku project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from __future__ import unicode_literals
import os
import sys
import djcelery  

# Used to
sys.path.insert(0, '../../django-hitcount')  # our hitcount app

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_k9)2t+-+=i!_y=rz0cj*w+0v!-=)4=xcot2)(w*g(=izrw28v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move'
}

ALLOWED_HOSTS = []
DATABASE_ROUTERS = ['webku.routers.MyApp2Router',]


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'bootstrap_themes',
	'easy_thumbnails',
	'filer',
	'mptt',
	'django_windows_tools',
	'embed_video',
	'hitcount',
	'contact_form',
	'ckeditor',
	'ckeditor_uploader',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'checkboxselectmultiple',
	'kombu.transport.django',	
	'djcelery',
	'django.contrib.gis',
	'dynamic_scraper',
	'geoposition',
	'pure_pagination',
	'disqus',
	'mathfilters',
	'liststyle',
	'django_social_share',
	'django_object_actions',
	'webku',
	
]

DISQUS_API_KEY = 'JRv4Yp9DIBGuaLISP5pg1aolRPg0c41nW8nBMAtA8R7h9ppPAcSZ5XDPT3Dl5AQF'
DISQUS_WEBSITE_SHORTNAME = 'seputartegal'
 
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyBf0YLXA-IfVivhr_NwvvlFGora1gzVmJ8'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DOWNLOAD_HANDLERS = {
    'http': 'scraper.handlers.PhantomJSDownloadHandler',
    'https': 'scraper.handlers.PhantomJSDownloadHandler',
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# django-celery settings
import djcelery
djcelery.setup_loader()

# Broker configuration
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_BACKEND = "django"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Celery Redis configuration
CELERY_SEND_EVENTS=True
CELERY_RESULT_BACKEND='redis'
CELERY_REDIS_HOST='127.0.0.1'
CELERY_REDIS_PORT=6379
CELERY_REDIS_DB = 0
CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER=False


DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

ROOT_URLCONF = 'tegalku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'tegalku.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': 'webku',
		'USER': 'root',
		'PASSWORD':'',
		'HOST':'',
		'PORT':'',
		'OPTIONS': {
          'autocommit': True,
		 },
    },
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

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
 os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
MEDIA_URL = '/media/'
FILER_CANONICAL_URL = 'media/'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
FILER_CANONICAL_URL = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': (
            ['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
            ['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
        ),
    }
}

HITCOUNT_KEEP_HIT_ACTIVE = {'minutes': 60}
HITCOUNT_HITS_PER_IP_LIMIT = 0  # unlimited
HITCOUNT_EXCLUDE_USER_GROUP = ()  # not used
HITCOUNT_KEEP_HIT_IN_DATABASE = {'seconds': 10}

EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'alimcorporations@gmail.com'
EMAIL_HOST_PASSWORD = 'alim0494'
EMAIL_USE_TLS       = True
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
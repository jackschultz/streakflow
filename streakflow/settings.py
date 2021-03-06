# Django settings for streakflow project.
import os
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jack Schultz', 'jackschultz23@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'streakflow',                      # Or path to database file if using sqlite3.
        'USER': 'streakflow_user',
        'PASSWORD': 'somethingeasytoremember',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

##For regsitration here...
ACCOUNT_ACTIVATION_DAYS = 3 #three days for activation
REGISTRATION_OPEN=True
#change so not accounts/profile, but rather have reverse or something
LOGIN_REDIRECT_URL = '/profile/'
#the actual smtp backend. Need to get the domain figured out
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'register@streakflow.com'
EMAIL_HOST_PASSWORD = 'streakflowishere'
EMAIL_PORT = 587

#celery info. Need for sending emails and all that if nothign else
import djcelery
djcelery.setup_loader()

BROKER_URL = "amqp://guest:guest@localhost:5672//"

CELERY_IMPORTS = ('streakflow.apps.members.tasks',)
CELERY_TIMEZONE = 'UTC'

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'check-goals-complete': {
        'task': 'streakflow.apps.members.tasks.reminder_emails',
        'schedule': crontab(minute='*/30'),
    },
}

MANDRILL_API_KEY = 'FdYZou0jtJNao2sQTU1O_Q'

#recaptcha
RECAPTCHA_PUBLIC_KEY = '6LdzZOYSAAAAAMh-cWjEzrQvN-yATIP_W4H5izWl'
RECAPTCHA_PRIVATE_KEY = '6LdzZOYSAAAAALxBx018FLZFxJ6G0oDjPl_MWH5Y'


#for the framework
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
  ),
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
  ),
#  'DEFAULT_RENDERER_CLASSES': (
#    'rest_framework.renderers.JSONRenderer',
#    'rest_framework.renderers.BrowsableAPIRenderer',
#  ),
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


INTERNAL_IPS = ('127.0.0.1',)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_PATH + '/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/jackschultz/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + '/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'krw_%9l)j9#z#y5*&zpm@wf=-(f1z3at2d^65dz@!=tk4n8ap3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'streakflow.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'streakflow.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + '/templates',
)

AUTH_PROFILE_MODULE = 'members.Member'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'djcelery',
    'mailsnake',
    'captcha',
    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'south',
    'streakflow.apps.members',
    'streakflow.apps.goals',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

try:
  from local_settings import *
except ImportError:
  print "FASDSADFFDSAADFSDAFSFADSDAFSFADS"

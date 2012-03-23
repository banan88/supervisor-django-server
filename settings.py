import django.conf.global_settings as DEFAULT_SETTINGS
import os
import getpass

user = getpass.getuser()
DIRNAME = os.path.dirname(__file__)


import socket
PRODUCTION = (socket.getfqdn(socket.gethostname()) == 'http7.alwaysdata.com') #check for production env

if PRODUCTION:
    ADMINS = (
    ('mateusz banaszkiewicz', 'mat.banaszkiewicz@gmail.com'),
    )
else:
    ADMINS = (
    ('test/test', 'your_email@example.com'),
)

if PRODUCTION:
    ADMIN_MEDIA_PREFIX = '/media/'
else:
    ADMIN_MEDIA_PREFIX = '/static/admin/'

DEBUG = not PRODUCTION

if PRODUCTION:
    TEMPLATE_DEBUG = DEBUG
else:
    TEMPLATE_DEBUG = False

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(DIRNAME, 'sqlite/database.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'PL'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/supervisor-django-server/public/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = ('/static/')

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
if PRODUCTION:
    ADMIN_MEDIA_PREFIX = '/media/'
else:
    ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files

STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/
# Always use forward slashes, even on 
# Don't forget to use absolute paths, not relative paths.
os.path.join(DIRNAME,'static'),
    )


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n8(lono$*h8z*hqygd=n6t=@huf)b%92r4dav*7143axd0qyl2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS +(
  'django.core.context_processors.request',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'supervisor-django-server.main_app.api.CustomHeaderMiddleware', #mobile client header - request.META[autorization] visibility
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'supervisor-django-server.urls'

TEMPLATE_DIRS = (
    os.path.join(DIRNAME,'templates'),
    os.path.join(DIRNAME,'templates/ajax'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'supervisor-django-server.main_app',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

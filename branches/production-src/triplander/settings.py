import os.path
# Django settings for Flyopia project.
DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('aromano', 'info@triplander.com'),
)

MANAGERS = ADMINS

#CACHE_BACKEND = 'db://triplander_cachetable'
CACHE_BACKEND = 'memcached://127.0.0.1:8006/'

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'aromano_django'             # Or path to database file if using sqlite3.
DATABASE_USER = 'aromano_django'             # Not used with sqlite3.
DATABASE_PASSWORD = 'acchianat1'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# devapp ids/api keys for external services (e.g., Google Maps, Yahoo! Travel...)
YAHOO_DEVAPP_ID = "PCVFIjzIkY00STGdzLZWYnV7bkWrH5LUzIwJrQ--"
GOOGLEMAPS_APIKEY = "ABQIAAAA8YuyHu68hQTivoDIZS1VChScCbIvVPg0be-YWXpRP9_p6iZLsxRsgDaxlzs3Au0eV0ke7pHaGZJgrg"
GOOGLE_MAPS_API_KEY = GOOGLEMAPS_APIKEY

USER_HOME = DEFAULT_PATH
# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'it'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(USER_HOME+'/dontknow')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ayxi8#n4qj-#g41jt#r^2)9gek3g9z*_6-hprkec(65wijz&u@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.http.SetRemoteAddrFromForwardedFor',
    'triplander.middleware.Activity',
)

ROOT_URLCONF = 'triplander.urls'

TEMPLATE_DIRS = [
    USER_HOME+'/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.admin',
    'triplander'
)

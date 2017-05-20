# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join, normpath, isfile

import environ

SITE_ROOT = dirname(dirname(abspath(__file__)))

env = environ.Env()
env_file = join(dirname(SITE_ROOT), '.env')
if isfile(env_file):
    environ.Env.read_env(env_file=env_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "b=r$iq#q5wh@7vicmcp5neg=7#3*4(cb^j-kjz)_8vbusy+db&"


# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
DEBUG = env("DJANGO_DEBUG", cast=bool, default=False)
VERBOSE = env("DJANGO_VERBOSE", cast=bool, default=False)


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = False

USE_L10N = True

USE_TZ = False


# Application definition
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'oauth2_provider',  # for oauth2 server
    'rest_framework',  # for build RESTFull API
    'rest_framework_swagger',  # django-rest-swagger
)
LOCAL_APPS = (
    # Apps specific for this project go here.
    'zipcode_jp',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(SITE_ROOT, 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# AUTHENTICATION
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)


# django-rest-framework
REST_FRAMEWORK = {
    # TODO デバッグ中につきコメントアウト。アルファ版リリースまでに戻す。
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    # 'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    # ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        # 'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}


# django-oauth-toolkit
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}


# Django REST Swagger
SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    # "api_version": '0.1',  # Specify your API's version
    # "api_path": "/",  # Specify the path to your API not a root level
    # Specify which methods to enable in Swagger UI
    "enabled_methods": [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "is_authenticated": False
}


# CACHING
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': env.cache('DJANGO_CACHES_DEFAULT_URL', 'locmemcache://'),
}


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db(default='sqlite:////tmp/db.sqlite'),
}


# e-mail
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST =  env("DJANGO_EMAIL_HOST", default="")
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env("DJANGO_EMAIL_PORT", cast=int, default="")
EMAIL_USE_TLS = env("DJANGO_EMAIL_USE_TLS", cast=bool, default=False)


# SESSIONS
# https://docs.djangoproject.com/en/dev/topics/http/sessions/
SESSION_ENGINE = env('DJANGO_SESSION_ENGINE', default='django.contrib.sessions.backends.db')


# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_URL = '/media/'
MEDIA_ROOT = env('DJANGO_MEDIA_ROOT', default=normpath(join(SITE_ROOT, 'media')))


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = env('DJANGO_STATIC_ROOT', default=normpath(join(dirname(SITE_ROOT), 'staticfiles')))

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Host
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]


# django-debug-toolbar
if DEBUG and env("DJANGO_SHOW_DEBUG_TOOLBAR", cast=bool, default=True):
    LOCALHOST_IP = '127.0.0.1'
    VAGRANT_NAT_IP = '172.16.66.1'
    INTERNAL_IPS = (LOCALHOST_IP, VAGRANT_NAT_IP,)
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }


# Logging
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO' if DEBUG is False else 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'level': 'WARNING' if DEBUG is False else 'DEBUG',
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'ERROR' if VERBOSE is False else 'DEBUG',
            'handlers': ['console'],
        },
        'app': {
            'level': 'INFO' if DEBUG is False else 'DEBUG',
            'handlers': ['console'],
        },
    }
}

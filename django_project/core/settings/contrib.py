# coding=utf-8
"""
core.settings.contrib
"""
import ast
from core.settings.utils import ensure_unique_app_labels
from .base import *  # noqa
# Override base settings from geonode
from core.settings.geonode_generic import *  # noqa
import os
import raven
try:
    from .secret import IUCN_API_KEY  # noqa
except ImportError:
    IUCN_API_KEY = ''


STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that', 'to',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

# Django-allauth related settings
AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Django grappelli need to be added before django.contrib.admin
# INSTALLED_APPS = (
#     'grappelli',
# ) + INSTALLED_APPS

# Grapelli settings
GRAPPELLI_ADMIN_TITLE = 'IGRAC Admin Page'

INSTALLED_APPS += (
    # AppConfig Hook to fix issue from geonode
    'core.config_hook',
    'allauth',
    'allauth.account',
    # 'rolepermissions',
    'rest_framework',
    'celery',
    'pipeline',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'wagtailmenus',

)

if os.environ.get('RAVEN_CONFIG_DSN'):
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    RAVEN_CONFIG = {
        'dsn': os.environ.get('RAVEN_CONFIG_DSN'),
    }
    if os.environ.get('GIT_PATH'):
        RAVEN_CONFIG['release'] = (
            raven.fetch_git_sha(os.environ.get('GIT_PATH'))
        )

# workaround to get flatpages picked up in installed apps.
INSTALLED_APPS += (
    'django.contrib.sites',
)

# Set templates
try:
    TEMPLATES[0]['DIRS'] = [
        absolute_path('core', 'base_templates'),
    ] + TEMPLATES[0]['DIRS']
except (KeyError, NameError):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # project level templates
                absolute_path('core', 'base_templates'),
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',

                    # `allauth` needs this from django
                    'django.template.context_processors.request',
                ],
            },
        },
    ]

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    # IGRAC context processor
    'igrac.context_processors.resource_urls',

    # WAGTAIL
    'wagtail.contrib.settings.context_processors.settings',
    'wagtailmenus.context_processors.wagtailmenus',
]

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/web/static'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    absolute_path('core', 'base_static'),
] + STATICFILES_DIRS

TESTING = sys.argv[1:2] == ['test']

MIDDLEWARE += (
    # Wagtail middleware
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)
# if not TESTING and not on_travis:
    # INSTALLED_APPS += (
    #     'easyaudit',
    # )
    # MIDDLEWARE += (
    #     'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    # )
# for middleware in MIDDLEWARE_CLASSES:
#     if middleware not in MIDDLEWARE:
#         MIDDLEWARE += (middleware,)

# Defines whether to log model related events,
# such as when an object is created, updated, or deleted
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True

# Defines whether to log user authentication events,
# such as logins, logouts and failed logins.
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True

# Defines whether to log URL requests made to the project
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user:email', 'public_repo', 'read:org']
    }
}

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
LOGIN_REDIRECT_URL = "/"

AUTH_WITH_EMAIL_ONLY = ast.literal_eval(os.environ.get(
        'AUTH_WITH_EMAIL_ONLY', 'False'))

if AUTH_WITH_EMAIL_ONLY:
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_FORMS = {}
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
else:
    INSTALLED_APPS += (
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.github',
    )


INSTALLED_APPS = ensure_unique_app_labels(INSTALLED_APPS)
# ROLEPERMISSIONS_MODULE = 'roles.settings.roles'

IUCN_API_URL = 'http://apiv3.iucnredlist.org/api/v3'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

MODELSDOC_OUTPUT_FORMAT = 'rst'
MODELSDOC_MODEL_WRAPPER = 'modelsdoc.wrappers.ModelWrapper'
MODELSDOC_FIELD_WRAPPER = 'modelsdoc.wrappers.FieldWrapper'
MODELSDOC_INCLUDE_AUTO_CREATED = True

# contact us email
SERVER_EMAIL = os.environ.get('ADMIN_EMAILS', 'admin@kartoza.com')
CONTACT_US_EMAIL = os.environ.get('CONTACT_US_EMAIL', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', CONTACT_US_EMAIL)

# site tracking stats settings
TRACK_PAGEVIEWS = True
TRACK_AJAX_REQUESTS = False
TRACK_REFERER = True
TRACK_IGNORE_STATUS_CODES = [301, 303, 403, 404, 405, 410]

DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = [
    'layers.Layer',
    'people.Profile',
]

if MONITORING_ENABLED:
    DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA += [
        'monitoring.RequestEvent',
        'monitoring.MonitoredResource',
    ]

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'celery.log',
            'formatter': 'simple',
            'maxBytes': 1024 * 1024 * 10,  # 10 mb
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "INFO", },
        "geonode.qgis_server": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "gsconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
        "celery": {
            'handlers': ['celery', 'console'], 'level': 'DEBUG', },
    },
}

ACCOUNT_APPROVAL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = True
# ACCOUNT_ADAPTER = ''
ACCOUNT_EMAIL_VERIFICATION = 'none'

OGC_SERVER['default']['DATASTORE'] = os.environ.get(
        'DEFAULT_BACKEND_DATASTORE', '')

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS':
#         'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 100
# }

# Wagtail Settings
WAGTAIL_SITE_NAME = 'My Example Site'
WAGTAILMENUS_SITE_SPECIFIC_TEMPLATE_DIRS = True
# -- END Settings for Wagtail

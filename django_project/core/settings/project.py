# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from django.utils.translation import ugettext_lazy as _
from .contrib import *  # noqa

# Project apps
INSTALLED_APPS += (
    'igrac',
)

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
)

VALID_DOMAIN = [
    '0.0.0.0',
]

PIPELINE = {
    'STYLESHEETS': {
        'project': {
            'source_filenames': {
                'js/libs/bootstrap-4.0.0/css/bootstrap.min.css',
                'js/libs/font-awesome/css/font-awesome.min.css',
                'js/libs/magnific-popup/magnific-popup.css',
                'js/libs/openlayers-4.6.4/ol.css',
                'js/libs/jquery-ui-1.12.1/jquery-ui.min.css',
                'css/base.css',
                'css/default.css'
            },
            'output_filename': 'css/project.css',
            'extra_content': {
                'media': 'screen, projection',
            }
        }
    },
}

TEMP_FOLDER = MEDIA_ROOT + '/temp'

# Geometry used for others
# Turn off if it is not used (like showing on map)
# If it is not used, geometry that saved is just municipals
# Because of calculating cluster is just for municipals
USE_GEOMETRY_BOUNDARY = False

# Additional locations of static files
STATICFILES_DIRS = [
    absolute_path('igrac', 'static'),
] + STATICFILES_DIRS

# Additional locations of templates
TEMPLATES[0]['DIRS'] = [
    absolute_path('igrac', 'templates')
] + TEMPLATES[0]['DIRS']

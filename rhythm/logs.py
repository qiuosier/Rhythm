import os
from google.cloud import logging
client = logging.Client()
client.setup_logging()


RHYTHM_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'Aries': {
            '()': 'Aries.outputs.MessageFormatter',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'project_packages': {
            '()': 'Aries.outputs.PackageLogFilter',
            'folder_path': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true', 'project_packages'],
            'class': 'logging.StreamHandler',
            'formatter': 'Aries'
        },
        'stackdriver': {
            'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
            'client': client
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'] if os.getenv('GAE_RUNTIME', '') != "python37" else ['stackdriver'],
            'level': 'INFO' if os.getenv('GAE_RUNTIME', '') else 'DEBUG',
            'propagate': True,
            'name': 'Django:Rhythm'
        },
    },
}
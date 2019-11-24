import os
import sys
import socket


LOG_HANDLERS = {
    'console': {
        'level': 'DEBUG',
        'filters': ['require_debug_true', 'project_packages'],
        'class': 'logging.StreamHandler',
        'formatter': 'Aries'
    }
}
HANDLER_NAMES = ['console']
LOGGING_LEVEL = 'DEBUG'


# Stackdriver logging will NOT be enabled if
#   There is a file called "DEBUG" in the project root, or
#   The website is running by using the runserver command.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(BASE_DIR, "DEBUG")) and not 'runserver' in sys.argv:
    from google.cloud import logging
    client = logging.Client()
    client.setup_logging()
    LOG_HANDLERS['stackdriver'] = {
        'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
        'client': client,
        'name': socket.gethostname()
    }
    HANDLER_NAMES = ['stackdriver']
    LOGGING_LEVEL = 'DEBUG'


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
            'package_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        },
    },
    'handlers': LOG_HANDLERS,
    'loggers': {
        '': {
            'handlers': HANDLER_NAMES,
            'level': LOGGING_LEVEL,
            'propagate': True,
            'name': 'Django:Rhythm'
        },
    },
}

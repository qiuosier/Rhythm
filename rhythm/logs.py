import os


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


if os.getenv('GAE_RUNTIME', '') == "python37":
    from google.cloud import logging
    client = logging.Client()
    client.setup_logging()
    LOG_HANDLERS['stackdriver'] = {
        'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
        'client': client
    }
    HANDLER_NAMES = ['stackdriver']
    LOGGING_LEVEL = 'INFO'


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

import os


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
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
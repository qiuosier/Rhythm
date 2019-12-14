import os
import sys
import socket
from Aries.outputs import LoggingConfigDict


LOGGING_LEVEL = 'DEBUG'
config_dict = LoggingConfigDict().add_logger("", LOGGING_LEVEL)

# Stackdriver logging will NOT be enabled if
#   There is a file called "DEBUG" in the project root, or
#   The website is running by using the runserver command.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if True: # not os.path.exists(os.path.join(BASE_DIR, "DEBUG")) and not 'runserver' in sys.argv:
    logger_name = socket.gethostname()
    # Check if the website is running in Google App Engine
    if os.getenv('GAE_RUNTIME', '') == "python37":
        logger_name = 'AppEngine'

    from google.cloud import logging
    client = logging.Client()
    client.setup_logging()
    stackdriver_handler = {
        'handler_class': 'Aries.gcp.logging.StackdriverHandler',
        'filters': ['project_packages'],
        'client': client,
        'name': logger_name,
        'handler_name': "stackdriver"
    }
    print("Using Stackdriver logging...")
    config_dict.add_handler(**stackdriver_handler)
else:
    config_dict.add_handler(
        handler_name='console',
        handler_class="Aries.outputs.StreamHandler"
    )


config_dict.add_filters({
    'project_packages': {
        '()': 'Aries.outputs.PackageLogFilter',
        'package_root': os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    },
})

RHYTHM_CONFIG = config_dict.get_config()

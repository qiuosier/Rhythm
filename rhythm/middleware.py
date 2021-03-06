import traceback
import logging
import json
import socket
import os
from collections import OrderedDict
from django.utils import timezone
from django.contrib.auth import login, logout
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from google.cloud import error_reporting
logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Gets the IP address of the request client.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class StackdriverRequestLoggingMiddleware(MiddlewareMixin):
    """
    Logs the http request activities to database.

    The most data, including GET request data is saved before the view is processed (in process_request).
    However, the POST request data is saved after the view is processed (in process_response).
    See https://docs.djangoproject.com/en/1.10/topics/http/middleware/#process-view for more details.

    Remarks:
        __init__() is called only once, when the Web server starts.
        The attributes added to a middleware instance are preserved across multiple request/response.
        In Django 1.10+, __call__() method is called once per request.
        Before Django 1.10,  __call__() method is not used.
    """

    def __process_response(self, request, response=None):
        # Ignore static file requests
        if request.path.startswith('/static/') or request.path.startswith('/favicon.ico'):
            return
        try:
            files = request.FILES.dict()
            file_data = {}
            for key in files:
                file_data[key] = str(files[key])
        except Exception as ex:
            file_data = {type(ex).__name__: str(ex)}

        record = OrderedDict()
        record["Method"] = request.method
        record["Path"] = request.path
        record["IP"] = get_client_ip(request)
        record["GET"] = json.dumps({k: v if len(v) > 1 else v[0] for k, v in request.GET.lists()})
        record["POST"] = json.dumps({k: v if len(v) > 1 else v[0] for k, v in request.POST.lists()})
        record["FILES"] = file_data,
        record["Code"] = response.status_code if response else "500"
 
        logger.info(record)
        return

    def process_response(self, request, response):
        """Saves the request and response data, if available.
        """
        self.__process_response(request, response)
        return response

    def process_exception(self, request, exception):
        """Saves the exception data.

        Remarks:
        Any request without a activity_record attribute will be skipped.
        """
        # Send error to Stackdriver error reporting when DEBUG is false.
        if not settings.DEBUG:
            logger.debug("Sending exception to GCP error reporting...")
            client = error_reporting.Client(service=socket.gethostname())
            client.report_exception(error_reporting.HTTPContext(
                url=request.get_raw_uri(),
                method=request.method,
                user_agent=request.headers.get("User-Agent"),
                referrer=request.headers.get("Referer"),
                response_status_code=500,
                remote_ip=get_client_ip(request),
            ))

        # self.__process_response(request)
        logger.critical("Exception: %s: %s\n%s" % (
            type(exception), 
            str(exception), 
            traceback.format_exc
        ))

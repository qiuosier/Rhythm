import traceback
import logging
import json
from collections import OrderedDict
from django.utils import timezone
from django.contrib.auth import login, logout
from django.utils.deprecation import MiddlewareMixin
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

    The activity_record attribute added the request in the process_request method indicates that
        the request is processed by this middleware.
    The process_response method will skip the processing if activity_record is not found in the request.

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
        self.__process_response(request)
        logger.error("Exception: %s: %s\n%s" % (
            type(exception), 
            str(exception), 
            traceback.format_exc
        ))

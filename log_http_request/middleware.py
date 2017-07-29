"""
This is
"""
import json
from google.appengine.ext import ndb


class UserActivity(ndb.Model):
    url = ndb.StringProperty()
    method = ndb.StringProperty()
    ip = ndb.StringProperty()
    response_code = ndb.IntegerProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)


class IPAddress(ndb.Model):
    ip = ndb.StringProperty()
    country = ndb.StringProperty()
    region = ndb.StringProperty()
    city = ndb.StringProperty()
    isp = ndb.StringProperty()
    org = ndb.StringProperty()
    asn = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now=True)


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


class LogHttpRequestMiddleware(object):
    """
    Logs the http request activities to database.

    This middleware uses the UserActivity model to save the user activities into the database.

    This middleware is compatible with both MIDDLEWARE (Django 1.10) and MIDDLEWARE_CLASS (pre Django 1.10).
    See https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware

    The most data, including GET request data is saved before the view is processed (in process_request).
    However, the POST request data is saved after the view is processed (in process_response).
    See https://docs.djangoproject.com/en/1.10/topics/http/middleware/#process-view for more details.

    The activity_record attribute added the request in the process_request method indicates that
        the request is processed by this middleware.
    The process_response method will skip the processing if activity_record is not found in the request.
    """

    def __init__(self, get_response=None):
        """Initializes the middleware.

        Remarks:
        __init__() is called only once, when the Web server starts.
        The attributes added to a middleware instance are preserved across multiple request/response.
        """
        # This is required after Django 1.10
        self.get_response = get_response

    def __call__(self, request):
        """
        Remarks:
        In Django 1.10+, __call__() method is called once per request.
        Before Django 1.10,  __call__() method is not used.
        """
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        """Creates a user activity record in the database.

        Remarks:
        The full name of the user is recorded if the user is authenticated.
        Otherwise, "Anonymous" is used.
        An activity_record attribute is added to the request to store an UserActivity instance.

        """
        # Ignore static and media requests
        if request.path.startswith('/static/') or request.path.startswith('/favicon.ico'):
            return

        record = UserActivity()
        record.url = request.path
        record.method = request.method
        record.ip = get_client_ip(request)
        request.activity_record = record
        # record.put()

    def process_response(self, request, response):
        """Saves the response status code and POST request data.

        Remarks:
        Any request without a activity_record attribute will be skipped.
        """
        if not hasattr(request, 'activity_record'):
            return response
        record = request.activity_record
        if record:
            record.response_code = response.status_code
            record.put()
        return response

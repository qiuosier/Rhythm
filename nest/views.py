from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from google.appengine.api import urlfetch
from django.conf import settings
import os
import json


def index(request):
    return load_data_and_render(request, "index")


def load_data_and_render(request, name):
    """Loads data from a JSON file and renders a template.
    The JSON file and HTML template should have the same filename (different extensions, json and html).
    JSON files are stored in the "nest/data" folder.
    Data will be empty if JSON file does not exist.

    Args:
        request: HTTP request.
        name: Filename without extension.

    Returns: HTTP Response.

    """
    json_file = os.path.join(settings.BASE_DIR, "nest", "data", name + ".json")
    if os.path.exists(json_file):
        with open(json_file) as f:
            data = json.load(f)
    else:
        data = {}
    return render(request, "nest/" + name + ".html", data)


def activate(request):
    try:
        r = urlfetch.fetch('http://qiu.azurewebsites.net', method='GET', deadline=20)
        if r.status_code == 200:
            return HttpResponse("Nest activated successfully.")
        else:
            return HttpResponseBadRequest("Status Code: " + str(r.status_code))
    except Exception as ex:
        return HttpResponse("Exception.")

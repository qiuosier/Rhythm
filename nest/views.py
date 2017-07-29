from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from google.appengine.api import urlfetch
from django.conf import settings
import os
import json
import markdown


def index(request):
    return load_data_and_render(request, "index")


def load_json(file_name):
    """Loads data from a JSON file to a Python dictionary
    JSON files are stored in the "/data" folder.
    Data will be empty if JSON file does not exist.

    Args:
        file_name: Filename without extension.

    """
    json_file = os.path.join(settings.BASE_DIR, "data", file_name + ".json")
    if os.path.exists(json_file):
        with open(json_file) as f:
            data = json.load(f)
    else:
        print("File Not Found.")
        data = {}
    return data


def load_data_and_render(request, file_name):
    """Loads data from a JSON file and renders a template.
    The JSON file and HTML template should have the same filename (different extensions, json and html).
    JSON files are stored in the "/data" folder.
    HTML files are stored in the "nest" template folder.

    Args:
        request: HTTP request.
        file_name: Filename without extension.

    Returns: HTTP Response.

    """
    html_file = "nest/" + file_name + ".html"
    try:
        get_template(html_file)
    except TemplateDoesNotExist:
        message = "Template \"%s\" does not exist." % html_file
        return HttpResponseNotFound(message)
    return render(request, html_file, load_json(file_name))


def page(request, file_name):
    """Loads data from a markdown file and renders it in the "page" template.
    Markdown files are stored in the "static/data" folder.

    Args:
        request: HTTP request.
        file_name: Filename without extension.

    Returns: HTTP Response.

    """
    input_file = os.path.join(settings.BASE_DIR, "data", "markdown", file_name + ".md")
    if os.path.exists(input_file):
        with open(input_file) as f:
            text = f.read()
    else:
        return HttpResponseNotFound(file_name + " not found.")
    html_content = markdown.markdown(
        text,
        output_format="html5",
    )
    return render(request, "nest/page.html", {"html_content": html_content})


def activate(request):
    try:
        r = urlfetch.fetch('http://qiu.azurewebsites.net', method='GET', deadline=20)
        if r.status_code == 200:
            return HttpResponse("Nest activated successfully.")
        else:
            return HttpResponseBadRequest("Status Code: " + str(r.status_code))
    except Exception as ex:
        return HttpResponse("Exception.")

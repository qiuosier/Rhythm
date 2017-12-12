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


def skylark_collection(request, collection):
    data = load_json("skylark/" + collection)
    return render(request, "nest/skylark_collection.html", data)


def load_json(filename):
    """Loads data from a JSON file to a Python dictionary
    JSON files are stored in the "/data" folder.
    Data will be empty if JSON file does not exist.

    Args:
        filename: Filename without extension.

    """
    json_file = os.path.join(settings.BASE_DIR, "data", filename + ".json")
    if os.path.exists(json_file):
        with open(json_file) as f:
            data = json.load(f)
    else:
        print("File Not Found.")
        data = {}
    return data


def load_data_and_render(request, json_name, html_name=None):
    """Loads data from a JSON file and renders a template.
    JSON files are stored in the "/data" folder.
    HTML files are stored in the "nest" template folder.

    Args:
        request: HTTP request.
        json_name: JSON filename without extension.
        html_name: HTML filename without extension.
        If html_name is not specified, the json_name will be also used as the HTML filename.

    Returns: HTTP Response.

    """
    if html_name is None:
        html_name = json_name
    html_file = "nest/" + html_name + ".html"
    try:
        get_template(html_file)
    except TemplateDoesNotExist:
        message = "Template \"%s\" does not exist." % html_file
        return HttpResponseNotFound(message)
    return render(request, html_file, load_json(json_name))


def render_markdown(request, markdown_file):
    """Loads data from a markdown file and renders it in the "page" template.

    Args:
        request: HTTP request.
        markdown_file: Filename with full path and extension (.md).

    Returns: HTTP Response.

    """
    if os.path.exists(markdown_file):
        with open(markdown_file) as f:
            text = f.read()
    else:
        return HttpResponseNotFound(markdown_file + " not found.")
    html_content = markdown.markdown(
        text,
        output_format="html5",
    )
    return render(request, "nest/page.html", {"html_content": html_content})


def page(request, filename):
    """Renders a markdown file stored in the "data/markdown" folder.

    Args:
        request: HTTP request.
        filename: Filename without extension.

    Returns: HTTP Response.

    """
    markdown_file = os.path.join(settings.BASE_DIR, "data", "markdown", filename + ".md")
    return render_markdown(request, markdown_file)


def cards(request, filename):
    return load_data_and_render(request, "cards/" + filename, "cards")


def timeline(request, filename):
    return load_data_and_render(request, filename, "timeline")


def activate(request):
    try:
        r = urlfetch.fetch('http://qiu.azurewebsites.net', method='GET', deadline=20)
        if r.status_code == 200:
            return HttpResponse("Nest activated successfully.")
        else:
            return HttpResponseBadRequest("Status Code: " + str(r.status_code))
    except Exception as ex:
        return HttpResponse("Exception.")

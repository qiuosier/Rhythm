import os
import json
import markdown
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.conf import settings
from nest.lib import load_json, ascii_char, get_markdown_title


def index(request):
    return load_data_and_render(request, "index")


def skylark_collection(request, collection):
    data = load_json("skylark/" + collection)
    return render(request, "nest/skylark_collection.html", data)


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


def page(request, filename):
    """Renders a markdown file stored in the "data/markdown" folder.

    Args:
        request: HTTP request.
        filename: Filename without extension.

    Returns: HTTP Response.

    """
    markdown_file = os.path.join(settings.BASE_DIR, "data", "markdown", filename + ".md")
    if os.path.exists(markdown_file):
        with open(markdown_file) as f:
            text = f.read()
    else:
        return HttpResponseNotFound(markdown_file + " not found.")

    text = filter(ascii_char, text)
    title = get_markdown_title(text)
    html_content = markdown.markdown(
        text,
        output_format="html5",
    )
    return render(request, "nest/page.html", {
        "title": title,
        "html_content": html_content
    })


def timeline(request, filename):
    return load_data_and_render(request, filename, "timeline")

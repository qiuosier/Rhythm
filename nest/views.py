import os
import json
import markdown
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.template.loader import get_template, render_to_string
from django.template import TemplateDoesNotExist
from django.conf import settings
from nest.lib import load_json, ascii_char, get_markdown_title, search_file
from nest import transform


def render_template(request, html_name, json_name=None, transform_name=None):
    """Loads data from a JSON file, transforms it with a function and renders it with an HTML template.

    Args:
        request: HTTP request.
        html_name: HTML filename without extension.
        json_name: JSON filename without extension.
        transform_name: The function name in transform.py.
            This function will be used to transform the data loaded from the json file.

        If json_name is not specified, the html_name will be also used as json_name.
        If transform_name is not specified, the html_name will be also used as transform_name.

    Returns: If the request is AJAX, a JSON response. Otherwise HTTP Response.

    JSON files should be stored in the "/data" or "/data/components" folder.
    HTML files should be stored in the "/nest/templates/nest" or "/nest/templates/nest/components" folder.

    """
    html_root = os.path.join(settings.BASE_DIR, "nest", "templates")
    data_root = os.path.join(settings.BASE_DIR, "data")
    html_dirs = [
        "nest",
        "nest/components"
    ]
    data_dirs = [
        "",
        "components"
    ]

    # Get template file path.
    html_file = search_file(html_dirs, html_name + ".html", root=html_root)
    if not html_file:
        return HttpResponseNotFound("Template \"%s\" does not exist." % html_name)

    # Load data
    # Get data file path.
    if json_name is None:
        json_name = html_name
    json_file = search_file(data_dirs, json_name + ".json", root=data_root)
    if json_file:
        # Load json data from file.
        context = load_json(json_file)
        # Transform data.
        if transform_name is None:
            transform_name = json_name
        if hasattr(transform, transform_name):
            transform_func = getattr(transform, transform_name)
            context = transform_func(context)
    else:
        # No data file exists.
        context = {}

    # Return response
    if request.is_ajax():
        return JsonResponse({
            "html": render_to_string(html_file, context)
        })
    else:
        return render(request, html_file, context)


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


def index(request):
    return render_template(request, "index")


def skylark_collection(request, collection):
    data = load_json("skylark/" + collection)
    return render(request, "nest/skylark_collection.html", data)

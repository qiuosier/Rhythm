import os
from django import template
from django.conf import settings
register = template.Library()


@register.filter
def get_field_value(obj, field):
    """Gets the value of a field/property/attribute/key in an object.
    This function supports chained properties connected by dot(.) or double underscores(__)
    """
    field = field.replace('.', '__')
    attrs = field.split('__')
    value = ''
    for attr in attrs:
        if obj is not None and hasattr(obj, attr):
            value = getattr(obj, attr)
            if callable(value):
                value = value()
        elif isinstance(obj, dict):
            value = obj.get(attr)
        obj = value
        if obj is None:
            break
    return value


@register.filter
def canonical_link_tag(request):
    """Returns <link rel="canonical" href="..."> html tag,
    if request.META['HTTP_HOST'] is not the same as os.environ.get("DOMAIN")

    Empty string will be returned if os.environ.get("DOMAIN") is None or empty.
    
    Args:
        request (HttpRequest): Django Http Request
    
    Returns:
        str: A string of HTML <link /> tag or empty string.
    """
    canonical_domain = os.environ.get("DOMAIN")
    if canonical_domain and "HTTP_HOST" in request.META:
        domain = request.META['HTTP_HOST']
        if domain != canonical_domain:
            return "<link rel=\"canonical\" href=\"https://%s%s\" />" % (canonical_domain, request.path)
    return ""

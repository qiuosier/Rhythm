from django import template
register = template.Library()


@register.filter
def get_field_value(obj, field):
    """Gets the value of a field/property/attribute/key in an object.
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

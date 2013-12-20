from django import template
register = template.Library()


@register.filter('type')
def get_type(value):
    return value.__class__.__name__

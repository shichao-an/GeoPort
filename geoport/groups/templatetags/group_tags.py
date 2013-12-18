from django import template
register = template.Library()
from django.core.urlresolvers import reverse


@register.filter('join_group_tags')
def join_group_tags(value, arg):
    from django.utils.html import conditional_escape
    arr = []
    for t in value:
        arr.append('<a href="%s">%s</a>' % (
            reverse('groups:tag', kwargs={'slug': t}), t
        ))
    return arg.join(arr)


@register.filter('join_users')
def join_users(value, arg):
    from django.utils.html import conditional_escape
    arr = []
    for u in value:
        arr.append('<a href="%s">%s</a>' % (
            reverse('user', kwargs={'username': u.username}), u.name
        ))
    return arg.join(arr)

import json
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from groups.models import Group
from accounts.models import User
from .models import Event
from .utils import get_markers


@require_GET
@login_required
def markers(request, group_slug, event_id):
    """Get a list of Google Maps marker objects for visible participants"""
    data = {'success': False}
    try:
        group = Group.objects.get(slug=group_slug)
    except:
        data['code'] = 1
        data['message'] = 'This group does not exist.'
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        event = Event.objects.get(group=group, id=event_id)
    except:
        data['code'] = 2
        data['message'] = 'This event does not exist.'
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user not in event.users and request.user != event.creator:
        data['code'] = 3
        data['message'] = 'You are neither the creator nor a participant.'
        return HttpResponse(json.dumps(data), content_type="application/json")

    markers = get_markers(event)
    data['code'] = 0
    data['success'] = True
    data['markers'] = markers
    return HttpResponse(json.dumps(data), content_type="application/json")


@require_POST
@login_required
def leave(request, group_slug, event_id):
    data = {'success': False}
    try:
        group = Group.objects.get(slug=group_slug)
    except:
        data['code'] = 1
        data['message'] = 'This group does not exist.'
        return HttpResponse(json.dumps(data), content_type="application/json")
    try:
        event = Event.objects.get(group=group, id=event_id)
    except:
        data['code'] = 2
        data['message'] = 'This event does not exist.'
        return HttpResponse(json.dumps(data), content_type="application/json")
    if request.user not in event.users:
        data['code'] = 3
        data['message'] = 'You are not a participant.'
        return HttpResponse(json.dumps(data), content_type="application/json")

    if request.user in event.visible_users:
        event.remove_participant(request.user, True)
    else:
        event.remove_participant(request.user, False)
    data['code'] = 0
    data['success'] = True
    return HttpResponse(json.dumps(data), content_type="application/json")

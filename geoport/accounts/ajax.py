import json
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .models import User


FETCH_LIMIT = 8


@require_GET
@login_required
def users(request):
    """Query users"""
    query = request.GET.get('query')
    data = []
    if query:
        users = User.objects.filter(username__istartswith=query)[:FETCH_LIMIT]
        data = [
            {
                'name': user.name,
                'value': user.username,
            }
            for user in users
        ]
    return HttpResponse(json.dumps(data), content_type="application/json")


@require_POST
@login_required
def location(request):
    """Update user location"""
    data = {}
    data['success'] = True
    data['code'] = 0
    if request.method == 'POST':
        # `raw_location' is a comma-separated string
        raw_location = request.POST.get('location')
        if raw_location:
            location = [float(s.strip()) for s in raw_location.split(',')]
            # Perform atomic update of location on this user
            if len(location) == 2:
                request.user.update(set__location=location)
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
    data['success'] = False
    data['code'] = 1
    data['message'] = 'Invalid location.'
    return HttpResponse(json.dumps(data), content_type="application/json")

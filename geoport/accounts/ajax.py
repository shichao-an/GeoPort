import json
from django.http import HttpResponse
from django.views.decorators.http import require_GET
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


@login_required
def location(request):
    data = {}
    data['success'] = True
    data['code'] = 0
    if request.method == 'POST':
        # `raw_location' is a comma-separated string
        print request.POST
        raw_location = request.POST.get('location')
        print 1, raw_location
        if raw_location:
            location = [float(s.strip()) for s in raw_location.split(',')]
            # Perform atomic update of location on this user
            request.user.update(set__location=location)
            return HttpResponse(json.dumps(data),
                                content_type="application/json")

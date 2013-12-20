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
    if request.method == 'POST':
        raw_location = request.POST.get('location')
        if raw_location:
            pass

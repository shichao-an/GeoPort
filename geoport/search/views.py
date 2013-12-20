from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render


def index(request):
    return render(request, "portal/devops.html")

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render


@login_required
def event(request, blog_slug, event_slug):
    pass


@login_required
def edit(request, blog_slug, event_slug):
    pass


@login_required
def create(request, slug):
    pass

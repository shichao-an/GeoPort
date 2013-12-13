from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request):
    context = {}
    return render(request, "groups/index.html", context)

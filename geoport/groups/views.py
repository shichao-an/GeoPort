from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from .models import Group
from .forms import GroupForm
from .utils import get_post_data


@login_required
def index(request):
    context = {}
    return render(request, 'groups/index.html', context)


@login_required
def create(request):
    context = {}
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            print form.cleaned_data
            group.tags = form.cleaned_data['tags']
            group.save()
            return HttpResponseRedirect(group.get_absolute_url())
        else:
            # Retain POST data if invalid
            data = get_post_data(request, *form.fields)
            form.initial = data
            context['form'] = form
    else:
        form = GroupForm()
    context['form'] = form
    return render(request, 'groups/create.html', context)


@login_required
def events(request):
    pass


@login_required
def personal(request):
    """Personal Group"""
    pass


@login_required
def group(request, slug):
    """Public/Private Group"""
    context = {}
    try:
        group = Group.objects.get(slug=slug)
    except:
        raise Http404
    context['group'] = group
    return render(request, 'groups/group.html', context)

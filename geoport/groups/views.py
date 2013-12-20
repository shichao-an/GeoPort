from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from geoport.utils import (handle_uploaded_file, delete_file, get_post_data,
                           get_initial_data)
from events.models import Event
from .models import Group
from .forms import GroupForm


@login_required
def index(request):
    f = request.GET.get('filter')
    if f == 'yours':
        groups = Group.objects.filter(members__user=request.user)
    else:
        groups = Group.objects.all()
    context = {}
    context['groups'] = groups
    return render(request, 'groups/index.html', context)


@login_required
def create(request):
    context = {}
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.tags = form.cleaned_data['tags']
            if form.cleaned_data['logo']:
                path = handle_uploaded_file(request.FILES['logo'], 'uploads')
                group.logo = path
            group.save()
            return HttpResponseRedirect(group.get_absolute_url())
        else:
            # Retain POST data if invalid
            data = get_post_data(request, *form.fields)
            form.initial = data
            #context['form'] = form
    else:
        form = GroupForm()
    context['form'] = form
    return render(request, 'groups/create.html', context)


@login_required
def events(request):
    context = {}
    return render(request, 'groups/events.html', context)


@login_required
def personal(request):
    """Personal Group"""
    pass


@login_required
def group_index(request):
    """/groups/group/ redirected to /groups/"""
    return HttpResponseRedirect(reverse('groups:index'))


@login_required
def group(request, slug):
    """Public/Private Group"""
    context = {}
    try:
        group = Group.objects.get(slug=slug)
    except:
        raise Http404
    context['group'] = group
    events = Event.objects.filter(group=group)
    context['events'] = events
    return render(request, 'groups/group.html', context)


@login_required
def settings(request):
    """Settings/Management for `Your Groups' (reserved)"""
    pass


@login_required
def tag(request, slug):
    pass


@login_required
def group_settings(request, slug):
    context = {}
    try:
        group = Group.objects.get(slug=slug)
    except:
        raise Http404
    if request.user not in group.staff:
        raise PermissionDenied

    context['group'] = group
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.tags = form.cleaned_data['tags']
            if form.cleaned_data['logo']:
                path = handle_uploaded_file(request.FILES['logo'], 'uploads')
                old_path = group.logo
                if old_path:
                    delete_file(old_path)
                group.logo = path
            group.save()
            return HttpResponseRedirect(group.get_absolute_url())
        else:
            # Retain POST data if invalid
            data = get_post_data(request, *form.fields)
            form.initial = data
            #context['form'] = form
    else:
        form = GroupForm(instance=group)
        form.initial = get_initial_data(group, *form.fields)
        form.initial['tags'] = ','.join(form.initial['tags'])
    context['form'] = form
    return render(request, 'groups/group_settings.html', context)

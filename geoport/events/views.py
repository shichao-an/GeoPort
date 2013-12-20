from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from groups.models import Group
from geoport.utils import (handle_uploaded_file, delete_file, get_post_data,
                           get_initial_data)
from .models import Event
from .forms import EventForm, ParticipateForm
import pdb


@login_required
def event(request, group_slug, event_id):
    context = {}
    try:
        group = Group.objects.get(slug=group_slug)
    except:
        raise Http404
    try:
        event = Event.objects.get(group=group, id=event_id)
    except:
        raise Http404
    context['group'] = group
    context['event'] = event
    return render(request, 'events/event.html', context)


@login_required
def create(request, slug):
    try:
        group = Group.objects.get(slug=slug)
    except:
        raise Http404
    if request.user not in group.staff:
        return PermissionDenied
    context = {}
    context['group'] = group
    if request.method == 'POST':
        form = EventForm(request.POST)
        d = get_post_data(request, *form.fields)
        print d
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.group = group
            event.tags = form.cleaned_data['tags']
            event.save()
            return HttpResponseRedirect(event.get_absolute_url())
        else:
            # Retain POST data if invalid
            data = get_post_data(request, *form.fields)
            form.initial = data
    else:
        form = EventForm()
    #print 123, form.initial
    #print form.initial['start_time']
    context['form'] = form
    return render(request, 'events/create.html', context)


@login_required
def edit(request, group_slug, event_id):
    try:
        group = Group.objects.get(slug=group_slug)
    except:
        raise Http404
    try:
        event = Event.objects.get(group=group, id=event_id)
    except:
        raise Http404
    if request.user not in group.staff:
        return PermissionDenied
    context = {}
    context['group'] = group
    context['event'] = event
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        d = get_post_data(request, *form.fields)
        print d
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.group = group
            event.tags = form.cleaned_data['tags']
            event.save()
            return HttpResponseRedirect(event.get_absolute_url())
        else:
            # Retain POST data if invalid
            data = get_post_data(request, *form.fields)
            form.initial = data
    else:
        form = EventForm(instance=event)
        form.initial = get_initial_data(event, *form.fields)
        form.initial['tags'] = ','.join(form.initial['tags'])
    context['form'] = form
    return render(request, 'events/edit.html', context)


@login_required
def participate(request, group_slug, event_id):
    try:
        group = Group.objects.get(slug=group_slug)
    except:
        raise Http404
    try:
        event = Event.objects.get(group=group, id=event_id)
    except:
        raise Http404
    if request.user == event.creator:
        return HttpResponseRedirect(event.get_absolute_url())
    context = {}
    context['group'] = group
    context['event'] = event
    if request.method == 'POST':
        form = ParticipateForm(request.POST)
        if form.is_valid():
            visible = form.cleaned_data['visible']
            event.add_participant(request.user, visible)
            event.save()
            return HttpResponseRedirect(event.get_absolute_url())
        else:
            # Retain POST data if invalid
            data = get_post_data(request, *form.fields)
            form.initial = data
    else:
        form = ParticipateForm()
    context['form'] = form
    return render(request, 'events/participate.html', context)

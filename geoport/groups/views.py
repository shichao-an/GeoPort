from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from accounts.utils import handle_uploaded_file, delete_file
from .models import Group
from .forms import GroupForm
from geoport.utils import get_post_data


@login_required
def index(request):
    context = {}
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
def group_index(request):
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
    context['group'] = group
    return render(request, 'groups/group_settings.html', context)

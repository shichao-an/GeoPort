from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import GroupForm


def index(request):
    context = {}
    return render(request, "groups/index.html", context)


def create(request):
    context = {}
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            group.authors.add(request.user)
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('group', kwargs={'slug': group.slug}))
        else:
            # Retain POST data if invalid
            data = {
                'name': request.POST.get('name'),
            }
            form.initial = data
            context['form'] = form
    else:
        form = GroupForm()
    context['form'] = form
    return render(request, "groups/create.html", context)


def events(request):
    pass


def personal(request):
    """Personal Group"""
    pass


def group(request):
    """Public/Private Group"""
    pass

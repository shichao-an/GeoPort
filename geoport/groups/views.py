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
            blog = form.save(commit=False)
            blog.creator = request.user
            blog.save()
            blog.authors.add(request.user)
            form.save_m2m()
            return HttpResponseRedirect(
                reverse('blog', kwargs={'slug': blog.slug}))
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
    return render(request, "blogs/create.html", context)


def events(request):
    pass


def personal(request):
    pass

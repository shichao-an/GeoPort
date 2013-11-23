from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserCreationForm


@login_required
def index(request):
    """Index: /accounts/"""
    return HttpResponseRedirect("/accounts/profile/")


def login_view(request):
    """Global portal: /"""
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    else:
        import django.contrib.auth.views as auth_views
        return auth_views.login(request, template_name='accounts/login.html')


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/")
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password1"))
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    context['form'] = form
    return render(request, "accounts/signup.html", context)


@login_required
def profile(request):
    """Global portal: /accounts/profile/"""
    return render(request, "accounts/profile.html")

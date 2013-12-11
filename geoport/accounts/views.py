from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserCreationForm, FileUploadForm
from .utils import handle_uploaded_file, delete_file


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
    print dir(request.user._fields)
    return render(request, "accounts/profile.html")


@login_required
def settings(request):
    """Global portal: /accounts/settings/"""
    return render(request, "accounts/profile.html")


@login_required
def avatar(request):
    """Global portal: /accounts/avatar/"""
    context = {}
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            path = handle_uploaded_file(request.FILES['file'], 'avatar')
            old_path = request.user.avatar
            if old_path:
                delete_file(old_path)
            request.user.avatar = path
            request.user.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = FileUploadForm()

    context['form'] = form
    return render(request, "accounts/avatar.html", context)

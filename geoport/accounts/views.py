from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, FileUploadForm, UserSettingsForm
from .utils import handle_uploaded_file, delete_file, get_social_auth


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
    social_auth = get_social_auth(request.user)
    context = {
        'social_auth': social_auth,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def settings(request):
    """Global portal: /accounts/settings/"""
    context = {}
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:settings'))
    else:
        form = UserSettingsForm(instance=request.user)
    context['form'] = form
    return render(request, "accounts/settings.html")


@login_required
def password(request):
    """Global portal: /accounts/password/"""
    return render(request, "accounts/settings.html")


@login_required
def email(request):
    """Global portal: /accounts/email/"""
    return render(request, "accounts/settings.html")


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

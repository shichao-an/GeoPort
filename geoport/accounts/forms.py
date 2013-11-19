from django import forms
#from django.contrib.auth.forms import UserCreationForm as _UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from mongodbforms import DocumentForm
from accounts.models import User


class UserCreationForm(DocumentForm):
    """
    Custom UserCreationForm for use with MongoEngine.

    Based on django.contrib.auth.forms.UserCreationForm.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    first_name = forms.CharField(label=_("First name"), max_length=255)
    last_name = forms.CharField(label=_("Last name"), max_length=255)
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if first_name:
            return first_name.strip()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if last_name:
            return last_name.strip()
        return last_name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

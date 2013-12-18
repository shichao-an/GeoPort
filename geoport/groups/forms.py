from django import forms
from mongodbforms import DocumentForm
from .models import Group


class GroupForm(DocumentForm):

    class Meta:
        model = Group
        fields = ("name", "description", "is_public", "tags")

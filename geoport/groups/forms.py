from django import forms
from mongodbforms import DocumentForm
from .models import Group
import pdb


class GroupForm(DocumentForm):

    class Meta:
        model = Group
        fields = ('name', 'description', 'logo', 'is_public')

    tags = forms.CharField(required=False)

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(',') if data else []
        return tags

from django import forms
from mongodbforms import DocumentForm
from geoport.utils import DivErrorList
from .models import Group
import pdb


class GroupForm(DocumentForm):

    class Meta:
        model = Group
        fields = ('name', 'description', 'is_public')

    tags = forms.CharField(required=False)
    logo = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = DivErrorList
        super(GroupForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(',') if data else []
        return tags

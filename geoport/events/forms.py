from django import forms
from mongodbforms import DocumentForm
from .models import Event
import pdb


class EventForm(DocumentForm):

    class Meta:
        model = Event
        fields = (
            'title', 'description', 'address', 'zip_code', 'start_time',
            'end_time', 'size',
        )

    tags = forms.CharField(required=False)
    start_time = forms.DateTimeField()  # Override SplitDateTimeField
    end_time = forms.DateTimeField(required=False)  # Ditto

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(',') if data else []
        return tags

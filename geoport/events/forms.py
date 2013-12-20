from django import forms
from django.utils import timezone
from mongodbforms import DocumentForm
from geoport.utils import get_location_by_address, DivErrorList
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

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = DivErrorList
        super(EventForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(',') if data else []
        return tags

    def clean(self):
        cleaned_data = super(DocumentForm, self).clean()
        start_time = cleaned_data['start_time']
        if start_time < timezone.now():
            msg = "Start time must be a future time."
            self._errors['start_time'] = self.error_class([msg])
            del cleaned_data['start_time']

        # Clean `end_time' is `start_time' is valid
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data['end_time']
        if start_time and end_time:
            if end_time <= start_time:
                msg = "End time must be later than start time."
                self._errors['end_time'] = self.error_class([msg])
                del cleaned_data['end_time']

        # Clean `address'
        address = cleaned_data.get('address')
        zip_code = cleaned_data.get('zip_code')
        if address:
            location = get_location_by_address(address)
            if location:
                cleaned_data['location'] = location
            else:
                if zip_code:
                    location = get_location_by_address(zip_code)
                    if location:
                        cleaned_data['location'] = location
                    else:
                        msg = "Both address and zip code are invalid."
                        raise forms.ValidationError(msg)
                else:
                    msg = "Address is invalid. Please enter a correct address."
                    self._errors['address'] = self.error_class([msg])
                    del cleaned_data['address']
        return cleaned_data


class ParticipateForm(forms.Form):
    visible = forms.BooleanField(required=False, help_text='Share location')

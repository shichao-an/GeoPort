# Signal handler functions for MongoEngine documents
from django.utils import timezone


def auto_now_add(sender, document, values):
    values['date_created'] = timezone.now()

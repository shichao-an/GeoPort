from django.core.urlresolvers import reverse
from mongoengine import Document, EmbeddedDocument
from mongoengine import (StringField, ListField, BooleanField, ReferenceField,
                         EmbeddedDocumentField, DateTimeField, GeoPointField,
                         IntField)
from mongoengine import CASCADE, PULL
from mongoengine import signals
from mongoengine_extras.fields import SlugField
from accounts.models import User
from groups.models import Group
from django.utils import timezone
from .signals import auto_now_add


class Participant(EmbeddedDocument):
    user = ReferenceField(User)
    visible = BooleanField(default=False)

    def __unicode__(self):
        visibility = 'visible' if self.visible else 'invisible'
        return "%s (%s)" % (self.user.name, visibility)


class Event(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    group = ReferenceField(Group, reverse_delete_rule=CASCADE)
    creator = ReferenceField(User)
    photos = ListField(StringField())
    participants = ListField(EmbeddedDocumentField(Participant))
    waiting_list = ListField(EmbeddedDocumentField(Participant))
    address = StringField(required=True)
    zip_code = IntField()
    location = GeoPointField()
    date_created = DateTimeField(required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField()
    size = IntField(min_value=1)  # Size cannot be changed after start
    tags = ListField(StringField())
    meta = {
        'indexes': ['title']
    }

    __original_size = None

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)

        # Get a copy of original size
        self.__original_size = self.size

    def save(self, *args, **kwargs):
        # Size has been changed
        if self.__original_size != self.size:
            # Event has not started yet
            if timezone.now() < self.start_time:
                if len(self.participants) > self.size:
                    p = self.participants[:self.size]  # Kept participants
                    w = self.participants[self.size:]  # Purged to waiting_list
                    self.participants = p
                    self.waiting_list = self.waiting_list + w

        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'group_slug': self.group.slug,
            'event_id': self.id,
        }
        return reverse(
            'events:event', kwargs=kwargs)

    def __unicode__(self):
        return self.title

    @property
    def users(self):
        """Return participants as users"""
        return [
            participant.user for participant in self.participants
        ]

    def add_participant(self, user, visible):
        if user == self.creator:
            raise Exception('Event creator cannot participate.')
        p = Participant(user=user, visible=visible)
        self.update(add_to_set__participants=p)

    def remove_participant(self, user):
        if user in self.users:
            participant = Participant(user=user)
            self.update(pull__participants=participant)
        else:
            raise Exception('This user is not a participant.')

    def edit_participant(self, user, visible):
        """Edit the visibility of a participant user."""
        events = Event.objects(id=self.id, participants__user=user)
        events.update_one(set__participants__S__visible=visible)

# Attaching events
signals.pre_init.connect(auto_now_add, Event)

from django.core.urlresolvers import reverse
from django.utils import timezone
from geoport.utils import uuslug
from mongoengine import Document, EmbeddedDocument
from mongoengine import (StringField, ListField, BooleanField, ReferenceField,
                         EmbeddedDocumentField, DateTimeField)
from mongoengine import CASCADE, PULL, Q
from mongoengine import signals
from mongoengine_extras.fields import SlugField, AutoSlugField
from accounts.models import User
from .signals import auto_now_add


# Member.member_type options
GROUP_CREATOR = 'creator'
GROUP_ADMIN = 'admin'


class Member(EmbeddedDocument):
    member_type = StringField()  # `admin' and `creator' (None for `member')
    user = ReferenceField(User)  # reverse_delete_rule not supported here

    def is_staff(self):
        if self.member_type is not None:
            return True
        return False

    @property
    def is_creator(self):
        if self.member_type == GROUP_CREATOR:
            return True
        return False

    @property
    def is_admin(self):
        if self.member_type == GROUP_ADMIN:
            return True
        return False

    def __unicode__(self):
        return "%s (%s)" % (self.user.name, self.member_type)


class Group(Document):
    name = StringField(required=True, max_length=100)
    slug = SlugField()  # AutoSlugField has bugs
    description = StringField()
    is_public = BooleanField(default=True, help_text='Is Public')
    logo = StringField()
    photos = ListField(StringField())
    members = ListField(EmbeddedDocumentField(Member))
    date_created = DateTimeField(required=True)
    tags = ListField(StringField())
    meta = {
        'indexes': ['name', 'slug']
    }

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Group, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:group', kwargs={'slug': self.slug})

    @property
    def past_events(self):
        from events.models import Event
        events = Event.objects.filter(
            Q(group=self) & Q(date_created__lte=timezone.now())
        )
        return events

    @property
    def upcoming_events(self):
        from events.models import Event
        events = Event.objects.filter(
            Q(group=self) & Q(date_created__gte=timezone.now())
        )
        return events

    @property
    def creator(self):
        """Creator is always the first member of a group"""
        return self.members[0].user

    @creator.setter
    def creator(self, user):
        if not self.members:
            member = Member(user=user, member_type=GROUP_CREATOR)
            self.members.append(member)

    def __unicode__(self):
        return self.name


class PersonalGroup(Document):
    user = ReferenceField(User)
    members = ListField(ReferenceField(User, reverse_delete_rule=PULL))

    @property
    def name(self):
        return self.user.name

    @property
    def slug(self):
        return self.user.username

    def __unicode__(self):
        return self.name

# Attaching events
signals.pre_init.connect(auto_now_add, Group)

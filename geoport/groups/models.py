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

    @property
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
        if self.member_type:
            return "%s (%s)" % (self.user.name, self.member_type)
        else:
            return self.user.name


class Group(Document):
    name = StringField(required=True, max_length=100)
    slug = SlugField(unique=True)  # AutoSlugField has bugs
    description = StringField()
    is_public = BooleanField(default=True, help_text='Is Public')
    logo = StringField()
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

    @property
    def admins(self):
        return [
            member.user for member in self.members if member.is_admin
        ]

    @property
    def staff(self):
        return [
            member.user for member in self.members if member.is_staff
        ]

    @property
    def users(self):
        return [
            member.user for member in self.members
        ]

    @property
    def regular_users(self):
        return [
            member.user for member in self.members if not member.is_staff
        ]

    @property
    def authentic_users(self):
        """All members except creator
        Admins will be in the front
        """
        return [
            user for user in self.admins + self.regular_users
        ]

    @property
    def regular_members(self):
        return [
            member for member in self.members if not member.is_staff
        ]

    @property
    def authentic_members(self):
        """All members except creator
        Admins will be in the front
        """
        admin_members = [member for member in self.members if member.is_admin]
        return [
            member for member in admin_members + self.regular_members
        ]

    def add_member(self, user, member_type=None):
        """Add a user as a member to the group
        Adding an existing user with a different `member_type' will raise.
        In other cases, atomic updates will be used.
        """
        if member_type == GROUP_CREATOR:
            raise Exception('Creator cannot be added.')
        if member_type is not None:
            if member_type not in [GROUP_ADMIN]:
                raise Exception('Invalid member type.')
        if user != self.creator:
            if member_type == GROUP_ADMIN:
                if user not in self.regular_users:
                    member = Member(user=user, member_type=GROUP_ADMIN)
                else:
                    raise Exception('This user is already a regular member.')
            else:
                if user not in self.admins:
                    member = Member(user=user)
                else:
                    raise Exception('This user is already an admin.')
            self.update(add_to_set__members=member)
        else:
            raise Exception('This user is already the creator.')

    def remove_member(self, user):
        """Remove a user (member) from the group
        Removing an non-existent user will not raise exceptions.
        """
        if user != self.creator:
            member = Member(user=user)
            self.update(pull__members=member)
        else:
            raise Exception('The creator cannot be removed.')

    def edit_member(self, user, member_type):
        """Edit the `member_type' of an existing member to
        """
        if user in self.users:
            if user == self.creator:
                raise Exception('Creator cannot be edited.')
            if member_type == GROUP_CREATOR:
                raise Exception('Creator cannot be edited.')
            if member_type is not None:
                if member_type not in [GROUP_ADMIN]:
                    raise Exception('Invalid member type.')

            # Use QuerySet to perform atomic update
            groups = Group.objects(id=self.id, members__user=user)
            if member_type:
                groups.update_one(set__members__S__member_type=member_type)
            else:
                # Set `member_type' to None
                groups.update_one(unset__members__S__member_type=member_type)
        else:
            raise Exception('This user is not a member.')

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

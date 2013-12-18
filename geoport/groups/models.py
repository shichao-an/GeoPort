from mongoengine import Document, EmbeddedDocument
from mongoengine import (StringField, ListField, BooleanField, ReferenceField,
                         EmbeddedDocumentField, DateTimeField)
from mongoengine import CASCADE, PULL
from mongoengine_extras.fields import AutoSlugField
from accounts.models import User


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


class Group(Document):
    name = StringField(required=True, max_length=100)
    slug = AutoSlugField(required=True)
    description = StringField()
    is_public = BooleanField(default=True)
    members = ListField(EmbeddedDocumentField(Member))
    date_created = DateTimeField(required=True)
    tags = ListField(StringField())
    meta = {
        'indexes': ['name', 'slug']
    }

    def save(self, *args, **kwargs):
        self.slug = self.name
        super(Group, self).save(*args, **kwargs)


class PersonalGroup(Document):
    user = ReferenceField(User)
    members = ListField(ReferenceField(User, reverse_delete_rule=PULL))

    @property
    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def slug(self):
        return self.user.username

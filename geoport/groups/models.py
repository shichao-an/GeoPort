from mongoengine import Document, EmbeddedDocument
from mongoengine import (StringField, ListField, BooleanField, ReferenceField,
                         EmbeddedDocumentField, DateTimeField)
from mongoengine import CASCADE, PULL
from mongoengine_extras.fields import SlugField
from accounts.models import User


# Member.member_type options
GROUP_CREATOR = 'creator'
GROUP_ADMIN = 'admin'


class Member(EmbeddedDocument):
    member_type = StringField()  # `admin' and `creator' (None for `member')
    member = ReferenceField(User)  # reverse_delete_rule not supported here

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
    name = StringField(required=True)
    description = StringField()
    is_public = BooleanField()
    slug = SlugField()
    members = ListField(EmbeddedDocumentField(Member))
    date_created = DateTimeField(required=True)
    tags = ListField(StringField())


class PersonalGroup(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    members = ListField(ReferenceField(User, reverse_delete_rule=PULL))

from mongoengine import Document, EmbeddedDocument
from mongoengine import (StringField, ListField, BooleanField, ReferenceField,
                         EmbeddedDocumentField, DateTimeField)
from mongoengine import CASCADE
from mongoengine_extras.fields import SlugField
from accounts.models import User


GROUP_CREATOR = 'creator'
GROUP_ADMIN = 'admin'
GROUP_MEMBER = 'member'


class Member(EmbeddedDocument):
    member_type = StringField()  # `admin', `creator', and `member'
    member = ReferenceField(User)  # reverse_delete_rule not supported here

    def is_staff(self):
        if self.member_type == GROUP_CREATOR \
                or self.member_type == GROUP_ADMIN:
            return True
        return False


class Group(Document):
    name = StringField(required=True)
    description = StringField()
    is_public = BooleanField()
    slug = SlugField()
    members = ListField(EmbeddedDocumentField(Member))
    date_created = DateTimeField(required=True)


class PersonalGroup(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    members = ListField(EmbeddedDocumentField(Member))

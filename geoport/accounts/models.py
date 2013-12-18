from django.core.urlresolvers import reverse
from mongoengine.django.auth import User as _User
from mongoengine import (Document, StringField, ListField, IntField,
                         ReferenceField, GenericReferenceField)


# GeoPortUser.gender options
GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_OTHERS = 3


class GeoPortUser(_User):
    """Custom user class for this project.

    `MONGOENGINE_USER_DOCUMENT` should specify this class.

    This class defines custom fields in addition to the default User document.

    Use mongoengine.django.mongo_auth.models.get_user_document() to get
    this class.

    The collection name of this model is `User`, which is the same collection
    as its superclass uses

    """

    # `username` is already required
    REQUIRED_FIELDS = ['first_name', 'last_name']

    sid = StringField()  # unique=True is not necessary
    friends = ListField(ReferenceField('self'))
    social_friends = ListField(StringField())
    avatar = StringField()
    gender = IntField()
    meta = {
        'indexes': ['sid']
    }

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.username})

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

# Alias of `GeoPortUser`
# This makes sure get_user_document() equals `accounts.models.User`
User = GeoPortUser


class Request(Document):
    """Request associated with users as `action_object'
    """
    verb = StringField()  # `group', `event', `friend', `location'
    actor = ReferenceField(User)
    action_object = ReferenceField(User)
    target = GenericReferenceField()
    status = StringField()  # `pending', `approved', `declined'

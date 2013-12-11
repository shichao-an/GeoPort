from mongoengine.django.auth import User as _User
from mongoengine import (Document, StringField, ListField, IntField,
                         ReferenceField)


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
    meta = {
        'indexes': ['sid']
    }

# Alias of `GeoPortUser`
# This makes sure get_user_document() equals `accounts.models.User`
User = GeoPortUser

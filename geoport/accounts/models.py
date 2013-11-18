from mongoengine.django.auth import User


class GeoPortUser(User):
    """Custom user class for this project.

    `MONGOENGINE_USER_DOCUMENT` should specify this class.

    This class defines custom fields in addition to the default User document.

    Use mongoengine.django.mongo_auth.models.get_user_document() to get 
    this class.

    """
    REQUIRED_FIELDS = ['first_name', 'last_name']

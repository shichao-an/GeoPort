# User, account and social related utility functions
import os
import uuid
import random
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from social.apps.django_app.me.models import UserSocialAuth


def friending(user, friend):
    """Make `user' and `friend' friends with each other"""
    user.update(add_to_set__friends=friend)
    friend.update(add_to_set__friends=user)


def is_friend(user, friend):
    if user in friend.friends and friend in user.friends:
        return True
    return False


def generate_file_path(filename, category):
    """
    Generate hashed upload path similar to MediaWiki, though the filename is
    UUID instead of original one

    The result is something like this:
        avatars/5/d/5a754a6da92440f0b314edfcbad0bd5e.jpg

    """
    random_name = uuid.uuid4().hex
    directory, subdirectory = get_hashed_directories()
    extension = os.path.splitext(filename)[-1]
    fn = random_name + extension
    return os.path.join(category, directory, subdirectory, fn)


def get_hashed_directories():
    directory = hex(random.randint(1, 15)).lstrip('0x')
    subdirectory = hex(random.randint(1, 31)).lstrip('0x')
    return directory, subdirectory


def handle_uploaded_file(f, category, filename=None):
    """Universal function for handling uploaded file using `default_storage'"""
    path = None
    if hasattr(f, 'name'):
        path = generate_file_path(f.name, category)
        default_storage.save(path, f)
    elif not hasattr(f, 'name') and filename:
        path = generate_file_path(filename, category)
        default_storage.save(path, ContentFile(f))
    assert path is not None
    return path


def delete_file(path):
    default_storage.delete(path)


def get_social_auth(user):
    """Get social auth object if any"""
    try:
        social_auth = UserSocialAuth.objects.get(user=user)
    except UserSocialAuth.DoesNotExist:
        social_auth = None
    return social_auth

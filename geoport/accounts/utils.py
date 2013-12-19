# User, account and social related utility functions
from social.apps.django_app.me.models import UserSocialAuth


def friending(user, friend):
    """Make `user' and `friend' friends with each other"""
    user.update(add_to_set__friends=friend)
    friend.update(add_to_set__friends=user)


def is_friend(user, friend):
    if user in friend.friends and friend in user.friends:
        return True
    return False


def get_social_auth(user):
    """Get social auth object if any"""
    try:
        social_auth = UserSocialAuth.objects.get(user=user)
    except UserSocialAuth.DoesNotExist:
        social_auth = None
    return social_auth

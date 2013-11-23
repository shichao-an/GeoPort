# Custom pipeline functions for Python Social Auth Facebook backend
from social.backends.facebook import FacebookOAuth2


def retrieve_friends(strategy, details, response, user=None, *args, **kwargs):
    """Retrieve the list of Facebook friends of this social user"""
    if isinstance(strategy.backend, FacebookOAuth2):
        if user:
            pass


def retrieve_picture(strategy, details, response, user=None, *args, **kwargs):
    if isinstance(strategy.backend, FacebookOAuth2):
        if user:
            pass

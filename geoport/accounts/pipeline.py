# Custom pipeline functions for Python Social Auth Facebook backend
import requests
from social.backends.facebook import FacebookOAuth2


FACEBOOK_API_URL = 'https://graph.facebook.com/me'


def retrieve_friends(strategy, details, response, user=None, is_new=False,
                     *args, **kwargs):
    """Retrieve the list of friends from the social account of this user"""
    if isinstance(strategy.backend, FacebookOAuth2):
        if user:
            # Set `sid' field upon first social connection (signup)
            if is_new:
                facebook_id = response['id']
                user.sid = 'f' + facebook_id
                user.save()
            access_token = response['access_token']
            params = {
                'fields': 'friends',
                'access_token': access_token,
            }
            res = requests.get(FACEBOOK_API_URL, params=params).json()
            print res['friends']['data']


def retrieve_picture(strategy, details, response, user=None, *args, **kwargs):
    if isinstance(strategy.backend, FacebookOAuth2):
        if user:
            pass

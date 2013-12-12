# Custom pipeline functions for Python Social Auth Facebook backend
import urlparse
import requests
from social.backends.facebook import FacebookOAuth2
from .tasks import save_social_friends, save_social_avatar


FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
FACEBOOK_ME_URL = 'https://graph.facebook.com/me'


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
            res = requests.get(FACEBOOK_ME_URL, params=params).json()
            save_social_friends.delay(user, res, 'facebook')


def retrieve_picture(strategy, details, response, user=None, *args, **kwargs):
    if isinstance(strategy.backend, FacebookOAuth2):
        if user:
            path = response['id'] + '/' + 'picture'
            url = urlparse.urljoin(FACEBOOK_GRAPH_URL, path)
            save_social_avatar(url, user, 'facebook')

from __future__ import absolute_import
import requests
from celery import shared_task
from .models import User
from .utils import friending, is_friend
from geoport.utils import handle_uploaded_file, delete_file


@shared_task
def save_social_friends(user, result, social):
    if social == 'facebook':
        data = result['friends']['data']
        friend_ids = [friend['id'] for friend in data]
        user.social_friends = friend_ids
        user.save()


@shared_task
def match_social_friends(user, social):
    if social == 'facebook':
        for friend_id in user.social_friends:
            sid = 'f' + friend_id
            try:
                matched_friend = User.objects.get(sid=sid)
                if not is_friend(user, matched_friend):
                    friending(user, matched_friend)
            except User.DoesNotExist:
                continue


@shared_task
def save_social_avatar(url, user, social):
    """Save avatar from URL of social account"""
    params = {}
    if social == 'facebook':
        params['type'] = 'normal'
    f = requests.get(url, params=params).content
    fn = user.username + '.jpg'
    path = handle_uploaded_file(f, 'avatar', fn)
    old_path = user.avatar
    if old_path:
        delete_file(old_path)
    user.avatar = path
    user.save()

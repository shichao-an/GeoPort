# User, account and social related utility functions


def friending(user, friend):
    """Make `user' and `friend' friends with each other"""
    user.update(add_to_set__friends=friend)
    friend.update(add_to_set__friends=user)


def is_friend(user, friend):
    if user in friend.friends and friend in user.friends:
        return True
    return False

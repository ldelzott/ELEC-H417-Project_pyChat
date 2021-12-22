from constants import AUTH_SCREEN


def init():
    global active_users
    active_users = {}


def get_active_users():
    global active_users
    return active_users


def register(username, conn):
    """
    To allows for live exchanges between two users, a 'dict' data structure is used by the server. 'This dict'
    contains at any time the current 'screen' (i.e the menu) where any user is. It also contains the 'conn'
    object used in the SSL connection for that user, the name of that user as well as the person this user could be
    talking with.
    """
    global active_users
    active_users[username] = {
        "username": username,
        "conn": conn,
        "screen": AUTH_SCREEN,
        "talking_to": None,
    }


def unregister(username):
    """
    When a client leave the server, his name is removed from the 'dict' that contains all active users.
    """
    global active_users
    del active_users[username]


def update(username, dict):
    global active_users
    if username not in active_users:
        return

    for key, value in dict.items():
        active_users[username][key] = value

    # from pprint import pprint

    # for user in active_users.values():
    #     pprint(user)

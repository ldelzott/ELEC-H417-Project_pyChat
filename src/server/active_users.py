from constants import AUTH_SCREEN


def init():
    global active_users
    active_users = {}


def get_active_users():
    global active_users
    return active_users


def register(username, conn):
    global active_users
    active_users[username] = {
        "username": username,
        "conn": conn,
        "screen": AUTH_SCREEN,
        "talking_to": None,
    }


def unregister(username):
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

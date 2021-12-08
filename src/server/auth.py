from db import find_user_by_username, find_user_by_username_and_pwd, create_user
from reader import read_next_message, read_username_password
from writer import send_authentication_request, send_welcome_message, send_msg
from constants import LOGIN_MESSAGE, SIGNUP_MESSAGE


def on_login_success(conn, user):
    send_welcome_message(conn, user, False)


def on_signup_success(conn, user):
    send_welcome_message(conn, user, True)


def try_login(conn):
    username, password = read_username_password(conn)
    user = find_user_by_username_and_pwd(username, password)

    if not user:
        return False, "login error description"

    on_login_success(conn, user)
    return user, None


def try_signup(conn):
    username, password = read_username_password(conn)
    user_exists = find_user_by_username(username)

    if user_exists:
        return False, "username exists"

    new_user = create_user(username, password)

    on_signup_success(conn, new_user)
    return new_user, None


def authenticate_user(conn):
    user, error = None, "error"

    while error:
        send_authentication_request(conn)
        auth_msg = read_next_message(conn)

        if auth_msg == LOGIN_MESSAGE:
            user, error = try_login(conn)
        elif auth_msg == SIGNUP_MESSAGE:
            user, error = try_signup(conn)
        else:
            error = "invalid authentication message"

        if error:
            send_msg(conn, f"Authentication error: {error}, try again!")

    return user

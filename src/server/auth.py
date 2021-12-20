from db import login_user, create_user, is_user_exists
from reader import read_next_message, read_username_password, request_client_public_key
from writer import (
    send_msg,
    send_authentication_request,
    send_welcome_message,
    send_usage_information,
)
from constants import LOGIN_MESSAGE, SIGNUP_MESSAGE


def on_login_success(conn, user):
    send_welcome_message(conn, user, False)
    send_usage_information(conn)


def on_signup_success(conn, user):
    send_welcome_message(conn, user, True)
    send_usage_information(conn)


def try_login(conn):
    username, password = read_username_password(conn)
    user = login_user(username, password)

    if not user:
        return False, "invalid username or password"

    on_login_success(conn, user)
    return user, None


def try_signup(conn):
    username, password = read_username_password(conn)
    if is_user_exists(username):
        return False, "username already exists"

    pk = request_client_public_key(conn)
    new_user = create_user(username, password, pk)
    on_signup_success(conn, new_user)

    return new_user, None


def authenticate_user(conn):
    user, error = None, "error"

    while error:
        send_authentication_request(conn)
        auth_reply = read_next_message(conn)

        if auth_reply.lower() == LOGIN_MESSAGE:
            user, error = try_login(conn)
        elif auth_reply.lower() == SIGNUP_MESSAGE:
            user, error = try_signup(conn)
        else:
            error = "invalid authentication message"

        if error:
            send_msg(conn, f"Authentication error: {error}, try again!")

    return user

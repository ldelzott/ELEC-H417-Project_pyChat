from db import is_username_in_db, is_username_and_password_in_db, create_user
from reader import read_next_message, read_username_password
from writer import send_authentication_request, send_welcome_message, send_msg, send_hidden_public_key_request
from constants import LOGIN_MESSAGE, SIGNUP_MESSAGE


def on_login_success(conn, user):
    send_welcome_message(conn, user, False)


def on_signup_success(conn, user):
    send_welcome_message(conn, user, True)


def try_login(conn):

    username, password = read_username_password(conn)
    user_is_in_db, user = is_username_and_password_in_db(username, password)

    if not user_is_in_db:
        if not user:
            return False, "user not found in database"
        return False, "login error description"

    on_login_success(conn, user)
    return user, False


def try_signup(conn):
    username, password = read_username_password(conn)
    user_exists = is_username_in_db(username)
    if user_exists:
        return False, "username already exists"
    send_hidden_public_key_request(conn) # Will trigger the client to automatically retrieve his RSA key
    public_key = read_next_message(conn)
    new_user = create_user(username, password, public_key)
    on_signup_success(conn, new_user)
    return new_user, False


def authenticate_user(conn):
    user, error = None, "error"

    while error:
        send_authentication_request(conn)
        auth_msg = read_next_message(conn)
        if auth_msg.lower() == LOGIN_MESSAGE:
            user, error = try_login(conn)
        elif auth_msg.lower() == SIGNUP_MESSAGE:
            user, error = try_signup(conn)
        else:
            error = "invalid authentication message"

        if error:
            send_msg(conn, f"Authentication error: {error}, try again!")

    return user

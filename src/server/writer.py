from constants import FORMAT, HEADER, LOGIN_MESSAGE, SIGNUP_MESSAGE, DISCONNECT_MESSAGE


def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def send_authentication_request(conn):
    send_msg(conn, f'Please enter {LOGIN_MESSAGE} to login or {SIGNUP_MESSAGE} to signup')


def send_welcome_message(conn, user, is_new):
    if is_new:
        send_msg(conn, f'Welcome to the app, {user["username"]}!')
    else:
        send_msg(conn, f'Welcome back, {user["username"]}!')


def send_usage_information(conn):
    send_msg(conn, f'Type your message in the console, or {DISCONNECT_MESSAGE} to leave')


def send_username_request(conn):
    send_msg(conn, f'Type your username ([DEBUG-writer.py] try "dummy_username")')


def send_passphrase_request(conn):
    send_msg(conn, f'Type your passphrase([DEBUG-writer.py] try "pwd")')


def send_generic_error_incorrect_user_input(conn):
    send_msg(conn, f'Incorrect input type, try again')

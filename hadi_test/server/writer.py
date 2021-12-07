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
    send_msg(conn, f'Type any message to be sent to the server in the console..')
    send_msg(conn, f'type {DISCONNECT_MESSAGE} to disconnect anytime!')
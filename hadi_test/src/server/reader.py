from constants import HEADER, FORMAT, DISCONNECT_MESSAGE


def read_next_message(conn):
    message = None
    msg_length = conn.recv(HEADER).decode(FORMAT)

    if msg_length:
        msg_length = int(msg_length)
        message = conn.recv(msg_length).decode(FORMAT)
    else:
        raise Exception

    if message == DISCONNECT_MESSAGE:
        raise Exception

    return message


def read_username_password(conn):
    return 'dummy_username', 'pwd'
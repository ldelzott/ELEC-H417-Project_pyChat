from constants import HEADER, FORMAT, DISCONNECT_MESSAGE
from writer import (
    send_username_request,
    send_passphrase_request,
    send_hidden_public_key_request
)


def read_next_message(conn):
    message = None
    msg_length = conn.recv(HEADER).decode(FORMAT)

    if msg_length:
        msg_length = int(msg_length)
        message = conn.recv(msg_length).decode(FORMAT)
    else:
        raise Exception

    if message == DISCONNECT_MESSAGE:
        raise Exception("Client Disconnected")

    return message


def read_username(conn):
    send_username_request(conn)
    return read_next_message(conn)


def read_password(conn):
    send_passphrase_request(conn)
    return read_next_message(conn)


def read_username_password(conn):
    username = read_username(conn)
    password = read_password(conn)

    return username, password


def request_client_public_key(conn):
    send_hidden_public_key_request(conn)
    return read_next_message(conn)
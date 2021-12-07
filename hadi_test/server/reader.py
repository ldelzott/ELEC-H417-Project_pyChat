from constants import HEADER, FORMAT, DISCONNECT_MESSAGE
from writer import send_username_request, send_passphrase_request, send_generic_error_incorrect_user_input


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


# Looks like the Reader class doesn't have the full responsibility when reading
# user inputs : empty strings from the user seems to create errors in
# client.py | send() function (SSL doesn't agree with empty string ?)
def read_username_password(conn):

    send_username_request(conn)
    username = read_next_message(conn)
    send_passphrase_request(conn)
    password = read_next_message(conn)

    return username, password

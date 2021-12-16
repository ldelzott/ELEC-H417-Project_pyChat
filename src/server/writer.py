from constants import *


def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def send_authentication_request(conn):
    send_msg(conn, f'Please enter {LOGIN_MESSAGE} to login or {SIGNUP_MESSAGE} to signup\n')


def send_main_menu_command_list(conn):
    send_msg(conn, f'Please enter {PRINT_USER_COMMAND} to list all users or {START_SESSION} if you know the '
                   f'destination name.\n')


def send_destination_name_request(conn):
    send_msg(conn, f'Please enter the destination name. Use {BACK_COMMAND} for main menu.\n')


def send_user_list(conn, user_list):
    for user in user_list:
        send_msg(conn, f'{user["user"]}')


def send_user_blank_space(conn):
    send_msg(conn, f'\n')


def send_welcome_message(conn, user, is_new):
    if is_new:
        send_msg(conn, f'Welcome to the app, {user["user"]}!')
    else:
        send_msg(conn, f'Welcome back, {user["user"]}!')


def send_usage_information(conn):
    send_msg(conn, f'Type your messages in the console, or {DISCONNECT_MESSAGE} to leave at any moment\n')


def send_username_request(conn):
    send_msg(conn, f'Type your username ([DEBUG-writer.py] try "test")')


def send_passphrase_request(conn):
    send_msg(conn, f'Type your passphrase([DEBUG-writer.py] try "test")')


def send_generic_error_incorrect_user_input(conn):
    send_msg(conn, f'Incorrect input type, try again')


def send_back_info(conn):
    send_msg(conn, f'Type your messages in the console, or {BACK_COMMAND} to go to the name selection menu\n')


def send_debug(conn):
    send_msg(conn, "Debug message\n")


def send_new_conversation_creation_info(conn):
    send_msg(conn, f'Creation of a new conversation\n')


def send_message_from_conversation(conn, tuple):
    send_msg(conn, f'{tuple["user"]} - {tuple["date"]} :  {tuple["message"]}')
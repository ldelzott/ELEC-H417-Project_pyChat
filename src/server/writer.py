from constants import *


def send_msg(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def send_authentication_request(conn):
    send_msg(
        conn, f"Please enter {LOGIN_MESSAGE} to login or {SIGNUP_MESSAGE} to signup:\n"
    )


def send_main_menu_command_list(conn):
    send_msg(
        conn,
        f"Please enter {PRINT_USER_COMMAND} to list all users or {START_SESSION} if you know the "
        f"destination name.\n",
    )


def send_destination_name_request(conn):
    send_msg(
        conn, f"Please enter the destination name. Use {BACK_COMMAND} for main menu.\n"
    )


def send_user_list(conn, user_list):
    send_msg(conn, "users list:")
    for user in user_list:
        send_msg(conn, f'{user["username"]}')


def send_user_blank_space(conn):
    send_msg(conn, f"\n")


def send_welcome_message(conn, user, is_new):
    if is_new:
        send_msg(conn, f'\nWelcome to the app, {user["username"]}!')
    else:
        send_msg(conn, f'\nWelcome back, {user["username"]}!')


def send_usage_information(conn):
    send_msg(
        conn,
        f"Type your messages in the console, or {DISCONNECT_MESSAGE} to leave at any moment\n",
    )


def send_username_request(conn):
    send_msg(conn, f"Type your username:")


def send_passphrase_request(conn):
    send_msg(conn, f"Type your passphrase:")


def send_generic_error_incorrect_user_input(conn):
    send_msg(conn, f"Incorrect input type, try again:")


def send_back_command_info(conn):
    send_msg(
        conn,
        f"\nType your messages in the console, or {BACK_COMMAND} to go to the name selection menu\n",
    )


def send_debug(conn):
    send_msg(conn, "Debug message\n")


def send_new_conversation_creation_info(conn):
    send_msg(conn, f"Creation of a new conversation\n")


def send_message_from_conversation(conn, tuple):
    send_msg(conn, f'{tuple["date"][0:10]} ~ [{tuple["username"]}]:')
    send_msg(conn, f'{CRYPTED_CONTENT}{tuple["message"]}')


def send_hidden_public_key_request(conn):
    send_msg(conn, f"{GET_PUBLIC_KEY}")


def send_hidden_encrypted_AES_key_request(conn, dest_public_key):
    send_msg(conn, f"{CREATE_ENCR_AES_KEY}{dest_public_key}")


def send_conversation_id(conn, conversation_id):
    send_msg(conn, f"{SEND_CONVERSATION_ID}{conversation_id}")


def send_encrypted_key_to_user(conn, encrypted_aes_from_conversation_table):
    send_msg(conn, f"{SERVER_SEND_ENCRYPTED_AES_KEY}{encrypted_aes_from_conversation_table}")


def send_encryption_start_point(conn):
    send_msg(conn, f"{START_ENCRYPTION}")


def send_encryption_stop_point(conn):
    send_msg(conn, f"{STOP_ENCRYPTION}")

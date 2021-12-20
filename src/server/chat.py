from constants import *
from db.auth import list_users, is_user_exists, get_user_by_username
from db.chat import (
    is_user_tuple_in_conversations_db,
    create_new_conversation,
    insert_message_in_conversation_table,
    retrieve_conversation_id,
    retrieve_messages_from_conversation_id,
)
from reader import read_next_message
from writer import (
    send_msg,
    send_user_list,
    send_main_menu_command_list,
    send_destination_name_request,
    send_back_command_info,
    send_new_conversation_creation_info,
    send_message_from_conversation,
)


def print_user_list(conn):
    try:
        all_users = list_users()
        send_user_list(conn, all_users)
    except Exception as e:
        return e

    return None


def read_old_conversation(conn, conversation_id):
    tuples = retrieve_messages_from_conversation_id(conversation_id)
    for tuple in tuples:
        send_message_from_conversation(conn, tuple)


def start_chat_session(conn, user, dest_user):
    go_back = False
    if not is_user_tuple_in_conversations_db(dest_user["username"], user["username"]):
        create_new_conversation(user, dest_user)
        send_new_conversation_creation_info(conn)

    conversation_id = retrieve_conversation_id(user["username"], dest_user["username"])

    read_old_conversation(conversation_id)

    send_back_command_info(conn)

    while not go_back:
        message = read_next_message(conn)
        if message == BACK_COMMAND:
            go_back = True
            message = "SYSTEM : USER LOGOUT"

        insert_message_in_conversation_table(conversation_id, user, message)

    return None


def initialize_chat_session(conn, user):
    """
    User will pick a name to talk to.
    """

    go_back = False
    while not go_back:
        error = None, "error"
        while error:
            send_destination_name_request(conn)
            user_choice = read_next_message(conn)
            if user_choice == BACK_COMMAND:
                error = False
                go_back = True
            elif is_user_exists(user_choice):
                error = start_chat_session(
                    conn, user, get_user_by_username(user_choice)
                )
            else:
                error = "Invalid name or command\n"  # Could be cleaner

            if error:
                send_msg(conn, f"Request error: {error}, try again!\n")

    return False


def login_main_menu(conn, user):
    """
    Main menu for the user. User can choose to:
        - View all users
        - Start a conversation
    """

    error = None, "error"
    while error:
        send_main_menu_command_list(conn)
        user_choice = read_next_message(conn)

        if user_choice == PRINT_USER_COMMAND:
            error = print_user_list(conn)
        elif user_choice == START_SESSION:
            error = initialize_chat_session(conn, user)
        else:
            error = "this request does not exist"

        if error:
            send_msg(conn, f"Request error: {error}, try again!\n")

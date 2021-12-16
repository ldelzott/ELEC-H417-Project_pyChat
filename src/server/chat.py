from src.server.constants import *
from src.server.db import db_user_print, is_username_in_db, is_user_tuple_in_conversations_db, get_user, \
    create_new_conversation, insert_message_in_conversation_table, retrieve_conversation_id, \
    retrieve_messages_from_conversation_id
from src.server.reader import read_next_message
from src.server.writer import send_msg, send_user_list, \
    send_main_menu_command_list, send_destination_name_request, send_back_info, \
    send_new_conversation_creation_info, send_message_from_conversation


def print_user_list(conn):
    user_list = db_user_print()
    send_user_list(conn, user_list)
    return False


def read_old_conversation(conn, user, dest_user):
    conversation_id = retrieve_conversation_id(user["user"], dest_user["user"])
    tuples = retrieve_messages_from_conversation_id(conversation_id)
    for tuple in tuples:
        send_message_from_conversation(conn, tuple)


def start_chat_session(conn, user, dest_user):
    go_to_name_menu = False
    if not is_user_tuple_in_conversations_db(dest_user["user"], user["user"]):
        create_new_conversation(user, dest_user)
        send_new_conversation_creation_info(conn)

    conversation_id = retrieve_conversation_id(user["user"], dest_user["user"]);
    read_old_conversation(conn, user, dest_user)
    send_back_info(conn)
    while not go_to_name_menu:
        user_choice = read_next_message(conn)
        insert_message_in_conversation_table(conversation_id, user, user_choice)
        if user_choice == BACK_COMMAND:
            insert_message_in_conversation_table(conversation_id, user, "SYSTEM : USER LOGOUT")
            go_to_name_menu = True

    return False


def initialize_chat_session(conn, user):
    go_to_main_menu = False
    while not go_to_main_menu:
        error = None, "error"
        while error:
            send_destination_name_request(conn)
            user_choice = read_next_message(conn)
            if user_choice == BACK_COMMAND:
                error = False
                go_to_main_menu = True
            elif is_username_in_db(user_choice):
                error = start_chat_session(conn, user, get_user(user_choice))
            else:
                error = "Invalid name or command\n"  # Could be cleaner
            if error:
                send_msg(conn, f"Request error: {error}, try again!\n")
    return False


def login_main_menu(conn, user):
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

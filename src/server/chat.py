from constants import *
from db.auth import list_users, is_user_exists, get_user_by_username
from db.chat import (
    initialize_new_conversation,
    insert_conversation_message,
    retrieve_conversation_id,
    get_messages_by_conversation_id,
    get_user_mailbox,
    update_user_mailbox,
    clear_mailbox,
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
import active_users


def print_user_list(conn):
    all_users = list_users()
    send_user_list(conn, all_users)

    return None


def send_the_conversation(conn, conversation_id):
    messages = get_messages_by_conversation_id(conversation_id)
    for message in messages:
        send_message_from_conversation(conn, message)


def send_conversation_message(conversation_id, user, user_dest, message):
    msg_tuple = insert_conversation_message(conversation_id, user, message)

    dest_conn = is_peer_talking_to_me(user["username"], user_dest["username"])

    if dest_conn:
        send_message_from_conversation(dest_conn, msg_tuple)
    else:
        update_user_mailbox(user_dest["username"], user["username"])


def is_peer_talking_to_me(me_username, peer_username):
    if not peer_username in active_users.get_active_users():
        return None

    peer_status = active_users.get_active_users()[peer_username]
    if peer_status["talking_to"] == me_username:
        return peer_status["conn"]

    else:
        return None


def start_chat_session(conn, user, user_dest):
    active_users.update(
        user["username"], {"screen": CHAT_SCREEN, "talking_to": user_dest["username"]}
    )
    clear_mailbox(user["username"], user_dest["username"])

    go_back = False

    conversation_id = retrieve_conversation_id(user["username"], user_dest["username"])
    if not conversation_id:
        conversation_id = initialize_new_conversation(user, user_dest)
        send_new_conversation_creation_info(conn)

    send_the_conversation(conn, conversation_id)
    send_back_command_info(conn)

    while not go_back:
        message = read_next_message(conn)
        if message == BACK_COMMAND:
            go_back = True
            message = f"SYSTEM: {user['username']} LEFT"

        send_conversation_message(conversation_id, user, user_dest, message)

    active_users.update(user["username"], {"screen": MAIN_SCREEN, "talking_to": None})

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
            elif user_choice == user["username"]:
                error = "You can't talk to yourself"
            elif is_user_exists(user_choice):
                error = start_chat_session(
                    conn, user, get_user_by_username(user_choice)
                )
            else:
                error = "Invalid name or command\n"  # Could be cleaner

            if error:
                send_msg(conn, f"Request error: {error}, try again!\n")

    return None


def send_mailbox_summary(conn, user):
    mailbox = get_user_mailbox(user["username"])

    if len(mailbox) == 0:
        return send_msg(conn, "You have no new messages\n")
    for record in mailbox:
        send_msg(conn, f"{record['sender']} sent you {record['count']} message\n")


def login_main_menu(conn, user):
    """
    Main menu for the user. User can choose to:
        - View all users
        - Start a conversation with a picked user
    """

    active_users.update(user["username"], {"screen": MAIN_SCREEN})
    send_mailbox_summary(conn, user)

    error = None, "error"
    while error:
        send_main_menu_command_list(conn)
        user_choice = read_next_message(conn)

        if user_choice == PRINT_USER_COMMAND:
            error = print_user_list(conn)
        elif user_choice == START_SESSION:
            error = initialize_chat_session(conn, user)
        else:
            error = "invalid command"

        if error:
            send_msg(conn, f"Request error: {error}, try again!\n")

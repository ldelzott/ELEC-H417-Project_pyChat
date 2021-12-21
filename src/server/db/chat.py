from tinydb import Query
from datetime import datetime
from db import retrieve_db_access
from uuid import uuid4


def get_conversation_info_table():
    conversation_info_table = retrieve_db_access().table("conversation_info")
    return conversation_info_table, Query()


def get_conversation_id_table(conversation_id):
    conversation_id_table = retrieve_db_access().table(conversation_id)
    return conversation_id_table, Query()


def get_mailbox_table():
    mailbox_table = retrieve_db_access().table("mailbox")
    return mailbox_table, Query()


def initialize_new_conversation(user_init, user_dest, encr_aes_key):
    conversation_id = create_new_conversation(user_init, user_dest, encr_aes_key)
    insert_conversation_message(conversation_id, user_init, "Conversation started")
    return conversation_id


def create_new_conversation(user_init, user_dest, encr_aes_key):
    conversation_info, _ = get_conversation_info_table()
    encrypted_symmetric_key = encr_aes_key
    conversation_id = user_init["username"] + user_dest["username"]
    conversation_info.insert(
        {
            "user1": user_init["username"],
            "user2": user_dest["username"],
            "conversation_id": conversation_id,
            "encr_aeskey": encrypted_symmetric_key,
        }
    )

    return conversation_id


def retrieve_conversation_id(username1, username2):
    conversation_info, query = get_conversation_info_table()
    result = conversation_info.search(
        ((query.user1 == username1) & (query.user2 == username2))
        | ((query.user1 == username2) & (query.user2 == username1))
    )

    if len(result) == 0:
        return None

    return result[0]["conversation_id"]


def get_messages_by_conversation_id(conversation_id):
    conversation_list, _ = get_conversation_id_table(conversation_id)
    return conversation_list.all()


def insert_conversation_message(conversation_id, user, message):
    conversation_data, _ = get_conversation_id_table(conversation_id)
    new_message = {
        "id": str(uuid4()),
        "username": user["username"],
        "message": message,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seen": False,
    }
    conversation_data.insert(new_message)
    return new_message


def update_user_mailbox(receiver_username, sender_username):
    mailbox_table, query = get_mailbox_table()
    result = mailbox_table.search(
        (query.receiver == receiver_username) & (query.sender == sender_username)
    )

    if len(result) == 0:
        create_mailbox_record(sender_username, receiver_username)
    else:
        increment_mailbox_count(receiver_username, sender_username)


def create_mailbox_record(sender_username, receiver_username):
    mailbox_table, _ = get_mailbox_table()
    mailbox_table.insert(
        {"receiver": receiver_username, "sender": sender_username, "count": 1}
    )


def increment_mailbox_count(receiver_username, sender_username):
    mailbox_table, query = get_mailbox_table()
    mailbox_table.update(
        {
            "count": mailbox_table.get(
                (query.receiver == receiver_username)
                & (query.sender == sender_username)
            )["count"]
            + 1
        },
        (query.receiver == receiver_username) & (query.sender == sender_username),
    )


def get_user_mailbox(username):
    mailbox_table, query = get_mailbox_table()
    return mailbox_table.search(query.receiver == username)


def clear_mailbox(receiver_username, sender_username):
    mailbox_table, query = get_mailbox_table()
    mailbox_table.remove(
        (query.receiver == receiver_username) & (query.sender == sender_username)
    )

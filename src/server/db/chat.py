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


def initialize_new_conversation(user_init, user_dest):
    conversation_id = create_new_conversation(user_init, user_dest)
    send_conversation_message(conversation_id, user_init, "Conversation started")
    return conversation_id


def create_new_conversation(user_init, user_dest):
    conversation_info, _ = get_conversation_info_table()
    encrypted_symmetric_key = "encrypted_aes_key_using_user_destination_public_key"
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


def send_conversation_message(conversation_id, user, message):
    conversation_data, _ = get_conversation_id_table(conversation_id)
    conversation_data.insert(
        {
            "id": str(uuid4()),
            "username": user["username"],
            "message": message,
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "seen": False,
        }
    )

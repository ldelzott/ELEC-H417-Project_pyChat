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


def insert_message_in_conversation_table(conversation_id, user, message):
    conversation_data = get_conversation_id_table(conversation_id)
    conversation_data.insert(
        {
            "id": uuid4(),
            "username": user["username"],
            "message": message,
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "seen": False,
        }
    )


def create_new_conversation(user_initiator, user_destination):
    conversation_info, _ = get_conversation_info_table()
    encrypted_symmetric_key = "encrypted_aes_key_using_user_destination_public_key"
    conversation_id = user_initiator["username"] + user_destination["username"]
    conversation_info.insert(
        {
            "user1": user_initiator["username"],
            "user2": user_destination["username"],
            "conversation_id": conversation_id,
            "encr_aeskey": encrypted_symmetric_key,
        }
    )
    insert_message_in_conversation_table(
        conversation_id, user_initiator, "Conversation start"
    )


def retrieve_conversation_id(username1, username2):
    conversation_info, query = get_conversation_info_table()
    conversation_id = conversation_info.search(
        ((query.user1 == username1) & (query.user2 == username2))
        | ((query.user1 == username2) & (query.user2 == username1))
    )[0]["conversation_id"]

    return conversation_id


def retrieve_messages_from_conversation_id(conversation_id):
    conversation_list, _ = get_conversation_id_table(conversation_id)
    return conversation_list.all()


# The pair (user1, user2) is assumed to be equivalent to the pair (user2, user1) when storing / searching for messages
def is_user_tuple_in_conversations_db(user1, user2):
    conversation_info, query = get_conversation_info_table()
    return conversation_info.contains(
        ((query.user1 == user1) & (query.user2 == user2))
        | ((query.user1 == user2) & (query.user2 == user1))
    )

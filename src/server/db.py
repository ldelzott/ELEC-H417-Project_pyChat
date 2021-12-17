import bcrypt
from crypto_utils import hash_pwd
from tinydb import TinyDB, Query
import datetime


def retrieve_db_access():
    try:
        db = TinyDB('data/db.json')
    except:
        print("An error occurred on a database transaction. Exiting...")
        exit()

    authTable = db.table('authTable')
    query = Query()

    return db, authTable, query


def insert_message_in_conversation_table(conversation_id, user, message):
    db, _, query = retrieve_db_access()
    conversation_data = db.table(conversation_id)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    conversation_data.insert({'date': timestamp, 'user': user["user"], 'seen': False, 'message': message})


def create_new_conversation(user_initiator, user_destination):
    db, _, query = retrieve_db_access()
    conversation_info = db.table('conversation_info')
    encrypted_symmetric_key = "encrypted_aes_key_using_user_destination_public_key"
    conversation_id = user_initiator["user"] + user_destination["user"]
    conversation_info.insert({'user1': user_initiator["user"], 'user2': user_destination["user"],
                              'conversation_id': conversation_id, 'encr_aeskey': encrypted_symmetric_key})
    insert_message_in_conversation_table(conversation_id, user_initiator, "Conversation start")


def retrieve_conversation_id(username1, username2):
    db, _, query = retrieve_db_access()
    conversation_info = db.table('conversation_info')
    conversation_id = conversation_info.search(((query.user1 == username1) & (query.user2 == username2)) | (
            (query.user1 == username2) & (query.user2 == username1)))[0]["conversation_id"]
    print(conversation_id)
    return conversation_id


def retrieve_messages_from_conversation_id(conversation_id):
    db, _, query = retrieve_db_access()
    conversation_list = db.table(conversation_id)
    return conversation_list.all()


def db_user_print():
    _, authTable, query = retrieve_db_access()
    return authTable.all()


# The pair (user1, user2) is assumed to be equivalent to the pair (user2, user1) when storing / searching for messages
def is_user_tuple_in_conversations_db(user1, user2):
    db, _, query = retrieve_db_access()
    conversations_table = db.table('conversation_info')
    return conversations_table.contains(
        (query.user1 == user1) & (query.user2 == user2)) or conversations_table.contains(
        (query.user1 == user2) & (query.user2 == user1))


def is_username_in_db(username):
    _, authTable, query = retrieve_db_access()
    return authTable.contains(query.user == username)


# db_tuple is a list of dict(s). The dict(s) in this list are the resulting tuples from the query.
# The second tuple with the same user value will be ignored : only the first tuple will be considered.
def is_username_and_password_in_db(username, pwd):
    _, authTable, query = retrieve_db_access()
    db_tuple = authTable.search(query.user == username)

    if len(db_tuple) == 0:
        return False, None

    check_value = bcrypt.checkpw(pwd.encode("utf-8"), db_tuple[0]["hpassword"].encode("utf-8"))
    return check_value, db_tuple[0]


def get_user(username):
    _, authTable, query = retrieve_db_access()
    return authTable.search(query.user == username)[0]


def create_user(username, pwd, public_key):
    encoded_hashed_pwd = hash_pwd(pwd)
    _, authTable, query = retrieve_db_access()
    if is_username_in_db(username):
        return False, "the username is already in the database"
        exit()
    authTable.insert({'user': username, 'hpassword': encoded_hashed_pwd.decode(), 'rsa_public': public_key})
    return authTable.search(query.user == username)[0]

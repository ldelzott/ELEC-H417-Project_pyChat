from crypto_utils import hash_pwd
from tinydb import TinyDB, Query


def retrieve_db_access():
    try:
        db = TinyDB('data/db.json')
    except:
        print("An error occurred on a database transaction. Exiting...")
        exit()

    authTable = db.table('authTable')
    query = Query()

    return db, authTable, query


def is_username_in_db(username):
    _, authTable, query = retrieve_db_access()
    return authTable.contains(query.user == username)


def is_username_and_password_in_db(username, pwd):
    hashed_pwd = hash_pwd(pwd)
    _, authTable, query = retrieve_db_access()
    return authTable.contains((query.user == username) & (query.hpassword == hashed_pwd))


def create_user(username, pwd):
    hashed_pwd = hash_pwd(pwd)
    _, authTable, query = retrieve_db_access()
    if is_username_in_db(username):
        return False, "the username is already in the database"
        exit()
    else:
        authTable.insert({'user': username, 'hpassword': hashed_pwd})
    return username

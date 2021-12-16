import bcrypt

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

# db_tuple is a list of dict(s). The dict(s) in this list are the resulting tuples from the query.
def is_username_and_password_in_db(username, pwd):
    _, authTable, query = retrieve_db_access()
    db_tuple = authTable.search(query.user == username)
    check_value = bcrypt.checkpw(pwd.encode("utf-8"), db_tuple[0]["hpassword"].encode("utf-8"))
    return check_value


def create_user(username, pwd):
    encoded_hashed_pwd = hash_pwd(pwd)
    _, authTable, query = retrieve_db_access()
    if is_username_in_db(username):
        return False, "the username is already in the database"
        exit()
    else:
        authTable.insert({'user': username, 'hpassword': encoded_hashed_pwd.decode()})
    return username

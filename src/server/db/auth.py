from tinydb import Query
from db import retrieve_db_access
from crypto_utils import hash_pwd, compare_pwd


def get_users_table():
    db = retrieve_db_access()
    users_table = db.table("users")

    return users_table, Query()


def list_users():
    users, _ = get_users_table()
    return users.all()


def is_user_exists(username):
    users, query = get_users_table()
    return users.contains(query.user == username)


def login_user(username, pwd):
    users, query = get_users_table()
    result = users.search(query.user == username)

    if len(result) == 0:
        return None
    if compare_pwd(pwd, result[0]["hpassword"]):
        return result[0]

    return None


def get_user_by_username(username):
    users, query = get_users_table()
    return users.search(query.user == username)[0]


def create_user(username, pwd, public_key):
    users, query = get_users_table()
    encoded_hashed_pwd = hash_pwd(pwd)

    users.insert(
        {
            "username": username,
            "hpassword": encoded_hashed_pwd.decode(),
            "rsa_public": public_key,
        }
    )

    return users.search(query.user == username)[0]

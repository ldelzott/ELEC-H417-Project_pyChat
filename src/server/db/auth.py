from db import retrieve_db_access
from crypto_utils import hash_pwd, compare_pwd


def is_user_exists(username):
    _, authTable, query = retrieve_db_access()
    return authTable.contains(query.user == username)


def login_user(username, pwd):
    _, authTable, query = retrieve_db_access()
    result = authTable.search(query.user == username)

    if len(result) == 0:
        return None

    if compare_pwd(pwd, result[0]["hpassword"]):
        return result[0]

    return None


def get_user_by_username(username):
    _, authTable, query = retrieve_db_access()
    return authTable.search(query.user == username)[0]


def create_user(username, pwd, public_key):
    encoded_hashed_pwd = hash_pwd(pwd)
    _, authTable, query = retrieve_db_access()

    authTable.insert(
        {
            "user": username,
            "hpassword": encoded_hashed_pwd.decode(),
            "rsa_public": public_key,
        }
    )

    return authTable.search(query.user == username)[0]

from constants import DUMMY_USER
from crypto_utils import hash_pwd


def find_user_by_username(username):
    # db call to find existing username
    return False


def find_user_by_username_and_pwd(username, password):
    hashed_pwd = hash_pwd(password)

    # select from database where username = username and pwd = hashed_pwd

    return DUMMY_USER



def create_user(username, pwd):
    hashed_pwd = hash_pwd(pwd)

    # add the user to the db
    return DUMMY_USER
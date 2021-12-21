from tinydb import TinyDB, Query
from db.init_database import db_path


def retrieve_db_access():
    try:
        db = TinyDB(db_path)
    except:
        print("An error occurred on a database transaction. Exiting...")
        exit()

    return db

from tinydb import TinyDB, Query


def retrieve_db_access():
    try:
        db = TinyDB("data/db.json")
    except:
        print("An error occurred on a database transaction. Exiting...")
        exit()

    authTable = db.table("authTable")
    query = Query()

    return db, authTable, query

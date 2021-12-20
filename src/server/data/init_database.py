from tinydb import TinyDB
import os


db_path = os.path.join(os.path.dirname(__file__), "db.json")


def delete_db():
    if os.path.exists(db_path):
        os.remove(db_path)


def inti_db():
    TinyDB(db_path)


if __name__ == "__main__":
    delete_db()
    inti_db()

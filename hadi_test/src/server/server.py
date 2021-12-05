import socket
import threading

from constants import PORT
from auth import authenticate_user
from reader import read_next_message
from writer import send_usage_information


SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def receive_messages_loop(conn, user):
    while True:
        message = read_next_message(conn)
        print(f'{user["username"]}: {message}')


def handle_client(conn):
    try:
        user = authenticate_user(conn)
        send_usage_information(conn)
        receive_messages_loop(conn, user)
    except Exception:
        pass
    finally:
        conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[CONNECTION] {addr} connected.")
        threading.Thread(target=handle_client, args=(conn, )).start()


start()

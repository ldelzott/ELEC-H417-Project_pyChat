import socket
import threading

from constants import SERVER_HOST_NAME, SERVER_PORT
from auth import authenticate_user
from ssl_wrapper import make_ssl_server_socket
from reader import read_next_message
from writer import send_usage_information

server = make_ssl_server_socket()

def receive_messages_loop(conn, user):
    while True:
        message = read_next_message(conn)
        print(f'{user["username"]}: {message}')


def handle_client(conn):
    try:
        user = authenticate_user(conn)
        send_usage_information(conn)
        receive_messages_loop(conn, user)
    except Exception as e:
        print(f"[EXCEPTION CAUGHT]: {e}")
    finally:
        conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_HOST_NAME}:{SERVER_PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[CONNECTION] {addr} connected.")
        threading.Thread(target=handle_client, args=(conn, )).start()


start()

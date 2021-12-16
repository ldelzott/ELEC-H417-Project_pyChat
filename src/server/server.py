import threading
from auth import authenticate_user
from chat import login_main_menu
from ssl_wrapper import make_ssl_server_socket
from reader import read_next_message
from writer import send_usage_information
from constants import SERVER_HOST_NAME, SERVER_PORT

# Use local private key and certificate to create make a ssl socket
server = make_ssl_server_socket()


def receive_messages_loop(conn, user):
    while True:
        login_main_menu(conn, user)


def handle_client(conn, addr):
    try:
        user = authenticate_user(conn)
        send_usage_information(conn)
        receive_messages_loop(conn, user)
    except Exception as e:
        print(f"[EXCEPTION CAUGHT]: client: {addr} -- {e}")
    finally:
        conn.close()


def handle_connections():
    while True:
        conn, addr = server.accept()
        print(f"[CONNECTION] {addr} connected.")
        threading.Thread(target=handle_client, args=(conn, addr)).start()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_HOST_NAME}:{SERVER_PORT}")
    handle_connections()


start()

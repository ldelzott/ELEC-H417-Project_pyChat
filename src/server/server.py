import threading
from ssl_wrapper import make_ssl_server_socket
from auth import authenticate_user
from chat import login_main_menu
from constants import SERVER_HOST_NAME, SERVER_PORT, MAIN_SCREEN
import active_users

active_users.init()

# Use local private key and certificate to create make a ssl socket
server = make_ssl_server_socket()


def receive_messages_loop(conn, user):
    while True:
        login_main_menu(conn, user)


def handle_client(conn, addr):
    user = None
    try:
        user = authenticate_user(conn)
        active_users.register(user["username"], conn)
        receive_messages_loop(conn, user)
    except Exception as e:
        print(f"[EXCEPTION CAUGHT]: client: {addr} -- {e}")
        # raise e  # just in dev, so we can see where is the error
    finally:
        print(f"[CONNECTION] {addr} disconnected.")
        active_users.unregister(user)
        conn.close()
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

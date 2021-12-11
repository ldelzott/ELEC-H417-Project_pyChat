import threading
from writer import send_msg
from ssl_wrapper import make_ssl_client_socket
from constants import SERVER_HOST_NAME, SERVER_PORT, HEADER, FORMAT

ADDR = (SERVER_HOST_NAME, SERVER_PORT)

client = make_ssl_client_socket()


def listen_to_user_loop():
    while True:
        try:
            message = input("> ")
            if message == "":
                print("[ALERT]: Empty message ignored")
                continue

            send_msg(client, message)

        except Exception:
            client.close()
            break


def listen_to_server_loop():
    while True:
        message_header = client.recv(HEADER)
        if not len(message_header):
            print("Connection closed by the server, please close the program")
            client.close()
            return

        message_length = int(message_header.decode(FORMAT))
        message = client.recv(message_length).decode(FORMAT)
        print(f"[SERVER]: {message}")


def start():
    client.connect(ADDR)
    threading.Thread(target=listen_to_user_loop).start()
    threading.Thread(target=listen_to_server_loop).start()


start()

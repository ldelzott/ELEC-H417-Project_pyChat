import threading
from writer import send_msg
from ssl_wrapper import make_ssl_client_socket
from constants import SERVER_HOST_NAME, SERVER_PORT, HEADER, FORMAT, GET_PUBLIC_KEY, GET_ENCR_AES_KEY
from symmetric_crypto import create_encrypted_symmetric_key
from asymmetric_crypto import (
    get_rsa_private_key,
    get_rsa_public_key,
    rsa_encrypt,
    rsa_decrypt,
    get_rsa_storable_public_key,
)

ADDR = (SERVER_HOST_NAME, SERVER_PORT)
client = make_ssl_client_socket()


def listen_to_user_loop():
    while True:
        try:
            message = input("")
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
        if message == GET_PUBLIC_KEY:
            send_msg(client, get_rsa_storable_public_key())
            message = ""  # To avoid diplaying the command !GETRSA on the user screen when signup
        if message[0:11] == GET_ENCR_AES_KEY:
            send_msg(client, create_encrypted_symmetric_key(message[11:]))
        else:
            print(f"{message}")


def start():
    client.connect(ADDR)
    threading.Thread(target=listen_to_user_loop).start()
    threading.Thread(target=listen_to_server_loop).start()


start()

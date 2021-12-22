import threading
from queue import Queue
from writer import send_msg
from ssl_wrapper import make_ssl_client_socket
from constants import *
from symmetric_crypto import create_encrypted_symmetric_key, encryption_using_AES_key, byte_to_base64_string, check_for_existing_local_key, decryption_using_AES_key, base64_string_to_byte
from asymmetric_crypto import (
    get_rsa_private_key,
    get_rsa_public_key,
    rsa_encrypt,
    rsa_decrypt,
    get_rsa_storable_public_key,
)

ADDR = (SERVER_HOST_NAME, SERVER_PORT)
client = make_ssl_client_socket()


def listen_to_user_loop(out_pipe):
    encryption_on = False
    conversation_id = ""
    while True:
        try:
            message = input("")
            if message == "":
                print("[ALERT]: Empty message ignored")
                continue
            if not out_pipe.empty():
                pipe_content = out_pipe.get()
                if pipe_content == NO_ENCRYPTION:
                    encryption_on = False
                else:
                    conversation_id = pipe_content
                    encryption_on = True
            if encryption_on and not message == BACK_COMMAND:
                message = byte_to_base64_string(encryption_using_AES_key(message, conversation_id))

            send_msg(client, message)

        except Exception:
            client.close()
            break


def listen_to_server_loop(in_pipe):
    conversation_id = ""
    received_encrypted_aes = ""
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
            message = ""
        if message[0:11] == CREATE_ENCR_AES_KEY:
            send_msg(client, create_encrypted_symmetric_key(message[11:], conversation_id)) # Used when the current user initiate a new conversation with a new peer.
            message = ""                                                                    # The current user will uses the public RSA key of the peer to encrypt
        if message[0:10] == SEND_CONVERSATION_ID:                                           # the new AES key that will be used to encrypt/decrypt the new conversation.
            conversation_id = message[10:]
            message = ""
        if message[0:14] == SERVER_SEND_ENCRYPTED_AES_KEY: # If a secret key doesn't exit locally, this means that the AES key was encrypted by the other user, using the public RSA key of the current user
            received_encrypted_aes = message[14:]
            check_for_existing_local_key(conversation_id, received_encrypted_aes)
            message = ""
        if message == START_ENCRYPTION:
            in_pipe.put(conversation_id)
            message=""
        if message == STOP_ENCRYPTION:
            in_pipe.put(NO_ENCRYPTION)
            message=""
        if message[0:13] == CRYPTED_CONTENT:
            message = decryption_using_AES_key(base64_string_to_byte(message[13:]), conversation_id)
            print(message.decode('utf-8'))
        else:
            print(f"{message}")


def start():
    pipe = Queue()
    client.connect(ADDR)
    threading.Thread(target=listen_to_user_loop, args=(pipe, )).start()
    threading.Thread(target=listen_to_server_loop, args=(pipe, )).start()


start()

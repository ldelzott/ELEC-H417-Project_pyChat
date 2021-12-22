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
    """
        The client will react to messages coming from the server.
        Some message contains a prefix part: this prefix allows to trigger
        specific behaviors on the client side while keeping to code relatively compact.

        The 'GET_PUBLIC_KEY' prefix allows the server to retrieve the public RSA key of the client when he signup

        The 'CREATE_ENCR_AES_KEY' prefix will generate a (new) random AES key on client side. This key is encrypted
        using the public RSA key that follows the prefix.

        The 'SEND_CONVERSATION_ID' prefix allows the client to store the ID of the current conversation : this ID is
        helpful for the client to identify the AES secret key he needs to use in the decryption process.

        The 'SERVER_SEND_ENCRYPTED_AES_KEY' prefix will be used by the client that doesn't initiate the conversation.
        This client will not have yet a local AES secret key locally and needs to use his private RSA key to generate it

        The 'START_ENCRYPTION' and 'STOP_ENCRYPTION' prefixes uses a 'pipe' between the two python threads created
        in the start() function. This pipe allows to trigger the encryption of the chat messages that are send to
        the server in listen_to_user_loop() function.

        The 'CRYPTED_CONTENT' prefix is used by the server to tag encrypted messages.
        """
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
            send_msg(client, create_encrypted_symmetric_key(message[11:], conversation_id))
            message = ""
        if message[0:10] == SEND_CONVERSATION_ID:
            conversation_id = message[10:]
            message = ""
        if message[0:14] == SERVER_SEND_ENCRYPTED_AES_KEY:
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

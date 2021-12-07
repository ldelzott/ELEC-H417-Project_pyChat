import threading
from ssl_wrapper import make_ssl_client_socket
from constants import SERVER_HOST_NAME, SERVER_PORT, HEADER, FORMAT

ADDR = (SERVER_HOST_NAME, SERVER_PORT)

client = make_ssl_client_socket()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    try:
        client.send(send_length)
        client.send(message)
    except ConnectionAbortedError:
        client.close()


def listen_to_user():
    while True:
        #take input from the user
        message = input("> ")
        send(message)


def listen_to_server():
    while True:
        #listen to the server
        message_header = client.recv(HEADER)
        if not len(message_header):
            print("Connection closed by the server, please close the program")
            client.close()
            return
        message_length = int(message_header.decode(FORMAT))
        message = client.recv(message_length).decode(FORMAT)
        print(f'[SERVER]: {message}')


def start():
    client.connect(ADDR)
    threading.Thread(target=listen_to_user).start()
    threading.Thread(target=listen_to_server).start()


start()
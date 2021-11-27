import threading
import socket

host = '127.0.0.1'

port = 56000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)  # 1024 is the max number of byte the server can receive from a client
            broadcast(message)
        except:
            index = clients.index(
                client)  # Index will return the position of the tuple of the clients list that correspond the value 'client'
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the room!'.encode(
                'utf-8'))  # "Encode" (and "decode") is used to convert to 'bytes' the sended/received content
            aliases.remove(alias)
            break


def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()

        print(
            f'connection is established with {str(address)}')  # str casting since one cannot concatenate string with integer in python
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat rooms'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive()







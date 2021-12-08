# The code should run properly on windows 11
# The current code is based on : https://www.youtube.com/watch?v=nmzzeAvQHp8


# When closing and re-opening the current script, the following
# error can appear :

# Traceback (most recent call last):
#   File "server.py", line 22, in <module>
#     server.bind((host, port))
# OSError: [WinError 10048] Une seule utilisation de chaque adresse de socket (protocole/adresse r▒seau/port) est habituellement autoris▒e

# The command 'netstat -ano|findstr PORT_NUMBER' can be used to determine the process ID
# that uses the specified PORT_NUMBER.
# The command 'taskkill /F /PID PID_NUMBER' can be used to release the corresponding PORT_NUMBER.
# Use 'taskkill /?' for help.

import threading
import socket

host = '127.0.0.1'
# Standard loopback interface address : this means that only process that runs on the host
# will eventually by able to connect to the server we create here. If an empty string is given
# instead of the loopback address, the server should accept connections on all available IPv4
# interfaces

port = 59000
# Number of the port to listen. Should be an integer between 1 and 65535.
# In some cases, usage of port number < 1024 could require super-user privilege.
# This port number cannot be taken yet by another application : run command 'netstat'
# to display current used port. A list of 'reserved' port number are available on
# wikipedia : https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Here, 'AF.INET' refer to the address family of IPv4 and 'SOCK_STREAM' is the socket type
# that correspond to TCP.
# Those infos were given on this link : https://realpython.com/python-sockets/

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
            message = client.recv(1024) # 1024 is the max number of byte the server can receive from a client
            broadcast(message)
        except:
            index = clients.index(client) # Index will return the position of the tuple of the clients list that correspond the value 'client'
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the room!'.encode('utf-8')) # "Encode" (and "decode") is used to convert to 'bytes' the sended/received content
            aliases.remove(alias)
            break

def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept() # Accept method is running constantly on the server
                                          # and wait for any connections from any client
                                          # return a socket representing the connection (?)
                                          # and the address of the client

        print(f'connection is established with {str(address)}') #str casting since one cannot concatenate string with integer in python
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







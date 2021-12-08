import socket, ssl, os
from constants import SERVER_HOST_NAME, SERVER_PORT

cert_file = os.path.join(os.path.dirname(__file__), "..", "..", "ssl/localhost.pem")
key_file = os.path.join(os.path.dirname(__file__), "..", "..", "ssl/localhost.key")


def make_ssl_server_socket():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind((SERVER_HOST_NAME, SERVER_PORT))
    sock.listen(5)

    return context.wrap_socket(sock, server_side=True)

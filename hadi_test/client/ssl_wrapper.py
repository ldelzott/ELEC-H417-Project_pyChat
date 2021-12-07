import socket, ssl, os
from constants import SERVER_HOST_NAME

cert_file = os.path.join(os.path.dirname(__file__), '..', 'ssl/localhost.pem')

def make_ssl_client_socket():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cert_file)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    return context.wrap_socket(sock, server_hostname=SERVER_HOST_NAME)

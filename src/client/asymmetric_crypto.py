# https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
# https://stackoverflow.com/questions/65597453/how-to-store-private-and-public-key-into-pem-file-generated-by-rsa-module-of-pyt
# https://stackoverflow.com/questions/65230554/cannot-decode-encrypted-rsa-message-python3

import os
import rsa
import base64

# This file contains functions for RSA keys management as well as encryption and decryption processes.


def generate_rsa_key_pair():
    """
    Each client have both a private and a public RSA key stored locally.
    That key pair will be generated only once if the corresponding files are not created yet.
    """
    publicKey, privateKey = rsa.newkeys(1024)
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8')
    privateKeyPkcs1PEM = privateKey.save_pkcs1().decode('utf8')

    if not os.path.exists("./keys"):
        os.mkdir("./keys")

    with open("keys/private_rsa.pem", "w") as file:
        file.write(privateKeyPkcs1PEM)

    with open("keys/public_rsa.pub", "w") as file:
        file.write(publicKeyPkcs1PEM)


def get_rsa_public_key():

    if not os.path.exists("keys/public_rsa.pub"):
        generate_rsa_key_pair()

    f = open("keys/public_rsa.pub", "r")
    public_key = rsa.PublicKey.load_pkcs1(f.read().encode('utf-8'))
    return public_key


def get_rsa_storable_public_key():
    """
    The database system used by the server (TinyDB) relies on .JSON files that doesn't accept serialized data.
    Thus, particular processing needs to be done prior to any storage in the DB. The conversion used in this
    project relies on the base64 library. This library allows for easy conversions between 'bytes' and 'strings'.
    """
    return get_rsa_public_key().save_pkcs1().decode('utf-8')


def get_rsa_private_key():
    if not os.path.exists("keys/private_rsa.pem"):
        generate_rsa_key_pair()

    f = open("keys/private_rsa.pem", "r")
    private_key = rsa.PrivateKey.load_pkcs1(f.read().encode('utf-8'))
    return private_key


def get_rsa_storable_private_key():
    """
    The database system used by the server (TinyDB) relies on .JSON files that doesn't accept serialized data.
    Thus, particular processing needs to be done prior to any storage in the DB. The conversion used in this
    project relies on the base64 library. This library allows for easy conversions between 'bytes' and 'strings'.
    """
    return get_rsa_private_key().save_pkcs1().decode('utf-8')


def rsa_encrypt(message):
    publicKey = get_rsa_public_key()
    return rsa.encrypt(message.encode(), publicKey)


def rsa_encrypt_with_peer_public_key(peer_public_key, plaintext):
    publicKey = rsa.PublicKey.load_pkcs1(peer_public_key.encode('utf-8'))
    binary_cipher = rsa.encrypt(plaintext.encode(), publicKey)
    binary_cipher_in_b64 = base64.b64encode(binary_cipher)
    binary_cipher_in_b64_string = binary_cipher_in_b64.decode()
    return binary_cipher_in_b64_string


def rsa_decrypt_b64_with_private_key(binary_cipher_in_b64_string):
    encoded_encrypted_b64 = binary_cipher_in_b64_string.encode()
    encoded_encrypted = base64.b64decode(encoded_encrypted_b64)
    decoded_decrypted = rsa_decrypt(encoded_encrypted)
    return decoded_decrypted


def rsa_decrypt(encr_message):
    privatekey = get_rsa_private_key()
    return rsa.decrypt(encr_message, privatekey).decode()



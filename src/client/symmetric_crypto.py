# https://cryptobook.nakov.com/symmetric-key-ciphers/aes-encrypt-decrypt-examples
# https://stackoverflow.com/questions/65230554/cannot-decode-encrypted-rsa-message-python3

import base64
import binascii
import os
import pyaes
import secrets
from asymmetric_crypto import rsa_encrypt_with_peer_public_key, rsa_decrypt_b64_with_private_key


def byte_to_base64_string(byte_message):
    byte_message_b64 = base64.b64encode(byte_message)
    return byte_message_b64.decode()


def base64_string_to_byte(b64_string):
    encoded_b64 = b64_string.encode()
    return base64.b64decode(encoded_b64)


def initialize_personal_aes_key():
    key = os.urandom(32)
    key_b64_string = byte_to_base64_string(key)
    iv_string = secrets.randbits(256)
    print('AES encryption key:', key_b64_string)
    print('Initialization vector of CTR mode:', iv_string)

    if not os.path.exists("./keys"):
        os.mkdir("./keys")
    with open("keys/private_AES.pem", "w") as file:
        file.write(key_b64_string)
    with open("keys/CTR_IV.txt", "w") as file:
        file.write(str(iv_string))


def get_AES_secret_key():
    if not os.path.exists("keys/private_AES.pem"):
        initialize_personal_aes_key()
    f1 = open("keys/private_AES.pem", "r")
    f2 = open("keys/CTR_IV.txt")

    aes_key = f1.read()
    iv_string = f2.read()
    return base64_string_to_byte(aes_key), int(iv_string)


def encryption_using_AES_key(plaintext):
    aes_key, iv = get_AES_secret_key()
    aes = pyaes.AESModeOfOperationCTR(aes_key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decryption_using_AES_key(ciphertext):
    aes_key, iv = get_AES_secret_key()
    aes = pyaes.AESModeOfOperationCTR(aes_key, pyaes.Counter(iv))
    plaintext = aes.decrypt(ciphertext)
    return plaintext


def create_encrypted_symmetric_key(rsa_public_key):
    aes_key = byte_to_base64_string(get_AES_secret_key())
    encrypted_dummy_aes_key = rsa_encrypt_with_peer_public_key(rsa_public_key, aes_key)
    print(encrypted_dummy_aes_key)
    print(rsa_decrypt_b64_with_private_key(encrypted_dummy_aes_key)) # Only works since all users have the same RSA key pair
    return encrypted_dummy_aes_key


# To check if encr/decr is working properly :
# initialize_personal_aes_key()
# aes, iv = get_AES_secret_key()
# print(decryption_using_AES_key(encryption_using_AES_key("Hello64")))

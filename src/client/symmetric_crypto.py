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


def initialize_personal_aes_key(conversation_id):
    key = os.urandom(32)
    key_b64_string = byte_to_base64_string(key)
    # iv_string = secrets.randbits(256)
    #print('AES encryption key:', key_b64_string)
    if not os.path.exists("./keys"):
        os.mkdir("./keys")
    with open(f'keys/private_AES_{conversation_id}.pem', "w") as file:
        file.write(key_b64_string)


def get_AES_secret_key(conversation_id):
    if not os.path.exists(f'keys/private_AES_{conversation_id}.pem'):
        initialize_personal_aes_key(conversation_id)
    f1 = open(f'keys/private_AES_{conversation_id}.pem', "r")
    f2 = open(f'keys/CTR_IV.txt')

    aes_key = f1.read()
    iv_string = f2.read()
    return base64_string_to_byte(aes_key), int(iv_string)


def encryption_using_AES_key(plaintext, conversation_id):
    aes_key, iv = get_AES_secret_key(conversation_id)
    aes = pyaes.AESModeOfOperationCTR(aes_key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext


def decryption_using_AES_key(ciphertext, conversation_id):
    aes_key, iv = get_AES_secret_key(conversation_id)
    aes = pyaes.AESModeOfOperationCTR(aes_key, pyaes.Counter(iv))
    plaintext = aes.decrypt(ciphertext)
    return plaintext


def check_for_existing_local_key(conversation_id, encr_aes_key):
    if not os.path.exists(f'keys/private_AES_{conversation_id}.pem'):
        print("WRITING NEW AES KEY IN LOCAL FILE")
        new_secret_aes_key = rsa_decrypt_b64_with_private_key(encr_aes_key)
        with open(f'keys/private_AES_{conversation_id}.pem', "w") as file:
            file.write(new_secret_aes_key)


def create_encrypted_symmetric_key(rsa_public_key, conversation_id):
    base64_key, iv_string = get_AES_secret_key(conversation_id)
    aes_key = byte_to_base64_string(base64_key)
    encrypted_aes_key = rsa_encrypt_with_peer_public_key(rsa_public_key, aes_key)
    #print('encrypted_aes_key', encrypted_aes_key)
    #print('aes_key', aes_key)
    #print('rsa_decrypt_aes_key', rsa_decrypt_b64_with_private_key(encrypted_aes_key)) # Only works since all users have the same RSA key pair
    return encrypted_aes_key


# To check if encr/decr is working properly :
#initialize_personal_aes_key("user1user2")
#aes, iv = get_AES_secret_key("test33test30")
#print(decryption_using_AES_key(encryption_using_AES_key("Hello64", "user1user2"), "user1user2"))

# From https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
# From https://stackoverflow.com/questions/65597453/how-to-store-private-and-public-key-into-pem-file-generated-by-rsa-module-of-pyt

import os
import rsa


def generate_rsa_key_pair():
    publicKey, privateKey = rsa.newkeys(1024)
    publicKeyPkcs1PEM = publicKey.save_pkcs1().decode('utf8') # Use this to store (files, DB, etc) the RSA keys
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
    return get_rsa_public_key().save_pkcs1().decode('utf-8')


def get_rsa_private_key():
    if not os.path.exists("keys/private_rsa.pem"):
        generate_rsa_key_pair()

    f = open("keys/private_rsa.pem", "r")
    private_key = rsa.PrivateKey.load_pkcs1(f.read().encode('utf-8'))
    return private_key


def get_rsa_storable_private_key():
    return get_rsa_private_key().save_pkcs1().decode('utf-8')


def rsa_encrypt(message):
    publicKey = get_rsa_public_key()
    return rsa.encrypt(message.encode(), publicKey)


def rsa_decrypt(encr_message):
    privatekey = get_rsa_private_key()
    return rsa.decrypt(encr_message, privatekey).decode()



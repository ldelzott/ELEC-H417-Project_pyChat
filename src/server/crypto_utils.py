import hashlib as h


def hash_pwd(pwd):
    m = h.sha256()
    m.update(pwd.encode())
    return m.hexdigest()

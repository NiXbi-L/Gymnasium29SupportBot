import hashlib
def passhashing(password):
    return hashlib.sha256(password.encode()).hexdigest()
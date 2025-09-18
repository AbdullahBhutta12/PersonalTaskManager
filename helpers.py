from argon2 import PasswordHasher

ph = PasswordHasher()


def bcrypt(password: str) -> str:
    return ph.hash(password)

def verify(hashed_password, plain_password) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False

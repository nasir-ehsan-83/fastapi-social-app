from passlib.context import CryptContext

password_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    password_truncade = password_bytes.decode("utf-8", errors = "ingore")

    return password_context.hash(password_context)

def verify(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    
    return password_context.verify(plain_password, hashed_password)
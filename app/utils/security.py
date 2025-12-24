from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# bcrypt supports max 72 bytes
MAX_PASSWORD_LENGTH = 72


def _normalize_password(password: str) -> str:
    """
    Ensures password length is safe for bcrypt.
    """
    if password:
        return password[:MAX_PASSWORD_LENGTH]
    return password


def hash_password(password: str) -> str:
    safe_password = _normalize_password(password)
    return pwd_context.hash(safe_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = _normalize_password(plain_password)
    return pwd_context.verify(safe_password, hashed_password)

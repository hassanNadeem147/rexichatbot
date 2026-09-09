from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config.settings import config_auth

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        password_hasher.verify(hashed_password, password)
        return True
    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError,
    ):
        return False


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=config_auth.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        payload,
        config_auth.JWT_SECRET_KEY,
        algorithm=config_auth.JWT_ALGORITHM
    )
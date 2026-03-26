from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.config import settings
from app.models.user import User
from app.schemas.auth import AuthUser, UserRole

_DEFAULT_USERS = {
    "admin": {"password": "admin123", "role": UserRole.ADMIN},
    "user": {"password": "user123", "role": UserRole.USER},
}


def _hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


def get_user_by_username(db: Session, username: str) -> AuthUser | None:
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        return None
    return AuthUser(username=user.username, role=user.role)


def authenticate_user(db: Session, username: str, password: str) -> AuthUser | None:
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        return None
    if not _verify_password(password, user.password_hash):
        return None
    return AuthUser(username=user.username, role=user.role)


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    ttl_minutes = expires_minutes or settings.JWT_EXPIRES_MINUTES
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    payload = {**data, "exp": expire_at}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

    except ExpiredSignatureError as exc:
        raise ValueError("Токен истёк") from exc

    except InvalidTokenError as exc:
        raise ValueError("Некорректный токен") from exc


def seed_default_users(db: Session) -> None:
    for username, data in _DEFAULT_USERS.items():
        existing = db.scalar(select(User).where(User.username == username))

        if existing is not None:
            continue

        db.add(
            User(
                username=username,
                password_hash=_hash_password(data["password"]),
                role=data["role"],
            )
        )
    db.commit()


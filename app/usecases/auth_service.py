from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import AuthUser, TokenResponse, UserRole
from app.services.auth import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    get_user_by_username,
)


class AuthUseCase:
    def __init__(self, db: Session) -> None:
        self._db = db

    def login(self, username: str, password: str) -> TokenResponse:
        user = authenticate_user(self._db, username, password)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )

        access_token = create_access_token(
            {
                "sub": user.username,
                "role": user.role,
            }
        )

        return TokenResponse(access_token=access_token)

    def get_current_user(self, token: str) -> AuthUser:
        try:
            payload = decode_access_token(token)

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Некорректный payload токена",
            )

        try:
            token_role = UserRole(role)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неизвестная роль в токене",
            ) from exc

        db_user = get_user_by_username(self._db, username)

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден в БД",
            )

        if db_user.role != token_role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Роль в токене не совпадает с ролью в БД",
            )
        return db_user

    def ensure_roles(self, user: AuthUser, allowed_roles: set[UserRole]) -> AuthUser:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )
        return user

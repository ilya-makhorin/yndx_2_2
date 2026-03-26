from collections.abc import Callable
from typing import Annotated, TypedDict

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import AuthUser, UserRole
from app.services.task_storage import SqlAlchemyTaskStorage
from app.usecases.auth_service import AuthUseCase
from app.usecases.task_service import TaskUseCase


class RequestContext(TypedDict):
    request_id: str
    process_time: float

DbDep = Annotated[Session, Depends(get_db)]

bearer_scheme = HTTPBearer(auto_error=False)


def get_task_use_case(db: DbDep) -> TaskUseCase:
    return TaskUseCase(storage=SqlAlchemyTaskStorage(db=db))


def get_auth_use_case(db: DbDep) -> AuthUseCase:
    return AuthUseCase(db=db)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)],
) -> AuthUser:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется Bearer токен",
        )
    return auth_use_case.get_current_user(credentials.credentials)


def require_roles(*allowed_roles: UserRole) -> Callable[[AuthUser], AuthUser]:
    allowed = set(allowed_roles)

    def _checker(
        current_user: Annotated[AuthUser, Depends(get_current_user)],
        auth_use_case: Annotated[AuthUseCase, Depends(get_auth_use_case)],
    ) -> AuthUser:
        return auth_use_case.ensure_roles(current_user, allowed)
    return _checker


def get_request_context(request: Request) -> RequestContext:
    return {
        "request_id": getattr(request.state, "request_id", "unknown"),

        "process_time": getattr(request.state, "process_time", 0.0),
    }

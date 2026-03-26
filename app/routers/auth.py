from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.common import get_auth_use_case, get_current_user
from app.schemas.auth import AuthUser, LoginRequest, TokenResponse
from app.usecases.auth_service import AuthUseCase


router = APIRouter(prefix="/auth", tags=["auth"])

AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_use_case)]


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    data: LoginRequest,
    auth_use_case: AuthUseCaseDep,
) -> TokenResponse:
    return auth_use_case.login(data.username, data.password)


@router.get(
    "/me",
    response_model=AuthUser,
    status_code=status.HTTP_200_OK,
)
def me(
    current_user: AuthUser = Depends(get_current_user),
) -> AuthUser:
    return current_user


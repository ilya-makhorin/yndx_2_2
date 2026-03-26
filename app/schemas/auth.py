from enum import StrEnum

from pydantic import BaseModel

class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class AuthUser(BaseModel):
        username: str
        role: UserRole
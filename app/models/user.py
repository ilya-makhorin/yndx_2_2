from app.models.base import Base
from app.schemas.auth import UserRole
from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100),unique=True, nullable=False)
    password_hash: Mapped[str|None] = mapped_column(String(128), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda values: [item.value for item in values],
            native_enum=False,
            length=16,
        ),
        nullable = False,
        default = UserRole.USER,
    )
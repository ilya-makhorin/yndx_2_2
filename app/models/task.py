from app.models.base import Base
from app.schemas.task import TaskStatus
from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str|None] = mapped_column(String(100), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            values_callable=lambda values: [item.value for item in values],
            native_enum=False,
            length=32,
        ),
        nullable = False,
        default = TaskStatus.TODO,
    )
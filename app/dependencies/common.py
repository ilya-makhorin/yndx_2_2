from typing import TypedDict, Annotated

from fastapi import Depends, Request, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.services.task_storage import SqlAlchemyTaskStorage
from app.usecases.task_service import TaskUseCase
from app.db.session import get_db

class RequestContext(TypedDict):
    request_id: str
    process_time: float



DBDep = Annotated[Session, Depends(get_db)]

def get_task_use_case(db: DBDep) -> TaskUseCase:
    return TaskUseCase(storage=SqlAlchemyTaskStorage(db=db))


def verify_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != "secret-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный ключ"
        )

    return x_api_key


def get_request_context(request: Request) -> RequestContext:
    return {
        "request_id": getattr(request.state, "request_id", "unknown"),
        "process_time": getattr(request.state, "process_time", 0.0)
    }
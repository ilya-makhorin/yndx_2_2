from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.common import (
    get_current_user,
    get_request_context,
    get_task_use_case,
    require_roles,
)
from app.schemas.auth import AuthUser, UserRole
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.usecases.task_service import TaskUseCase

router = APIRouter(prefix="/tasks", tags=["tasks"])

TaskUseCaseDep = Annotated[TaskUseCase, Depends(get_task_use_case)]
RequestContextDep = Annotated[dict[str, float | str], Depends(get_request_context)]
CurrentUserDep = Annotated[AuthUser, Depends(get_current_user)]
AdminDep = Annotated[AuthUser, Depends(require_roles(UserRole.ADMIN))]


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
def list_tasks(use_case: TaskUseCaseDep, _: CurrentUserDep) -> TaskListResponse:
    return use_case.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, use_case: TaskUseCaseDep, _: CurrentUserDep) -> TaskResponse:
    return use_case.get_task(task_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    use_case: TaskUseCaseDep,
    _: AdminDep,
    context: RequestContextDep,
) -> TaskResponse:
    _ = context
    task = use_case.create_task(data)
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    data: TaskUpdate,
    use_case: TaskUseCaseDep,
    _: AdminDep,
) -> TaskResponse:
    return use_case.update_status(task_id, data)

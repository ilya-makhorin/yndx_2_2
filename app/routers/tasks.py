from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.dependencies.common import get_request_context, get_task_use_case, verify_api_key
from app.schemas.task import TaskCreate, TaskStatus, TaskUpdate, TaskResponse, TaskListResponse
from app.usecases.task_service import TaskUseCase

router = APIRouter(prefix="/tasks", tags=["tasks"])

TaskUseCaseDep = Annotated[TaskUseCase, Depends(get_task_use_case)]
RequestContextDep = Annotated[dict[str, float | str], Depends(get_request_context)]
ApiKeyDep = Annotated[str, Depends(verify_api_key)]


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
def list_tasks(use_case:  TaskUseCaseDep) -> TaskListResponse:
    return use_case.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def list_tasks(task_id: int, use_case: TaskUseCaseDep) -> TaskResponse:
    return use_case.get_task(task_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
        data: TaskCreate,
        use_case: TaskUseCaseDep,
        _: ApiKeyDep,
        context: RequestContextDep
                ) -> TaskResponse:
        task = use_case.create_task(data)
        return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
        tasl_id: int,
        data: TaskUpdate,
        use_case: TaskUseCaseDep,
        _: ApiKeyDep,
            ) -> TaskResponse:
    return use_case.update_status(tasl_id, data)

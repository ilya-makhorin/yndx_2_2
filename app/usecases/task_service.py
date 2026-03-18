from fastapi import HTTPException, status

from app.schemas.task import TaskResponse, TaskStatus, TaskCreate, TaskListResponse, TaskUpdate
from app.services.task_storage import InMemoryTaskStorage


class TaskUseCase:
    def __init__(self, storage: InMemoryTaskStorage) -> None:
        self.storage = storage

    def list_tasks(self) -> TaskListResponse:
        items = self.storage.list_tasks()
        return TaskListResponse(items=items, total=len(items))

    def get_task(self, task_id: int) -> TaskResponse:
        task = self.storage.get_task(task_id)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с id={task_id} не найдена"
            )
        return task

    def create_task(self, data: TaskCreate) -> TaskResponse:
        return self.storage.create_task(data)

    def update_status(self, task_id: int, data:TaskUpdate) -> TaskResponse:
        update_task = self.storage.update_status(task_id, TaskStatus(data.status))
        if update_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с id={task_id} не найдена"
            )
        return update_task
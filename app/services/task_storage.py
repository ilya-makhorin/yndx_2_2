from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskStatus


class SqlAlchemyTaskStorage:
    def __init__(self, db: Session):
        self._db = db
    def _to_response(self, task: Task) -> TaskResponse:
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
        )
    def list_tasks(self) ->list[TaskResponse]:
        tasks = self._db.scalars(select(Task).order_by(Task.id)).all()
        return [self._to_response(task) for task in tasks]

    def get_task(self, task_id: int) -> TaskResponse | None:
        task = self._db.get(Task, task_id)
        if task is None:
            return None
        return self._to_response(task)

    def create_task(self, data: TaskCreate) -> TaskResponse:
        task = Task(
            title = data.title,
            description = data.description,
            priority=data.priority,
            status=TaskStatus.TODO,
        )

        self._db.add(task)
        self._db.commit()
        self._db.refresh(task)

        return self._to_response(task)

    def update_status(self, task_id: int, status: TaskStatus) -> TaskResponse | None:
        task = self._db.get(Task, task_id)
        if task is None:
            return None

        task.status = status
        self._db.commit()
        self._db.refresh(task)

        return self._to_response(task)
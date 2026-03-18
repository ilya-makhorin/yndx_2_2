from app.schemas.task import TaskCreate, TaskResponse, TaskStatus


class InMemoryTaskStorage:
    def __init__(self) -> None:
        self._task: list[TaskResponse] = [
            TaskResponse(
                id=1,
                title="TestTest",
                description="TestTestTestTestTestTestTestTest",
                priority=2,
                status=TaskStatus.TODO
            ),
            TaskResponse(
                id=2,
                title="2222",
                description="22222222",
                priority=2,
                status=TaskStatus.IN_PROGRESS
            ),
        ]
        self._next_id = 3

    def list_tasks(self) -> list[TaskResponse]:
        return self._task

    def get_task(self, task_id: int) -> TaskResponse | None:
        return next((task for task in self._task if task.id == task_id), None)

    def create_task(self, data: TaskCreate) -> TaskResponse:
        task = TaskResponse(
                id=self._next_id,
                title=data.title,
                description=data.description,
                priority=data.priority,
                status=TaskStatus.TODO,
            )
        self._task.append(task)
        self._next_id += 1
        return task

    def update_status(self, task_id: int, status: TaskStatus) -> TaskResponse:
        task = self.get_task(task_id)

        if task is None:
            return None

        updated_task = task.model_copy(update={"status": status})
        index = self._task.index(task)
        self._task[index] = updated_task
        return updated_task

from app.schemas.TaskSchema import TaskInstance
from app.models.TaskModel import Task, TaskInstance


def convert_to_task_instance_response(
    task: Task, task_instance: TaskInstance
) -> TaskInstance:
    return TaskInstance(
        task_id=task_instance.task_id,
        title=task.title,
        description=task.description,
        id=task.id,
        completed=task_instance.completed,
        completed_at=task_instance.completed_at,
        due_date=task_instance.due_date,
        status=task_instance.status,
    )

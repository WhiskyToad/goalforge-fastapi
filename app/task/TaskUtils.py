from typing import List
from app.task.TaskModel import Task, TaskInstance
from app.task.TaskSchema import TaskInstanceSchema, TaskSchema


def map_task_to_schema(task: Task, instances: List[TaskInstance]) -> TaskSchema:
    return TaskSchema(
        id=task.id,
        title=task.title,
        description=task.description,
        recurring=task.recurring,
        recurring_interval=task.recurring_interval,
        created_at=task.created_at.isoformat(),
        is_habit=task.is_habit,
        icon=task.icon,
        instances=[map_instance_to_schema(instance) for instance in instances],
    )


def map_instance_to_schema(instance: TaskInstance) -> TaskInstanceSchema:
    return TaskInstanceSchema(
        task_id=instance.task_id,
        title=instance.task.title,
        description=instance.task.description,
        id=instance.id,
        completed=instance.completed,
        completed_at=(
            instance.completed_at.isoformat() if instance.completed_at else None
        ),
        due_date=instance.due_date.isoformat() if instance.due_date else None,
        status=instance.status,
    )


def map_task_task_instances(
    task: Task, task_instance: TaskInstance
) -> TaskInstanceSchema:
    due_date_str = task_instance.due_date.isoformat()
    return TaskInstanceSchema(
        task_id=task.id,
        title=task.title,
        description=task.description,
        id=task_instance.id,
        completed=task_instance.completed,
        completed_at=task_instance.completed_at,
        due_date=due_date_str,
        status=task_instance.status,
    )
from fastapi import Depends
from sqlalchemy.orm import Session
from app.shared.config.Database import get_db_connection
from app.task.TaskSchema import (
    CompleteTaskInstanceInput,
    EditTaskInput,
    TaskInstanceStatus,
)
from app.task.TaskModel import Task, TaskInstance
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from datetime import date


class TaskRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    async def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    async def create_task_instance(
        self, task_id: int, due_date: Optional[date]
    ) -> TaskInstance:
        task_instance = TaskInstance(task_id=task_id, due_date=due_date)
        self.db.add(task_instance)
        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    async def get_task_by_id_and_owner(
        self, task_id: int, owner_id: int
    ) -> tuple[Task | None, list[TaskInstance]]:
        task_with_instances = (
            self.db.query(Task)
            .options(joinedload(Task.task_instances))
            .filter(Task.id == task_id, Task.owner_id == owner_id)
            .first()
        )

        if task_with_instances:
            return task_with_instances, task_with_instances.task_instances
        else:
            return None, []

    async def get_all_tasks_for_owner(
        self, user_id: int
    ) -> List[tuple[Optional[Task], List[TaskInstance]]]:
        tasks_with_instances = (
            self.db.query(Task)
            .options(joinedload(Task.task_instances))
            .filter(Task.owner_id == user_id)
            .all()
        )
        results: List[tuple[Optional[Task], List[TaskInstance]]] = []
        for task in tasks_with_instances:
            instances: List[TaskInstance] = task.task_instances if task else []
            results.append((task, instances))
        return results

    async def get_tasks_by_due_date(self, due_date: date, user_id: int):
        tasks = (
            self.db.query(Task, TaskInstance)
            .join(TaskInstance, Task.id == TaskInstance.task_id)
            .filter(
                Task.owner_id == user_id,
                func.date(TaskInstance.due_date) == due_date,
            )
            .all()
        )
        return tasks

    async def complete_task_instance(
        self, input: CompleteTaskInstanceInput, task_instance_id: int, user_id: int
    ):
        task_instance = (
            self.db.query(TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                TaskInstance.id == task_instance_id,
                Task.owner_id == user_id,
            )
            .first()
        )
        if task_instance is None:
            return None

        task_instance.completed = True
        task_instance.completed_at = func.now()
        task_instance.status = input.status

        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    async def uncomplete_task_instance(self, task_instance_id: int, user_id: int):
        task_instance = (
            self.db.query(TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                TaskInstance.id == task_instance_id,
                Task.owner_id == user_id,
            )
            .first()
        )
        if task_instance is None:
            return None

        task_instance.completed = False
        task_instance.completed_at = None
        task_instance.status = TaskInstanceStatus.PENDING

        self.db.commit()
        self.db.refresh(task_instance)
        return task_instance

    async def edit_task(self, task_id: int, task_input: EditTaskInput, user_id: int):
        task = (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.owner_id == user_id)
            .first()
        )
        if task is None:
            return None
        task.title = task_input.title
        task.description = task_input.description
        task.recurring = task_input.recurring
        self.db.commit()
        self.db.refresh(task)
        return task

    async def delete_task_instance(self, instance_id: int, user_id: int):
        task_instance = (
            self.db.query(TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                TaskInstance.id == instance_id,
                Task.owner_id == user_id,
            )
            .first()
        )
        self.db.delete(task_instance)
        self.db.commit()
        return {"success": True}

    async def get_tasks_by_ids_and_user_id(
        self, task_ids: List[int], user_id: int
    ) -> List[tuple[Optional[Task], List[TaskInstance]]]:
        tasks_with_instances = (
            self.db.query(Task)
            .options(joinedload(Task.task_instances))
            .filter(Task.id.in_(task_ids), Task.owner_id == user_id)
            .all()
        )
        results: List[tuple[Optional[Task], List[TaskInstance]]] = []
        for task in tasks_with_instances:
            instances: List[TaskInstance] = task.task_instances if task else []
            results.append((task, instances))
        return results

    async def get_all_pending_tasks_for_owner(self, user_id: int):
        today = date.today()
        tasks_with_instances = (
            self.db.query(Task, TaskInstance)
            .join(Task, Task.id == TaskInstance.task_id)
            .filter(
                Task.owner_id == user_id,
                func.date(TaskInstance.due_date) < today,
                TaskInstance.status == TaskInstanceStatus.PENDING,
            )
            .all()
        )
        return tasks_with_instances

    async def delete_task_and_instances(self, task_id: int, user_id: int):
        # Retrieve the task with the specified task_id and its associated instances
        task = (
            self.db.query(Task)
            .options(joinedload(Task.task_instances))
            .filter(Task.owner_id == user_id, Task.id == task_id)
            .first()
        )
        if task:
            # Delete each associated task instance
            for task_instance in task.task_instances:
                self.db.delete(task_instance)
            # Delete the task itself
            self.db.delete(task)
            # Commit the changes
            self.db.commit()
        return {"success": True}

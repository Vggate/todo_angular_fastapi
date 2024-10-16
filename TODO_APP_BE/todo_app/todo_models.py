from sqlalchemy import Boolean, Column, DateTime, String

from base.models import Base
from base.exceptions import RecordNotFoundError, ValidationError, UserError

class Task(Base):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime)

    def get_tasks(self, showCompleted: Boolean = True, task_id: int = 0, q: str = '', order: str = None, offset: int = 0, limit: int = None):
        task_filter = [] if showCompleted else [Task.completed == showCompleted]
        if task_id:
            task_filter.append(Task.id == task_id)
        if q:
            task_filter.append(Task.title.like(f"%{q}%"))
        tasks_count = self.search_count(filters=task_filter)
        tasks = self.search(filters=task_filter, order=order, offset=offset, limit=limit)
        return {
            'length': tasks_count,
            'records': tasks,
        }

    def add_task(self, create_val: dict):
        create_val.pop('id', None)  # Safely remove 'id' if it exists

        if not create_val.get('title'):
            raise UserError("Task must have a title.")

        return self.create(create_val)

    def remove_task(self, task_id) -> bool:
        task = self.browse(task_id)
        if not task:
            raise RecordNotFoundError(f"Task with id {task_id} not found.")

        return task.delete()

    def edit_task(self, task_id, val: dict):
        if not task_id:
            raise ValidationError("Task ID is required for editing.")

        task = self.browse(task_id)
        if not task:
            raise RecordNotFoundError(f"Task with id {task_id} not found.")

        return task.update(val)

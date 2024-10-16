from typing import List
from datetime import datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing_extensions import Annotated

from base.http.middleware import Request, session_handler
from todo_app.todo_models import Task

todo_api = APIRouter(prefix='/api')

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    completed: bool = False

class RequestCreate(TaskBase):
    pass

class RequestUpdateTask(TaskBase):
    pass

class ReponseTask(TaskBase):
    id: int

class ResponseTaskList(BaseModel):
    length: int
    records: List[ReponseTask]

class FilterParams(BaseModel):
    showCompleted: bool = True
    task_id: int = 0
    q: str = ''
    order: str = ''
    offset: int = 0
    limit: int = 80

def _get_model(request) -> Task:
    return request.env['tasks']

@todo_api.get('/task/', response_model=ResponseTaskList)
@session_handler
def get_tasks(request: Request, search_query: Annotated[FilterParams, Query()]):
    result = _get_model(request).get_tasks(search_query.showCompleted, search_query.task_id, search_query.q, 
                                           search_query.order, search_query.offset, search_query.limit)
    return result

@todo_api.post('/task/', response_model=ReponseTask)
@session_handler
def add_task(request: Request, payloads: RequestCreate):
    result = _get_model(request).add_task(payloads.model_dump())
    return result

@todo_api.delete('/task/{task_id}')
@session_handler
def remove_task(request: Request, task_id: int):
    result = _get_model(request).remove_task(task_id)
    return result

@todo_api.put('/task/{task_id}')
@session_handler
def edit_task(request: Request, task_id:int, payloads: RequestUpdateTask):
    result = _get_model(request).edit_task(task_id, payloads.model_dump())
    return result
from fastapi import APIRouter, status, Response
from bson import ObjectId
from passlib.hash import sha256_crypt
from config.db import conn
from schemas.task import taskEntity, tasksEntity
from models.task import Task

task = APIRouter() 

# Tasks List
@task.get('/tasks', response_model=list[Task], tags=["tasks"])
async def find_all_tasks():
    return tasksEntity(conn.local.task.find())

# Create Task
@task.post('/tasks', response_model=Task, tags=["tasks"])
async def create_task(task: Task):
    new_task = dict(task)
    del new_task["id"]
    
    id = conn.local.task.insert_one(new_task).inserted_id
    task = conn.local.task.find_one({"_id": id})
    return taskEntity(task)


# Get Task By Id
@task.get('/tasks/{id}', response_model=Task, tags=["tasks"])
async def find_task(id: str):
    return taskEntity(conn.local.task.find_one({"_id": ObjectId(id)}))

# Update Task
@task.put("/tasks/{id}", response_model=Task, tags=["tasks"])
async def update_task(id: str, task: Task):
    conn.local.task.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(task)
    })
    return taskEntity(conn.local.task.find_one({"_id": ObjectId(id)}))

# Delete Task
@task.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
async def delete_task(id: str):
    conn.local.task.find_one_and_delete({
        "_id": ObjectId(id)
    })
    return Response(status_code=204)
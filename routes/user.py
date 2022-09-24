from fastapi import APIRouter, status, Response
from bson import ObjectId
from passlib.hash import sha256_crypt
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User

user = APIRouter() 

# Lista de user
@user.get('/users', response_model=list[User], tags=["users"])
async def find_all_users():
    return usersEntity(conn.local.user.find())

# Crear user
@user.post('/users', response_model=User, tags=["users"])
async def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    
    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({"_id": id})
    return userEntity(user)

# Get user By Id
@user.get('/users/{id}', response_model=User, tags=["users"])
async def find_user(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

# Update user
@user.put("/users/{id}", response_model=User, tags=["users"])
async def update_user(id: str, user: User):
    conn.local.user.find_one_and_update({
        "_id": ObjectId(id)
    }, {
        "$set": dict(user)
    })
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

# Delete user
@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
    conn.local.user.find_one_and_delete({
        "_id": ObjectId(id)
    })
    return Response(status_code=204)

from ast import dump
from re import X
from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from models import Gender, User, Role, UserUpdate

app = FastAPI();

db: List[User] = [
    User(
        id=UUID("b39be06e-c073-4f7f-a7d0-a1367317c5cb"),
        first_name="Jade",
        last_name="Doe",
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID("ac0f2027-1c25-4aa0-a35f-228af1ed7ff2"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]


@app.get("/")
async def root():
    return {"Hello": "Wooorld"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_to_update: UserUpdate, user_id: UUID):
    elemToUpdate = next(x for x in db if x.id == user_id)
    val = user_to_update
    for x, y in val:
        if y != None:
            setattr(elemToUpdate, x, y)
    return 

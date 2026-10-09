from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    name: str
    email: str


users_db: dict[int, User] = {}
next_id: int = 1


@router.get("/{user_id}")
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"id": user_id, **users_db[user_id].model_dump()}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    global next_id
    user_id = next_id
    next_id += 1
    users_db[user_id] = user
    return {"id": user_id, **user.model_dump()}


@router.put("/{user_id}")
async def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    users_db[user_id] = user
    return {"id": user_id, **user.model_dump()}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del users_db[user_id]
    return None
from fastapi import FastAPI

from src.routers import user

app = FastAPI()

app.include_router(user.router, prefix="/users")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
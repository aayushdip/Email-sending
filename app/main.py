from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine
from app.hashing_password import hash_password
import app.models as models
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserRead
from app.dependencies import get_db
from typing import List
<<<<<<< HEAD:app/main.py
from app.send_email import send_email_background
from app.send_email import send_email_background

app = FastAPI(title="mail sending API")
models.Base.metadata.create_all(bind=engine)
=======
from send_email import send_email_background
from send_email import send_email_background
app =FastAPI(title="mail sending API")
model.Base.metadata.create_all(bind=engine)
>>>>>>> main:main.py


@app.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(
            fullname=user.fullname,
            email=user.email,
            hashed_password=hash_password(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database Error")


@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).get(user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/users", response_model=List[UserRead])
async def read_user(db: Session = Depends(get_db)):
    try:
        db_users = db.query(User).all()
        if not db_users:
            raise HTTPException(status_code=404, detail="No users are registered")
        return db_users
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/send-email/backgroundtasks")
async def send_email_backgroundtasks(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    try:
        users = db.query(User).all()
        email = [user.email for user in users]
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database error")
    send_email_background(background_tasks, "Hello World", email)
    return "Success"

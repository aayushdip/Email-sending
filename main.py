from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import  engine
from hashing_password import hash_password
import model
from model import User
from schemas import UserCreate, UserRead
from dependencies import get_db
from typing import List

app =FastAPI(title="mail sending API")
model.Base.metadata.create_all(bind=engine)


@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(fullname=user.fullname, email=user.email, hashed_password=hash_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except SQLAlchemyError as e:
        print("Error caught:", e)
        raise HTTPException(status_code=500, detail="Database Error")

@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int,db: Session = Depends(get_db)):
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
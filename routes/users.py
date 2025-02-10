from fastapi import APIRouter, HTTPException, Depends
from database import SessionLocal, engine, Base, RecipeDB, UserDB
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.users import Ingredient, CreateUser, User
from typing import List
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


user_routes = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

````



@user_routes.post("/", response_model=User, status_code=201)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    db_user = UserDB(**user.model_dump())
    # user = db.query(UserDB).first() #Temporary, we will create users later
    # db_user.created_by = user.id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user


@user_routes.put("/{user_id}", )    
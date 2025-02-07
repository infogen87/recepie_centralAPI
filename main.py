from typing import List
from routes.recipes import recipe_routes
from routes.recipes import get_db

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session


from database import SessionLocal, engine, Base, RecipeDB, UserDB
from sqlalchemy.orm import joinedload
from sqlalchemy import select

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app.include_router(recipe_routes, prefix="/recipes", tags= ["recipes"])



@app.get("/")
async def root():
    return {"message": "welcome to the Recipe API!"}       

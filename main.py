from typing import List
from fastapi.middleware.cors import CORSMiddleware
from routes.recipes import recipe_routes
from routes.recipes import get_db

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session


from database import SessionLocal, engine, Base, RecipeDB, UserDB
from sqlalchemy.orm import joinedload
from sqlalchemy import select

Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["*"] #change this to you frontend origin later

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"] )

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

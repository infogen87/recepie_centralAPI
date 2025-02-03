from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from models import Ingredient, Recipe
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

@app.get("/recipes", response_model=List[Recipe])
async def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(RecipeDB).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes", response_model=Recipe, status_code=201)
async def create_recipe(recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = RecipeDB(**recipe.model_dump())
    user = db.query(UserDB).first() #Temporary, we will create users later
    db_recipe.created_by = user.id
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, updated_recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for key, value in updated_recipe.model_dump().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return updated_recipe

@app.delete("/recipes/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeDB).filter(RecipeDB.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return
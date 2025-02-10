from typing import List, Optional

from pydantic import BaseModel






class Ingredient(BaseModel):
    id: int
    context: str


class RecipeStep(BaseModel):
    id: int
    context: str


class Recipe(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    steps: list[RecipeStep]
    ingredients: List[Ingredient]
    # created_by: Optional[int] = None
    class Config:
        orm_mode = True

  
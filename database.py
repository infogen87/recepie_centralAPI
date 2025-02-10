from dotenv import load_dotenv
import os
from datetime import datetime
import enum


load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class RecipeDifficulty(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  
    created_at = Column(DateTime, default=datetime.now)
    image_url = Column(String, default=)
    description = Column(String)
    email = Column(String, nullable=False, unique=True)

    comment = relationship("CommentDB", back_populates="user")
    category = relationship("CategoryDB", back_populates="user")
    recipes = relationship("RecipeDB", back_populates="user")
    saves = relationship("SaveDB", back_populates="user")
    likes = relationship("LikeDB", back_populates="user")


class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String)
    created_at = Column()
    difficulty = Column(Enum(RecipeDifficulty), nullable=False, default=RecipeDifficulty.MEDIUM)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    like_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)

    
    category = relationship("CategoryDB", back_populates="recipe")
    ingredients = relationship("IngredientDB", back_populates="recipe")
    steps = relationship("Recipe_stepsDB", back_populates="recipe")
    user = relationship("UserDB", back_populates="recipes")
    likes = relationship("LikeDB", back_populates="recipe")
    comment = relationship("CommentDB", back_populates="recipe")
    images = relationship("RecipeImagesDB", back_populates="recipe")
    saves = relationship("SaveDB", back_populates="recipe")


class RecipeImagesDB(Base):
    __tablename__ = "recipe_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    recipe = relationship("RecipeDB", back_populates="images")


class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("UserDB", back_populates="comment")
    recipe = relationship("RecipeDB", back_populates="comment")


class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    image_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("UserDB", back_populates="category")
    recipe = relationship("RecipeDB", back_populates="category")


class SaveDB(Base):
    __tablename__ = "saved_recipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("UserDB", back_populates="saves")
    recipe = relationship("RecipeDB", back_populates="saves")


class LikeDB(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("UserDB", back_populates="likes")
    recipe = relationship("RecipeDB", back_populates="likes")


class Recipe_stepsDB(Base):
    __tablename__ = "recipe_steps" 

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    content = Column()

    recipe = relationship("RecipeDB", back_populates="steps")
 


class IngredientDB(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    content = Column(String, nullable=False)

    recipe = relationship("RecipeDB", back_populates="ingredients")






Base.metadata.create_all(bind=engine)

from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Store the hashed password

    recipes = relationship("RecipeDB", back_populates="creator")
    favorites = relationship("FavouriteDB", back_populates="user")
    likes = relationship("LikeDB", back_populates="user")


class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    instructions = Column(String)
    ingredients = Column(ARRAY(String))
    time_taken = Column(Integer, nullable=False)  # Time in minutes
    difficulty = Column(String, nullable=False)  # Easy, Medium, Hard

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("UserDB", back_populates="recipes")

    likes = relationship("LikeDB", back_populates="recipe")
    favorites = relationship("FavouriteDB", back_populates="recipe")
    comments = relationship("CommentDB", back_populates="recipe")
    images = relationship("RecipeImagesDB", back_populates="recipe")


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
    
    made_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("UserDB")
    recipe = relationship("RecipeDB", back_populates="comments")


class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    image_url = Column(String)


class FavouriteDB(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("UserDB", back_populates="favorites")
    recipe = relationship("RecipeDB", back_populates="favorites")


class LikeDB(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)

    user = relationship("UserDB", back_populates="likes")
    recipe = relationship("RecipeDB", back_populates="likes")









Base.metadata.create_all(bind=engine)

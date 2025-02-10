from routes import recipes

from fastapi.testclient import TestClient
from main import app, get_db
from models import Recipe
from database import SessionLocal, RecipeDB, UserDB 

client = TestClient(app)

def test_create_recipe(db: Session = Depends(get_db)):
    # Create a sample recipe
    new_recipe = Recipe(
        name="Test Recipe",
        description="A delicious test recipe",
        instructions="Follow these instructions",
        ingredients=[
            {"name": "Ingredient 1", "quantity": "1 cup"},
            {"name": "Ingredient 2", "quantity": "2 tbsp"}
        ]
    )

    # Create a sample user (temporary)
    user = UserDB(username="testuser", hashed_password="testpassword") 
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create the recipe in the database
    response = client.post("/recipes", json=new_recipe.dict())
    assert response.status_code == 201

    # Assert that the created recipe is returned in the response
    created_recipe = response.json()
    assert created_recipe["name"] == "Test Recipe" 
    assert created_recipe["description"] == "A delicious test recipe"

    # Clean up: Delete the created recipe and user
    db.query(RecipeDB).filter(RecipeDB.id == created_recipe["id"]).delete()
    db.query(UserDB).filter(UserDB.username == "testuser").delete()
    db.commit()

# Run the tests
if __name__ == "__main__":
    import pytest
    pytest.main()
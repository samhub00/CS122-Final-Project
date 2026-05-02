import os
from dotenv import load_dotenv
import zlib
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

load_dotenv()

# Initialize SQLAlchemy database instance
db = SQLAlchemy()


# ---------------------------------------------------------------------------
# Database Models
# ---------------------------------------------------------------------------

class User(db.Model, UserMixin):
    """User model for storing login credentials."""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #name = db.Column(db.String(255), nullable=False)
    #email = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    # Relationship to favorites
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model):
    """Recipe model for storing compressed recipe data."""
    __tablename__ = "recipes"
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    
    # Relationship to favorites
    favorites = db.relationship('Favorite', backref='recipe', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Recipe {self.id}>'


class Favorite(db.Model):
    """Favorite model for storing user's favorite recipes."""
    __tablename__ = "favorites"
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)
    def __repr__(self):
        return f'<Favorite user_id={self.user_id}, recipe_id={self.recipe_id}>'


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def store_recipe(recipe):
    """
    Store a recipe in the database.
    
    Args:
        recipe (dict): Recipe dictionary with 'id' key and recipe data
    """
    try:
        # Compress the JSON data using zlib
        compressed_data = zlib.compress(json.dumps(recipe).encode('utf-8'))
        
        # Check if recipe already exists
        existing_recipe = Recipe.query.filter_by(id=recipe['id']).first()
        
        if existing_recipe:
            # Update existing recipe
            existing_recipe.data = compressed_data
        else:
            # Create new recipe
            new_recipe = Recipe(id=recipe['id'], data=compressed_data)
            db.session.add(new_recipe)
        
        db.session.commit()
        print(f"Recipe {recipe['id']} stored successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error storing recipe: {e}")


def get_recipe(recipe_id):
    """
    Retrieve and decompress a recipe from the database.
    
    Args:
        recipe_id (int): The ID of the recipe
        
    Returns:
        dict: The decompressed recipe data, or None if not found
    """
    try:
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe:
            decompressed_data = zlib.decompress(recipe.data).decode('utf-8')
            return json.loads(decompressed_data)
        return None
    except Exception as e:
        print(f"Error retrieving recipe: {e}")
        return None


def add_favorite(user_id, recipe_id):
    """
    Add a recipe to a user's favorites.
    
    Args:
        user_id (int): The user's ID
        recipe_id (int): The recipe's ID
    """
    try:
        # Check if already favorited
        existing = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        if existing:
            print(f"Recipe {recipe_id} already in favorites for user {user_id}.")
            return
        
        favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
        db.session.add(favorite)
        db.session.commit()
        print(f"Recipe {recipe_id} added to favorites for user {user_id}.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding favorite: {e}")


def remove_favorite(user_id, recipe_id):
    """
    Remove a recipe from a user's favorites.
    
    Args:
        user_id (int): The user's ID
        recipe_id (int): The recipe's ID
    """
    try:
        favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            print(f"Recipe {recipe_id} removed from favorites for user {user_id}.")
        else:
            print(f"Favorite not found.")
    except Exception as e:
        db.session.rollback()
        print(f"Error removing favorite: {e}")


def get_user_favorites(user_id):
    """
    Get all favorites for a user.
    
    Args:
        user_id (int): The user's ID
        
    Returns:
        list: List of Favorite objects
    """
    try:
        return Favorite.query.filter_by(user_id=user_id).all()
    except Exception as e:
        print(f"Error retrieving favorites: {e}")
        return []


sample_json = {'id': 715415, 'image': 'https://img.spoonacular.com/recipes/715415-556x370.jpg', 'imageType': 'jpg', 'title': 'Red Lentil Soup with Chicken and Turnips', 'readyInMinutes': 55, 'servings': 8, 'sourceUrl': 'https://www.pinkwhen.com/red-lentil-soup-with-chicken-and-turnips/', 'vegetarian': False, 'vegan': False, 'glutenFree': True, 'dairyFree': True, 'veryHealthy': True, 'cheap': False, 'veryPopular': True, 'sustainable': False, 'lowFodmap': False, 'weightWatcherSmartPoints': 11, 'gaps': 'no', 'preparationMinutes': 10, 'cookingMinutes': 45, 'aggregateLikes': 1866, 'healthScore': 100.0, 'creditsText': 'pinkwhen.com', 'license': None, 'sourceName': 'pinkwhen.com', 'pricePerServing': 300.45, 'extendedIngredients': [{'id': 9037, 'aisle': 'Produce', 'image': 'avocado.jpg', 'consistency': 'SOLID', 'name': 'additional toppings: avocado', 'nameClean': 'additional toppings: avocado', 'original': 'additional toppings: diced avocado, micro greens, chopped basil)', 'originalName': 'additional toppings: diced avocado, micro greens, chopped basil)', 'amount': 8.0, 'unit': 'servings', 'meta': ['diced', 'chopped'], 'measures': {'us': {'amount': 8.0, 'unitShort': 'servings', 'unitLong': 'servings'}, 'metric': {'amount': 8.0, 'unitShort': 'servings', 'unitLong': 'servings'}}}, {'id': 11124, 'aisle': 'Produce', 'image': 'sliced-carrot.png', 'consistency': 'SOLID', 'name': 'carrots', 'nameClean': 'carrots', 'original': '3 medium carrots, peeled and diced', 'originalName': 'carrots, peeled and diced', 'amount': 3.0, 'unit': 'medium', 'meta': ['diced', 'peeled'], 'measures': {'us': {'amount': 3.0, 'unitShort': 'medium', 'unitLong': 'mediums'}, 'metric': {'amount': 3.0, 'unitShort': 'medium', 'unitLong': 'mediums'}}}, {'id': 10111143, 'aisle': 'Produce', 'image': 'celery.jpg', 'consistency': 'SOLID', 'name': 'celery stalks', 'nameClean': 'celery stalks', 'original': '3 celery stalks, diced', 'originalName': 'celery stalks, diced', 'amount': 3.0, 'unit': '', 'meta': ['diced'], 'measures': {'us': {'amount': 3.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 3.0, 'unitShort': '', 'unitLong': ''}}}, {'id': 5064, 'aisle': 'Meat', 'image': 'cooked-chicken-breast.png', 'consistency': 'SOLID', 'name': 'chicken breast', 'nameClean': 'chicken breast', 'original': '2 cups fully-cooked chicken breast, shredded (may be omitted for a vegetarian version)', 'originalName': 'fully-cooked chicken breast, shredded (may be omitted for a vegetarian version)', 'amount': 2.0, 'unit': 'cups', 'meta': ['shredded', 'fully-cooked', 'for a vegetarian version', '(may be omitted )'], 'measures': {'us': {'amount': 2.0, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 280.0, 'unitShort': 'g', 'unitLong': 'grams'}}}, {'id': 10311297, 'aisle': 'Produce', 'image': 'parsley.jpg', 'consistency': 'SOLID', 'name': 'flat leaf parsley', 'nameClean': 'flat leaf parsley', 'original': '½ cup flat leaf Italian parsley, chopped (plus extra for garnish)', 'originalName': 'flat leaf Italian parsley, chopped (plus extra for garnish)', 'amount': 0.5, 'unit': 'cup', 'meta': ['italian', 'chopped', 'for garnish', '(plus extra )'], 'measures': {'us': {'amount': 0.5, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 30.0, 'unitShort': 'g', 'unitLong': 'grams'}}}, {'id': 11215, 'aisle': 'Produce', 'image': 'garlic.png', 'consistency': 'SOLID', 'name': 'garlic', 'nameClean': 'garlic', 'original': '6 cloves of garlic, finely minced', 'originalName': 'garlic, finely minced', 'amount': 6.0, 'unit': 'cloves', 'meta': ['finely minced'], 'measures': {'us': {'amount': 6.0, 'unitShort': 'cloves', 'unitLong': 'cloves'}, 'metric': {'amount': 6.0, 'unitShort': 'cloves', 'unitLong': 'cloves'}}}, {'id': 4053, 'aisle': 'Oil, Vinegar, Salad Dressing', 'image': 'olive-oil.jpg', 'consistency': 'LIQUID', 'name': 'olive oil', 'nameClean': 'olive oil', 'original': '2 tablespoons olive oil', 'originalName': 'olive oil', 'amount': 2.0, 'unit': 'tablespoons', 'meta': [], 'measures': {'us': {'amount': 2.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}, 'metric': {'amount': 2.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}}}, {'id': 10011693, 'aisle': 'Canned and Jarred', 'image': 'tomatoes-canned.png', 'consistency': 'SOLID', 'name': 'canned tomatoes', 'nameClean': 'canned tomatoes', 'original': '28 ounce-can plum tomatoes, drained and rinsed, chopped', 'originalName': 'can plum tomatoes, drained and rinsed, chopped', 'amount': 28.0, 'unit': 'ounce', 'meta': ['drained and rinsed', 'chopped'], 'measures': {'us': {'amount': 28.0, 'unitShort': 'oz', 'unitLong': 'ounces'}, 'metric': {'amount': 793.787, 'unitShort': 'g', 'unitLong': 'grams'}}}, {'id': 10016069, 'aisle': 'Canned and Jarred', 'image': 'red-lentils.png', 'consistency': 'SOLID', 'name': 'lentils', 'nameClean': 'lentils', 'original': '2 cups dried red lentils, rinsed', 'originalName': 'dried red lentils, rinsed', 'amount': 2.0, 'unit': 'cups', 'meta': ['dried', 'red', 'rinsed'], 'measures': {'us': {'amount': 2.0, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 360.0, 'unitShort': 'g', 'unitLong': 'grams'}}}, {'id': 1102047, 'aisle': 'Spices and Seasonings', 'image': 'salt-and-pepper.jpg', 'consistency': 'SOLID', 'name': 'salt and pepper', 'nameClean': 'salt and pepper', 'original': 'salt and black pepper, to taste', 'originalName': 'salt and black pepper, to taste', 'amount': 8.0, 'unit': 'servings', 'meta': ['black', 'to taste'], 'measures': {'us': {'amount': 8.0, 'unitShort': 'servings', 'unitLong': 'servings'}, 'metric': {'amount': 8.0, 'unitShort': 'servings', 'unitLong': 'servings'}}}, {'id': 11564, 'aisle': 'Produce', 'image': 'turnips.png', 'consistency': 'SOLID', 'name': 'turnip', 'nameClean': 'turnip', 'original': '1 large turnip, peeled and diced', 'originalName': 'turnip, peeled and diced', 'amount': 1.0, 'unit': 'large', 'meta': ['diced', 'peeled'], 'measures': {'us': {'amount': 1.0, 'unitShort': 'large', 'unitLong': 'large'}, 'metric': {'amount': 1.0, 'unitShort': 'large', 'unitLong': 'large'}}}, {'id': 6615, 'aisle': 'Canned and Jarred', 'image': 'chicken-broth.png', 'consistency': 'LIQUID', 'name': 'vegetable stock', 'nameClean': 'vegetable stock', 'original': '8 cups vegetable stock', 'originalName': 'vegetable stock', 'amount': 8.0, 'unit': 'cups', 'meta': [], 'measures': {'us': {'amount': 8.0, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 1.88, 'unitShort': 'l', 'unitLong': 'liters'}}}, {'id': 10511282, 'aisle': 'Produce', 'image': 'brown-onion.png', 'consistency': 'SOLID', 'name': 'onion', 'nameClean': 'onion', 'original': '1 medium yellow onion, diced', 'originalName': 'yellow onion, diced', 'amount': 1.0, 'unit': 'medium', 'meta': ['diced', 'yellow'], 'measures': {'us': {'amount': 1.0, 'unitShort': 'medium', 'unitLong': 'medium'}, 'metric': {'amount': 1.0, 'unitShort': 'medium', 'unitLong': 'medium'}}}], 'summary': 'Red Lentil Soup with Chicken and Turnips might be a good recipe to expand your main course repertoire. This recipe serves 8 and costs $3.0 per serving. One serving contains 477 calories, 27g of protein, and 20g of fat. It is brought to you by Pink When. 1866 people have tried and liked this recipe. It can be enjoyed any time, but it is especially good for Autumn. From preparation to the plate, this recipe takes approximately 55 minutes. It is a good option if you\'re following a gluten free and dairy free diet. Head to the store and pick up salt and pepper, canned tomatoes, flat leaf parsley, and a few other things to make it today. Overall, this recipe earns a spectacular spoonacular score of 99%. If you like this recipe, you might also like recipes such as <a href="https://spoonacular.com/recipes/red-lentil-and-chicken-soup-682185">Red Lentil and Chicken Soup</a>, <a href="https://spoonacular.com/recipes/red-lentil-and-chicken-soup-1058971">Red Lentil and Chicken Soup</a>, and <a href="https://spoonacular.com/recipes/red-lentil-soup-34121">Red-Lentil Soup</a>.', 'cuisines': [], 'dishTypes': ['lunch', 'soup', 'main course', 'main dish', 'dinner'], 'diets': ['gluten free', 'dairy free'], 'occasions': ['fall', 'winter'], 'instructions': 'To a large dutch oven or soup pot, heat the olive oil over medium heat. Add the onion, carrots and celery and cook for 8-10 minutes or until tender, stirring occasionally. Add the garlic and cook for an additional 2 minutes, or until fragrant. Season conservatively with a pinch of salt and black pepper.To the pot, add the tomatoes, turnip and red lentils. Stir to combine. Stir in the vegetable stock and increase the heat on the stove to high. Bring the soup to a boil and then reduce to a simmer. Simmer for 20 minutes or until the turnips are tender and the lentils are cooked through. Add the chicken breast and parsley. Cook for an additional 5 minutes. Adjust seasoning to taste.Serve the soup immediately garnished with fresh parsley and any additional toppings. Enjoy!', 'analyzedInstructions': [{'name': '', 'steps': [{'number': 1, 'step': 'To a large dutch oven or soup pot, heat the olive oil over medium heat.', 'ingredients': [{'id': 4053, 'name': 'olive oil', 'localizedName': 'olive oil', 'image': 'olive-oil.jpg'}, {'id': 0, 'name': 'soup', 'localizedName': 'soup', 'image': ''}], 'equipment': [{'id': 404667, 'name': 'dutch oven', 'localizedName': 'dutch oven', 'image': 'https://spoonacular.com/cdn/equipment_100x100/dutch-oven.jpg'}]}, {'number': 2, 'step': 'Add the onion, carrots and celery and cook for 8-10 minutes or until tender, stirring occasionally.', 'ingredients': [{'id': 11124, 'name': 'carrot', 'localizedName': 'carrot', 'image': 'sliced-carrot.png'}, {'id': 11143, 'name': 'celery', 'localizedName': 'celery', 'image': 'celery.jpg'}, {'id': 11282, 'name': 'onion', 'localizedName': 'onion', 'image': 'brown-onion.png'}], 'equipment': [], 'length': {'number': 10, 'unit': 'minutes'}}, {'number': 3, 'step': 'Add the garlic and cook for an additional 2 minutes, or until fragrant. Season conservatively with a pinch of salt and black pepper.To the pot, add the tomatoes, turnip and red lentils. Stir to combine. Stir in the vegetable stock and increase the heat on the stove to high. Bring the soup to a boil and then reduce to a simmer. Simmer for 20 minutes or until the turnips are tender and the lentils are cooked through.', 'ingredients': [{'id': 1102047, 'name': 'salt and pepper', 'localizedName': 'salt and pepper', 'image': 'salt-and-pepper.jpg'}, {'id': 6615, 'name': 'vegetable stock', 'localizedName': 'vegetable stock', 'image': 'chicken-broth.png'}, {'id': 10016069, 'name': 'red lentils', 'localizedName': 'red lentils', 'image': 'red-lentils.png'}, {'id': 11529, 'name': 'tomato', 'localizedName': 'tomato', 'image': 'tomato.png'}, {'id': 10316069, 'name': 'lentils', 'localizedName': 'lentils', 'image': 'lentils-brown.jpg'}, {'id': 11564, 'name': 'turnip', 'localizedName': 'turnip', 'image': 'turnips.png'}, {'id': 11215, 'name': 'garlic', 'localizedName': 'garlic', 'image': 'garlic.png'}, {'id': 0, 'name': 'soup', 'localizedName': 'soup', 'image': ''}], 'equipment': [{'id': 404794, 'name': 'stove', 'localizedName': 'stove', 'image': 'https://spoonacular.com/cdn/equipment_100x100/oven.jpg'}, {'id': 404752, 'name': 'pot', 'localizedName': 'pot', 'image': 'https://spoonacular.com/cdn/equipment_100x100/stock-pot.jpg'}], 'length': {'number': 22, 'unit': 'minutes'}}, {'number': 4, 'step': 'Add the chicken breast and parsley. Cook for an additional 5 minutes. Adjust seasoning to taste.', 'ingredients': [{'id': 5062, 'name': 'chicken breast', 'localizedName': 'chicken breast', 'image': 'chicken-breasts.png'}, {'id': 1042027, 'name': 'seasoning', 'localizedName': 'seasoning', 'image': 'seasoning.png'}, {'id': 11297, 'name': 'parsley', 'localizedName': 'parsley', 'image': 'parsley.jpg'}], 'equipment': [], 'length': {'number': 5, 'unit': 'minutes'}}, {'number': 5, 'step': 'Serve the soup immediately garnished with fresh parsley and any additional toppings. Enjoy!', 'ingredients': [{'id': 10511297, 'name': 'fresh parsley', 'localizedName': 'fresh parsley', 'image': 'parsley.jpg'}, {'id': 0, 'name': 'soup', 'localizedName': 'soup', 'image': ''}], 'equipment': []}]}], 'language': 'en', 'spoonacularScore': 99.434814453125, 'spoonacularSourceUrl': 'https://spoonacular.com/red-lentil-soup-with-chicken-and-turnips-715415'}


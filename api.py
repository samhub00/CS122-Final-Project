import spoonacular as sp
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SP_API_KEY")

api = sp.API(api_key)

def get_random_joke():
    response = api.get_a_random_food_joke()
    data  = response.json()
    return data['text']

def search_recipes(query):
    response = api.search_recipes_complex(query=query, number=10)
    data = response.json()
    return data['results']

def ingredient_search(ingredients):
    response = api.search_ingredients(ingredients)
    data = response.json()
    return data['results']

def get_similar_recipes(recipe_id):
    response = api.get_similar_recipes(recipe_id, number=5)
    data = response.json()
    return data

def get_recipe_information(recipe_id):
    response = api.get_recipe_information(recipe_id)
    data = response.json()
    return data

def get_recipe_summary(recipe_id):
    response = api.summarize_recipe(recipe_id)
    data = response.json()
    return data['summary']


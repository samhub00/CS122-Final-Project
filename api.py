import spoonacular as sp
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SP_API_KEY")

api = sp.API(api_key)

response = api.get_a_random_food_joke()
data  = response.json()
print(data['text'])

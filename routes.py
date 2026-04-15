from flask import Flask, request, render_template
import api

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return "Hello world!"

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = api.search_recipes(query)
    return results

@app.route('/fridge', methods=['POST'])
def fridge():
    ingredients = request.form['ingredients']
    results = api.ingredient_search(ingredients)
    return results

@app.route('/similar/<int:recipe_id>')
def similar(recipe_id):
    results = api.get_similar_recipes(recipe_id)
    return results

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    result = api.get_recipe_information(recipe_id)
    return result

@app.route('/joke')
def joke():
    #joke = api.get_random_joke()
    return "joke"

if __name__ == '__main__':
    app.run(debug=True)
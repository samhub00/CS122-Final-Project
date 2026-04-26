from flask import Flask, request, render_template, send_from_directory
import os
import api

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder='templates')


# ---------------------------------------------------------------------------
# Page routes (GET) -- render the HTML templates
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search_page():
    return render_template('search.html')


@app.route('/fridge', methods=['GET'])
def fridge_page():
    return render_template('fridge.html')


@app.route('/favorites', methods=['GET'])
def favorites_page():
    return render_template('favorites.html')


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@app.route('/about')
@app.route('/generic')
def generic_page():
    return render_template('generic.html')


@app.route('/elements')
def elements_page():
    return render_template('elements.html')


# ---------------------------------------------------------------------------
# API / form routes (POST) -- handle form submissions, return data
# ---------------------------------------------------------------------------

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query') or request.form.get('q') or ''
    results = api.search_recipes(query)
    return results


@app.route('/fridge', methods=['POST'])
def fridge():
    ingredients = request.form['ingredients']
    results = api.ingredient_search(ingredients)
    return results


@app.route('/login', methods=['POST'])
def login_submit():
    # TODO: wire up real authentication (e.g. DynamoDB). For now, acknowledge the post.
    username = request.form.get('username', '')
    return f"Login attempted for user: {username}. (Auth backend not yet implemented.)"


@app.route('/signup', methods=['POST'])
def signup_submit():
    # TODO: partner will wire up real account creation (DynamoDB).
    username = request.form.get('username', '')
    return f"Signup attempted for user: {username}. (Auth backend not yet implemented.)"

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
    # joke = api.get_random_joke()
    return "joke"


# ---------------------------------------------------------------------------
# Static assets -- the Hyperspace template references /assets/... and
# /images/... relative to the HTML files, which live in templates/. Serve
# them directly from there.
# ---------------------------------------------------------------------------

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'assets'), path)


@app.route('/images/<path:path>')
def images(path):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'images'), path)


if __name__ == '__main__':
    app.run(debug=True)

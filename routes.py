from flask import Flask, flash, request, render_template, send_from_directory, redirect, url_for
import os
import dotenv
import datetime
from api import *
from data_storage import db, User, Favorite, Recipe
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



dotenv.load_dotenv()  # Load environment variables from .env file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Create database tables
with app.app_context():
    db.create_all()


class RegisterForm(FlaskForm):
    #name = StringField(validators=[InputRequired(), Length(min=1, max=150)], render_kw={"placeholder": "Full name"})
    #email = StringField(validators=[InputRequired(), Length(min=1, max=150)], render_kw={"placeholder": "Email"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=150)], render_kw={"placeholder": "Password"})
    #confirm = PasswordField(validators=[InputRequired(), Length(min=8, max=150)], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("That username already exists. Please choose a different one.")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


# ---------------------------------------------------------------------------
# Login Handling -- use Flask-Login to manage user sessions, and Flask-WTF for form handling
# ---------------------------------------------------------------------------

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        #debug start 

        print(f"DEBUG: Attempting login for username: {form.username.data}")
        print(f"DEBUG: User query result: {user}")
        if user:
            #TODO password feels weird here

            print(f"DEBUG: Found User {user.username}")
            print(f"DEBUG: Password Hash in DB: {user.password}")
            #debug end

            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    return render_template('login.html', form=form)

# signup page if users do not have login
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = RegisterForm()

    if form.validate_on_submit():
        """
        if form.password.data != form.confirm.data:
            form.confirm.errors.append("Passwords do not match.")
            return render_template('signup.html', form=form)"""
        
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)


# logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ---------------------------------------------------------------------------
# Page routes (GET) -- render the HTML templates
# ---------------------------------------------------------------------------


#Home page route
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

#search page 
@app.route('/search', methods=['GET'])
def search():

    query = request.args.get('q', '')
    results = []

    if query:
        data = search_recipes(query)
        results = data.get('results', [])

    return render_template('results.html', search_items=results, query=query)

'''
#Fridge page route - DEPRECATED
@app.route('/fridge', methods=['GET'])
def fridge_page():
    return render_template('fridge.html')

'''

@app.route('/favorites', methods=['GET'])
@login_required
def favorites_page():
    return render_template('favorites.html')

@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    #placeholder atm will make stats.html later
    return render_template('index.html')

#generic page for project details
@app.route('/about')
@app.route('/generic')
def generic_page():
    return render_template('generic.html')

"""
@app.route('/elements')
def elements_page():
    return render_template('elements.html')
"""



# ---------------------------------------------------------------------------
# API / form routes (POST) -- handle form submissions, return data
# ---------------------------------------------------------------------------

@app.route('/search', methods=['POST'])
def results():
    query = request.form.get('query') or request.form.get('q') or ''
    results = api.search_recipes(query, number=10)
    return results

'''
@app.route('/fridge', methods=['POST'])
def fridge():
    ingredients = request.form['ingredients']
    results = api.ingredient_search(ingredients)
    return results
'''
@app.route('/add_favorite', methods=['POST'])
@login_required
def add_favorite():
    # Get recipe_id from the hidden form field
    #print("DEBUG: Received form data: ", request.form)  # Debug print to check form data

    recipe_id = request.form.get('recipe_id')

    #print(f"DEBUG: Extracted recipe_id: {recipe_id}")  # Debug print to check extracted recipe_id

    if not recipe_id:
        flash('Invalid recipe.', 'danger')
        return redirect(request.referrer or url_for('index'))

    # Check if this favorite already exists to provide a clean UX
    user_id = current_user.id

    #print(f"DEBUG: Current user_id: {user_id}")  # Debug print to check current user_id

    existing_fav = Favorite.query.filter_by(
        user_id=user_id, 
        recipe_id=recipe_id
    ).first()

    if existing_fav:
        flash('This recipe is already in your favorites!', 'info')
    else:
        # Create new favorite record using your model's structure
        new_fav = Favorite(
            user_id=user_id, 
            recipe_id=recipe_id
            # date_added defaults to datetime.utcnow per your model
        )
        
        try:
            db.session.add(new_fav)
            db.session.commit()
            flash('Added to favorites!', 'success')
        except Exception as e:
            db.session.rollback()
            # This handles cases where the recipe_id might not exist in the recipes table
            flash('Error adding favorite. Ensure the recipe is saved first.', 'danger')

    return redirect(request.referrer or url_for('index'))
"""
@app.route('/similar/<int:recipe_id>')
def similar(recipe_id):
    results = api.get_similar_recipes(recipe_id)
    return results
"""
#recipe route for information display
#TODO: add function for checking database for downloaded recipe pre api call, and add to database if not present

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    result = get_recipe_information(recipe_id)

    existing_recipe = db.session.query(Recipe).filter_by(id=recipe_id).first()

    if not existing_recipe and result:
        new_recipe = Recipe(
            id=result.get('id'),
            data=result
        )
        try:
            db.session.add(new_recipe)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving recipe to database: {e}")
    #debug print statement to verify recipe data is being retrieved correctly        
    #print("result: ", result)
    return render_template('recipe.html', recipe=result)



"""
@app.route('/joke')
def joke():
    # joke = api.get_random_joke()
    return "joke"

"""
# ---------------------------------------------------------------------------
# Static assets -- the Hyperspace template references /assets/... and
# /images/... relative to the HTML files, which live in templates/. Serve
# them directly from there.
# ---------------------------------------------------------------------------

"""
@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'assets'), path)


@app.route('/images/<path:path>')
def images(path):
    return send_from_directory(os.path.join(TEMPLATES_DIR, 'images'), path)
"""

if __name__ == '__main__':
    app.run(debug=True)

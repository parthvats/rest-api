from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
print(database_url)
# PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Recipe model
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    making_time = db.Column(db.String(50), nullable=False)
    serves = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# Create the database tables
with app.app_context():
    db.create_all()

# POST /recipes - Create a new recipe
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']

    if not data or not all(field in data and data[field] for field in required_fields):
        return jsonify({
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }), 400

    new_recipe = Recipe(
        title=data['title'],
        making_time=data['making_time'],
        serves=data['serves'],
        ingredients=data['ingredients'],
        cost=data['cost']
    )
    db.session.add(new_recipe)
    db.session.commit()

    recipe_data = {
        "id": new_recipe.id,
        "title": new_recipe.title,
        "making_time": new_recipe.making_time,
        "serves": new_recipe.serves,
        "ingredients": new_recipe.ingredients,
        "cost": new_recipe.cost,
        "created_at": new_recipe.created_at,
        "updated_at": new_recipe.updated_at,
    }

    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": [recipe_data]
    }), 201

# GET /recipes - Retrieve all recipes
@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    recipes_list = [
        {
            "id": recipe.id,
            "title": recipe.title,
            "making_time": recipe.making_time,
            "serves": recipe.serves,
            "ingredients": recipe.ingredients,
            "cost": recipe.cost
        }
        for recipe in recipes
    ]
    return jsonify({"recipes": recipes_list}), 200

# GET /recipes/<id> - Retrieve a specific recipe by ID
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "making_time": recipe.making_time,
        "serves": recipe.serves,
        "ingredients": recipe.ingredients,
        "cost": recipe.cost
    }
    return jsonify({
        "message": "Recipe details by id",
        "recipe": [recipe_data]
    }), 200

# PATCH /recipes/<id> - Update a recipe by ID
@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    data = request.get_json()
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']

    if not data or not all(field in data and data[field] for field in required_fields):
        return jsonify({
            "message": "Recipe update failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }), 400

    recipe.title = data['title']
    recipe.making_time = data['making_time']
    recipe.serves = data['serves']
    recipe.ingredients = data['ingredients']
    recipe.cost = data['cost']
    db.session.commit()

    updated_recipe = {
        "id": recipe.id,
        "title": recipe.title,
        "making_time": recipe.making_time,
        "serves": recipe.serves,
        "ingredients": recipe.ingredients,
        "cost": recipe.cost
    }
    return jsonify({
        "message": "Recipe successfully updated!",
        "recipe": [updated_recipe]
    }), 200

# DELETE /recipes/<id> - Delete a recipe by ID
@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe successfully removed!"}), 200

if __name__ == '__main__':
    app.run(debug=True)

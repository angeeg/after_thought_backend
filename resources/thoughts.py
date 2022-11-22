import models
from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

thought = Blueprint('thoughts', 'thought')

# GET - index, get all thoughts in a category 
@thought.route('category/<id>', methods=['GET'])
def thoughts_index(id):
    category = models.Category.get_by_id(id)
    query = models.Thought.select().where(category.id == id) 
    thoughts = query.execute()
    thought_dicts = [model_to_dict(thought) for thought in thoughts]
    
    return jsonify(
        data=thought_dicts,
        message=f'Found all thoughts in {category.name} category.',
        status=200
    ), 200

# POST - create a thought and thought property for its category
@thought.route('category/<id>', methods=['POST'])
def create_thought(id):
    payload = request.get_json()
    category = models.Category.get_by_id(id)
    new_thought = models.Thought.create(category=category.id, body=payload['body'])
    thought_dict = model_to_dict(new_thought)

    return jsonify(
        data=thought_dict,
        message=f'New thought was added under the {category.name}.category',
        status=201
    ), 201

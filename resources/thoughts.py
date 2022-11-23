import models
from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

thought = Blueprint('thoughts', 'thought')

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

# GET - index, get all thoughts in a category 
@thought.route('category/<id>', methods=['GET'])
def thoughts_index(id):
    thought_cat = models.Category.get_by_id(id)
    print('id:', thought_cat)
    thought = models.Thought
    print(thought)
    query = thought.select().where(thought.category == thought_cat) 
    thoughts = query.execute()
    print(query)
    thought_dicts = [model_to_dict(thought) for thought in thoughts]
    
    return jsonify(
        data=thought_dicts,
        message=f'Found {len(thought_dicts)} thoughts in {thought_cat.name} category.',
        status=200
    ), 200

# GET - get single thought by id 
@thought.route('/<id>', methods=['GET'])
def single_thought(id):
    thought = models.Thought.get_by_id(id)
    single_thought = model_to_dict(thought)
    return jsonify(
        data=single_thought,
        message='Thought found!',
        status=200
    ), 200

# PUT - edit thought 
@thought.route('/<id>', methods=['PUT'])
def edit_thought(id):
    payload = request.get_json()
    thought = models.Thought
    query = thought.update(**payload).where(thought.id == id) 
    query.execute()
    return jsonify(
        data=model_to_dict(thought.get_by_id(id)),
        message=f'Thought {thought.id} updated successfully!',
        status=200
    ), 200

# DELETE - delete single thought 
@thought.route('/<id>', methods=['DELETE'])
def delete_thought(id):
    thought = models.Thought
    query = thought.delete().where(thought.id == id)
    query.execute()
    return jsonify(
        data='Thought has been deleted',
        message='Thought successfully deleted!',
        status=200
    ), 200

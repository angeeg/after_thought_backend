import models
from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

thought = Blueprint('thoughts', 'thought')

# GET - index, get all thoughts 
@thought.route('/', methods=['GET'])
def thoughts_index():
    result = models.Thought.select()
    current_user_thoughts_dicts = [model_to_dict(thought) for thought in models.Thought]
    
    return jsonify(
        data=current_user_thoughts_dicts,
        message=f'Found all thoughts in {models.Thought.category.name} category.',
        status=200
    ), 200
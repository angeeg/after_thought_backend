import models
from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

category = Blueprint('categories', 'category')

# GET - index route - get all categories
@category.route('/', methods=['GET'])
def category_index():
    result = models.Category.select()
    current_user_categories_dicts = [model_to_dict(category) for category in current_user.categories]

    for category_dict in current_user_categories_dicts:
        category_dict['author'].pop('password')

    return jsonify(
        data=current_user_categories_dicts,
        message=f'Found {len(current_user_categories_dicts)} categories by {current_user.username}.',
        status=200
    ), 200

# POST - create a category
@category.route('/', methods=['POST'])
@login_required
def create_category():
    payload = request.get_json()
    category = models.Category.create(name=payload['name'], author=current_user.id)
    category_dict = model_to_dict(category)

    return jsonify(data=category_dict, status={'code':201, 'message': 'Success! A new category was created!'})

# PUT - edit category name 
@category.route('/<id>', methods=['PUT'])
def edit_category(id):
    payload = request.get_json()
    query = models.Category.update(**payload).where(models.Category.id == id)
    query.execute()
    return jsonify(data=model_to_dict(models.Category.get_by_id(id)), status=200, message='Category updated!')


# DELETE - delete category
@category.route('/<id>', methods=['DELETE'])
def delete_category(id):
    query = models.Category.delete().where(models.Category.id == id)
    query.execute()
    
    return jsonify(data='Category successfully deleted.', status=200, message='Category deleted!'), 200
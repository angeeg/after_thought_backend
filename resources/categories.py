import models
from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

category = Blueprint('categories', 'category')

# GET - index route - get all categories
@category.route('/', methods=['GET'])
def get_all_categories():
    try:    
        categories = [model_to_dict(category) for category in models.Category.select()]
        print(categories)
        return jsonify(data=categories, status={'code':200, 'message':'Success! Found all categories.'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code':401, 'message':'Error - cannot get categories.'})

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
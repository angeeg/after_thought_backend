import models
from flask import Blueprint, jsonify, request 
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user, login_required

user = Blueprint('users', 'user')

# POST - create a user
@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        # make sure user doesn't already exist
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={'code':401, 'message':'A user with that name already exists.'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        # start user session 
        login_user(user)

        user_dict = model_to_dict(user)
        del user_dict['password']
        return jsonify(data=user_dict, status={'code':201, 'message':f'Success! User {user.username} created.'})

# POST - login user 
@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    try:
        # try to find user by email 
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            # set up the user session 
            login_user(user)
            return jsonify(data=user_dict, status={'code': 200, 'message': f'Success, {user.username} is logged in!'}), 200
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Username or password is incorrect.'}), 401
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Username or password is incorrect.'}), 401

# GET - get logged in user data 
@user.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
    print(current_user)
    print(f'{current_user.username} is the current logged in user')
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
    return jsonify(data=user_dict), 200

# GET - logout user 
@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify(data={}, status=200, message='User is now logged out')


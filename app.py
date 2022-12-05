# importing blueprints 
from resources.users import user
from resources.categories import category 
from resources.thoughts import thought
from resources.quick_thoughts import quick_thought
# import from dependencies
from flask import Flask, jsonify, after_this_request
import models
from flask_login import LoginManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv() # grab varianles from .env file 


DEBUG = True 
PORT = os.environ.get('PORT')

# initialize instance of Flask class, this will start the website
app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'hi'

app.secret_key = os.environ.get('SECRET_KEY')

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None 

CORS(user, origins=['http://localhost:3000', 'https://after-thought-capstone.herokuapp.com/'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/after-thought/v1/users')
CORS(category, origins=['http://localhost:3000', 'https://after-thought-capstone.herokuapp.com/'], supports_credentials=True)
app.register_blueprint(category, url_prefix='/after-thought/v1/categories')
CORS(thought, origins=['http://localhost:3000', 'https://after-thought-capstone.herokuapp.com/'], supports_credentials=True)
app.register_blueprint(thought, url_prefix='/after-thought/v1/thoughts')
CORS(quick_thought, origins=['http://localhost:3000]', 'https://after-thought-capstone.herokuapp.com/'], supports_credentials=True)
app.register_blueprint(quick_thought, url_prefix='/after-thought/v1/quick_thoughts')

# we don't want to hog up the SQL connection pool
# so we should connect to the DB before every request
# and close the db connection after every request

@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                  # (in our case this will be some JSON)

# ADD THESE THREE LINES -- because we need to initialize the
# tables in production too!
if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
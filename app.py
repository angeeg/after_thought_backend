from flask import Flask, jsonify
import models
# importing blueprints 
from resources.users import user
from resources.categories import category 
from resources.thoughts import thought
from resources.quick_thoughts import quick_thought
from flask_cors import CORS


DEBUG = True 
PORT = 8000

# initialize instance of Flask class, this will start the website
app = Flask(__name__)

@app.route('/')
def index():
    return 'hi'


CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/after-thought/v1/users')
CORS(category, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(category, url_prefix='/after-thought/v1/categories')
CORS(thought, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(thought, url_prefix='/after-thought/v1/thoughts')
CORS(quick_thought, origins=['http://localhost:3000]'], supports_credentials=True)
app.register_blueprint(quick_thought, url_prefix='/after-thought/v1/quick_thoughts')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
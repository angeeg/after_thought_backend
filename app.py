from flask import Flask, jsonify

import models


DEBUG = True 
PORT = 8000

# initialize instance of Flask class, this will start the website
app = Flask(__name__)

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
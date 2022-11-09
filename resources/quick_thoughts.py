import models
from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict

quick_thought = Blueprint('quick_thoughts', 'quick_thought')
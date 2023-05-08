from flask import request, Blueprint
from recommendationapp.funcs import create_user, find_user

users = Blueprint('users', __name__)

@users.route('/register_user', methods=['POST'])
def register_user():
    registration_msg, code = create_user(request.json)
    return registration_msg, code
    
@users.route('/get_user')
def get_user():
    search_msg, code = find_user(request.json)
    return search_msg, code
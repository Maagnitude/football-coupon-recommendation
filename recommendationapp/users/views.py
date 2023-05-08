from flask import request, Blueprint
from recommendationapp.funcs import create_user, find_user, find_all_users

users = Blueprint('users', __name__)

@users.route('/register_user', methods=['POST'])
def register_user():
    return create_user(request.json)
    
@users.route('/get_user')
def get_user():
    return find_user(request.json)

@users.route('/get_all_users')
def get_all_users():
    return find_all_users()
from flask import request, Blueprint
from recommendationapp.funcs import create_user, find_user, find_all_users
from recommendationapp import db
from sqlalchemy.orm import sessionmaker

users = Blueprint('users', __name__)

@users.route('/register_user', methods=['POST'])
def register_user():
    Session = sessionmaker(bind=db.engine)
    batch_session = Session()
    json = request.get_json()
    print(json)
    result = create_user(json, batch_session)  
    batch_session.close()
    return {"result": result[-1]}
    
@users.route('/get_user')
def get_user():
    return find_user(request.json)

@users.route('/get_all_users')
def get_all_users():
    return find_all_users()
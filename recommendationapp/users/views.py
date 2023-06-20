from flask import request, Blueprint, jsonify
from recommendationapp.funcs import create_user, find_user, find_all_users
from recommendationapp import db
from sqlalchemy.orm import sessionmaker
from recommendationapp.models import User, Event, Coupon, Odd

users = Blueprint('users', __name__)

@users.route('/register_user', methods=['POST'])
def register_user():
    Session = sessionmaker(bind=db.engine)
    batch_session = Session()
    json = request.get_json()
    result = create_user(json, batch_session)  
    batch_session.close()
    return {"result": result[-1]}
    
@users.route('/get_user')
def get_user():
    return find_user(request.json)

@users.route('/get_all_users')
def get_all_users():
    return find_all_users()

# DELETES ALL ROWS FROM ALL TABLES (But not the tables themselves)
@users.route('/api/delete_all_rows', methods=['DELETE'])
def delete_all_rows():
    try:
        db.session.query(User).delete()
        db.session.query(Event).delete()
        db.session.query(Odd).delete()
        db.session.query(Coupon).delete()
        db.session.commit()
        return jsonify({'message': 'All rows deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})
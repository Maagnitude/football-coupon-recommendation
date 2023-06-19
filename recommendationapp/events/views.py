from flask import request, Blueprint
from recommendationapp.funcs import create_event, find_event, find_all_events, create_odds, find_all_odds
from recommendationapp import db
from sqlalchemy.orm import sessionmaker

events = Blueprint('events', __name__)

@events.route('/register_event', methods=['POST'])
def register_event():
    Session = sessionmaker(bind=db.engine)
    batch_session = Session()
    json_data = request.get_json()
    result = create_event(json_data, batch_session)  
    batch_session.close()
    return {"result": result[-1]}

@events.route('/get_event')
def get_event():
    return find_event(request.json)

@events.route('/get_all_events')
def get_all_events():
    return find_all_events()

@events.route('/register_odds', methods=['POST'])
def register_odds():
    Session = sessionmaker(bind=db.engine)
    batch_session = Session()
    json_data = request.get_json()
    result = create_odds(json_data, batch_session)  
    batch_session.close()
    return {"result": result[-1]}

@events.route('/get_odds')
def get_all_odds():
    return find_all_odds()
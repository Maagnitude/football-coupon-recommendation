from flask import request, Blueprint
from recommendationapp.funcs import create_event, find_event, find_all_events
from recommendationapp import db
from sqlalchemy.orm import sessionmaker

events = Blueprint('events', __name__)

@events.route('/register_event', methods=['POST'])
def register_event():
    Session = sessionmaker(bind=db.engine)
    batch_session = Session()
    json = request.json
    result = create_event(json, batch_session)  
    batch_session.close()
    
    if isinstance(result, tuple):
        status_code = result[-1]
        return json, status_code
    else:
        return json, 200

@events.route('/get_event')
def get_event():
    return find_event(request.json)

@events.route('/get_all_events')
def get_all_events():
    return find_all_events()
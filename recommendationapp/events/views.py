from flask import request, Blueprint, jsonify, render_template
from recommendationapp.funcs import create_event, find_event, find_all_events, create_odds, find_all_odds
from recommendationapp import db
from sqlalchemy.orm import sessionmaker
import json

events = Blueprint('events', __name__, template_folder='templates/events')

@events.route('/register_event', methods=['POST'])
def register_event():
    Session = sessionmaker(bind=db.engine)
    batch_session = Session()
    json_data = request.get_json()
    result = create_event(json_data, batch_session)  
    batch_session.close()
    return {"result": result[-1]}

@events.route('/api/get_event')
def api_get_event():
    return find_event(request.json)

@events.route('/get_all_events')
def get_all_events():
    events = find_all_events()[0]
    odds = find_all_odds()[0]
    json_response = jsonify(events)
    print(odds[0])

    # Render HTML template by default
    return render_template('events.html', events=events, odds=odds, json_response=json_response)

@events.route('/api/get_all_events')
def api_get_all_events():
    events = find_all_events()[0]
    json_response = jsonify(events)

    # Render HTML template by default
    return json_response

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
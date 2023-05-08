from flask import request, Blueprint
from recommendationapp.funcs import create_event, find_event, find_all_events

events = Blueprint('events', __name__)

@events.route('/register_event', methods=['POST'])
def register_event():
    return create_event(request.json)

@events.route('/get_event')
def get_event():
    return find_event(request.json)

@events.route('/get_all_events')
def get_all_events():
    return find_all_events()
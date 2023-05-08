from flask import request, Blueprint
from recommendationapp.funcs import create_event, get_event

events = Blueprint('events', __name__)

@events.route('/register_event', methods=['POST'])
def register_event():
    registration_msg, code = create_event(request.json)
    return registration_msg, code

@events.route('/events')
def get_events():
    user, events = get_event()
    return
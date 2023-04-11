from flask import render_template, Blueprint
from recommendationapp.funcs import get_event

events = Blueprint('events', __name__)

@events.route('/events')
def get_events():
    user, events = get_event()
    return render_template('events.html', user=user, events=events)
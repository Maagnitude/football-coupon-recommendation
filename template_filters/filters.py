from recommendationapp import app

# To get the enumerate function in jinja2 (for event index)
@app.template_filter('enumerate')
def jinja2_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)

# To get the odds for a given event in Jinja2
@app.template_filter('get_odds')
def get_odds(event_id, odds):
    matching_odd = next((odd['odds'] for odd in odds if odd['event_id'] == event_id), None)
    return matching_odd

@app.template_filter('get_event_participants')
def get_event_participants(event_id, events):
    matching_event = next((event['participants'] for event in events if event['event_id'] == event_id), None)
    return matching_event

@app.template_filter('multiply')
def multiply(values):
    result = 1
    for value in values:
        result *= float(value)
    return result
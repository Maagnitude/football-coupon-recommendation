from recommendationapp import app
import subprocess
from jinja2 import Environment

# Run the loader.py script
# @app.before_first_request
# def run_loader():
#     subprocess.Popen(['python', 'recommendationapp/teams/loader.py'])

# To get the enumerate function in jinja2 (for event index)
@app.template_filter('enumerate')
def jinja2_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)

# To get the odds for a given event in Jinja2
@app.template_filter('get_odds')
def get_odds(event_id, odds):
    matching_odd = next((odd['odds'] for odd in odds if odd['event_id'] == event_id), None)
    return matching_odd

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
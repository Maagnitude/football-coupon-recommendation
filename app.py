from recommendationapp import app
import subprocess
from template_filters.filters import jinja2_enumerate, get_odds, get_event_participants, multiply

# Run the loader.py script
@app.before_first_request
def run_loader():
    subprocess.Popen(['python', 'recommendationapp/teams/loader.py'])
    
app.add_template_filter(jinja2_enumerate)
app.add_template_filter(get_odds)
app.add_template_filter(get_event_participants)
app.add_template_filter(multiply)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
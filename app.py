from recommendationapp import app
import subprocess

# Run the loader.py script
@app.before_first_request
def run_loader():
    subprocess.Popen(['python', 'recommendationapp/teams/loader.py'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
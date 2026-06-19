import requests
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

API = 'http://localhost:5000'
SELF = 'http://localhost:5001'

task_ids = []
statuses = {}

@app.route('/')
def index():
    # for tid in task_ids:
    #     statuses[tid] = requests.get(f'{API}/task/{tid}').json()
        
    tasks = [(tid, statuses[tid]['status'], statuses[tid]['result']) for tid in task_ids]
    return render_template('index.html', tasks=tasks)

@app.route('/submit', methods=['POST'])
def submit():
    n1 = int(request.form['number1'])
    n2 = int(request.form['number2'])
    
    callaback_url = f'{SELF}/callback'
    
    response = requests.post(f'{API}/task', json={'number1': n1, 'number2': n2, 'callback_url': callaback_url})
    
    data = response.json()
    
    task_ids.append(data['task_id'])
    statuses[data['task_id']] = data
    
    return redirect('/')

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    statuses[data['task_id']] = data
    
    return '', 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
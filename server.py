import uuid
import time
import random
import threading

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = {}

def process(task_id, n1, n2, callback_url):
    time.sleep(random.randint(5, 15))
    
    try: 
        result = n1 / n2
        tasks[task_id] = {'status': 'SUCCESS', 'result': result}
    except ZeroDivisionError:
        tasks[task_id] = {'status': 'FAILED', 'result': 'Division by zero is not allowed.'}
        
    time.sleep(2)
    
    if callback_url:
        try:
            requests.post(callback_url, json={'task_id': task_id, **tasks[task_id]})
        except requests.RequestException:
            pass
        
@app.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()
    n1 = data['number1'] # Assuming n1 and n2 are provided in the request body and if not get exception
    n2 = data['number2']
    callback_url = data.get('callback_url') # Optional callback URL for task completion notification if not provided get None
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'PENDING', 'result': None}
    
    threading.Thread(target=process, args=(task_id, n1, n2, callback_url)).start()
    
    return jsonify({'task_id': task_id, **tasks[task_id]}), 202

@app.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    time.sleep(2)  # Simulate processing delay
    
    task = tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task), 200

if __name__ == '__main__':
    app.run(debug=True)
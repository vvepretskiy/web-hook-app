# Web Hook App

Simple demo of a webhook-based task processor: a client web UI creates background tasks on a processing service; when a task completes the processor calls back the client (webhook) with the result.

This repository contains two small Flask apps:

- server.py — processing service that accepts tasks, performs a simulated job (division), and calls a callback URL when done.
- client.py — web UI that creates tasks on the processing service and receives webhook callbacks to update in-memory task state.

This is intended for local development and learning how webhooks, callbacks, and simple async processing can work together.

## Features
- Create a task from a browser form (number1 / number2).
- Background processing with simulated delay and error handling (division by zero).
- Optional callback URL: server posts result back to client when task completes.
- Browser UI lists tasks and shows status/result (server-side in-memory state).

## Requirements
- Python 3.8+
- pip

Install dependencies:
```
pip install -r requirements.txt
```
If you don't have a requirements.txt, install:
```
pip install flask requests
```

## Files
- server.py — processing service (default runs on port 5000).
- client.py — simple web client and webhook receiver (default runs on port 5001).
- templates/index.html — (used by client.py) simple form and table to show tasks. (Create a templates/ folder and place index.html there.)

## How it works (high level)
1. The browser (client.py) submits a POST to server.py /task with JSON:
   { number1, number2, callback_url }.
2. server.py generates a task_id, stores a PENDING entry, and starts a background thread to process the task.
3. When processing finishes (or fails), server.py posts to the provided callback_url with JSON:
   { task_id, status: SUCCESS|FAILED, result }.
4. client.py exposes /callback which receives that webhook and updates its in-memory statuses for display.

Note: Both apps keep state in memory (dictionaries). This is only suitable for demos/local dev.

## Run locally 

1. Start the processing service (server.py) on port 5000:
```
python server.py
```

2. In a second terminal start the client/webhook receiver (client.py) on port 5001:
```
python client.py
```

3. Open the client UI:
- Visit http://localhost:5001
- Submit numbers to create tasks.
- The server will process the task in background and POST to /callback on the client. The client stores status in memory and the UI will show values on reload.

## Example usage
- Submit number1=10 and number2=2 → eventually the task status becomes SUCCESS and result 5.0.
- Submit number1=5 and number2=0 → task status becomes FAILED and result explains division by zero.

## Limitations and notes
- In-memory storage: both apps use Python dicts. Data is lost when processes restart.
- client.py does not push real-time updates to the browser automatically — you must refresh the page to see updated task states, or extend the client with polling/SSE/WebSockets to update automatically (see Ideas).
- server.py uses background threads and time.sleep to simulate asynchronous processing — not production-ready.
- No authentication or input validation beyond minimal checks. Do not expose these apps to untrusted networks.

## Optional improvements / next steps
- Use Server-Sent Events (SSE) or WebSockets in client.py to push updates to connected browsers when callback arrives.
- Persist tasks in a database (SQLite, PostgreSQL) instead of in-memory dicts.
- Use a task queue (Celery / RQ) for more robust background processing.
- Add logging and better error handling for webhook POST failures and timeouts.
- Add unit tests and Dockerfiles for containerized runs.

## Troubleshooting
- "requests" import error: ensure requests is installed in the same Python environment used to run the app:
  ```
  pip install requests
  ```
- Port conflicts: if ports 5000 or 5001 are in use, change the port in app.run() calls and update the API/SELF constants accordingly.
- Webhook unreachable: the processing server must be able to reach the callback URL (from its network). For cross-host testing use ngrok or similar to expose a public URL.

## License
This is a small demo — add your preferred license file if you intend to share.

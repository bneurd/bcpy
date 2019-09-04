from flask import Flask, request
from flask_cors import CORS
import socketio
from threading import Thread
import logging

sio = socketio.Server(async_mode='threading', cors_allowed_origins='*')
app = Flask(__name__)
CORS(app)
app.config.debug = False
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('eeg_data')
def my_custom_event(sid, data):
    sio.emit('eeg', data, skip_sid=sid)


def run():
    try:
        app.run()
    except Exception as ex:
        print(ex)
        exit(1)


def start_server():
    server_thread = Thread(target=run)
    server_thread.start()
    return server_thread

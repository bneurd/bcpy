from flask import Flask, render_template, send_from_directory, request
import socketio
from os import path
from threading import Thread
import logging

sio = socketio.Server(async_mode='threading')
web_dir = path.abspath(path.join(path.dirname(__file__), '../web'))
app = Flask(__name__, template_folder=web_dir)
# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config.debug = False
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/')
def sessions():
    return render_template('index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(path.join(web_dir, 'js'), path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(path.join(web_dir, 'css'), path)


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

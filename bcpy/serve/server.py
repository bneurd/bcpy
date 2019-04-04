from flask import Flask, render_template, send_from_directory, request
from os.path import abspath, join, dirname
from threading import Thread
import logging
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

web_dir = abspath(join(dirname(__file__), '../web'))
app = Flask(__name__, template_folder=web_dir)
# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config.debug = False

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
    return send_from_directory(join(web_dir, 'js'), path)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def run():
    try:
        app.run()
    except Exception as ex:
        print(ex)
        exit(1)


def start_server():
    server_thread = Thread(target=run)
    server_thread.start()
    return socket

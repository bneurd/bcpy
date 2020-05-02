from . import properties
from signal import signal, SIGINT


def _interrupt_gracefully(signal_received=None, frame=None):
    print("\nStopping...")
    props = properties.Properties()
    server = props.realtime_inst
    if server and server.stop:
        server.stop()
    props.running = False


def handle_stop_signal():
    signal(SIGINT, _interrupt_gracefully)

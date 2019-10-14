from . import properties
from signal import signal, SIGINT


def _interrupt_gracefully(signal_received, frame):
    print("\nStopping...")
    props = properties.Properties()
    server = props.realtime_inst
    server.stop()
    props.running = False


def handle_stop_signal():
    signal(SIGINT, _interrupt_gracefully)

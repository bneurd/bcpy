import sys
import multiprocessing
from . import properties
from signal import signal, SIGINT


def _interrupt_gracefully(signal_received, frame):
    print("\nStopping...")
    props = properties.Properties()

    props.running = False


def clean_all_process():
    for process in multiprocessing.active_children():
        process.kill()
    sys.exit(0)


def handle_stop_signal():
    signal(SIGINT, _interrupt_gracefully)

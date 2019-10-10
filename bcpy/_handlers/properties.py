from ..common import singleton


class Properties(metaclass=singleton.Singleton):
    def __init__(self):
        self.running = True
        self.realtime_inst = None


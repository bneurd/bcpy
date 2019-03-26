from .signalacquisition import OpenBCIAcquisition


class Connection():
    def __init__(self, board, channels, frequency=None, show_data=True):
        if board == "openBCI":
            if len(channels) < 8:
                f = 250
            else:
                f = 125

            self.Con = OpenBCIAcquisition(f, channels, print_data=show_data)
    
    def listen(self):
        self.Con.get_data()


import requests

class Room:

    def __init__(self, id, backend, duration=5):

        self.id = id
        self.backend = backend
        self.co2 = 0
        self.humidity = 0.0
        self.automatic = 0
        self.open = 0
        self.force = 0
        self.windows = []
        self.starttime = None
        self.duration = duration

    def __str__(self):
        s = f'Room: {self.id}\n'
        s += f'Backend: {self.backend}\n'
        s += f'Automatic: {self.automatic}\n'
        return s

    def load_config():
        pass

    def set_control():
        if self.force != self.open:
            override_windows()

    def override_windows(self):
        if not close_required():
            for window in windows:
                window.force_open()
        else:
            pass

    def push_update():
        pass
    
    def add_window(self, window):
        self.windows.append(window)

    def start_timer(self):
        self.start_time = now() 

    def close_required():
        if start_time is None:
            return False
        if start_time + duration < now():
            return True
        return False
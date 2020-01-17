
import requests
import json

class Room:

    def __init__(self, id, backend, duration=5):
        self.id = id
        self.backend = f'{backend}/room/control'
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
        s += f'Force: {self.force}\n'
        s += f'Open: {self.open}\n'
        s += f'Duration: {self.duration}\n'
        for window in self.windows:
            s += str(window)
        return s

    def get_update(self):
        params = {'token': self.id,}
        resp = requests.get(self.backend, params=params)
        if resp.status_code == 200:
            body = resp.json()
            self.automatic = int(body.get('automatic_enable', 0))
            self.force = int(body.get('is_open', 0))
        for window in self.windows:
            window.get_update()

    def set_update(self):
        params = {'token': self.id}
        room = {}
        room['is_open'] = self.open
        room['co2'] = self.co2
        room['humidity'] = self.humidity
        requests.put(self.backend, params=params, json=room)
        for window in self.windows:
            window.set_update()
    
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
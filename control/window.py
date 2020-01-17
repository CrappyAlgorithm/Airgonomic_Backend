import requests
import json

class Window:

    def __init__(self, id, room_id, backend):
        self.id = id
        self.room_id = room_id
        self.backend = f'{backend}/window/control'
        self.automatic = 0
        self.open = 0

    def __str__(self):
        s = f'Window: {self.id}\n'
        s += f'Backend: {self.backend}\n'
        s += f'Automatic: {self.automatic}\n'
        s += f'Open: {self.open}\n'
        return s

    def get_update(self):
        params = {'token': self.room_id,}
        resp = requests.get(self.backend, params=params, json={'id':self.id,})
        if resp.status_code == 200:
            body = resp.json()
            self.automatic = int(body.get('automatic_enable', 0))

    def set_update(self):
        params = {'token': self.room_id}
        window = {}
        window['id'] = self.id
        window['is_open'] = self.open
        requests.put(self.backend, params=params, json=window)

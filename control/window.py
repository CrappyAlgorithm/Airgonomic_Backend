import requests
import json

class Window:

    def __init__(self, id, room_id, backend):
        self.id = id
        self.room_id = room_id
        self.backend = f'{backend}/window/control'
        self.automatic = 1
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

    def change_state(self, to_state):
        if to_state == self.open:
            print('State already set.')
            return
        if self.automatic == 1:
            self.open = 1 if self.open == 0 else 0
            if self.open == 1:
                print(f'Window{self.id} will be opened.')
            else:
                print(f'Window{self.id} will be closed.')
        else:
            print(f'Window{self.id} automatic disabled')
            
def register_new_window(backend, room_id):
    params = {'token': room_id}
    resp = requests.post(f'{backend}/window/control', params=params)
    if resp.status_code == 201:
        body = resp.json()
        if body is not None:
            id = int(body.get('id', 0))
            return Window(id, room_id, backend)
    return None

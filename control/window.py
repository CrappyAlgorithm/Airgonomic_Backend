import requests
import json
import logging as log
from led_handler import open_window, close_window

class Window:

    def __init__(self, id, room_id, backend, gpio):
        self.id = id
        self.room_id = room_id
        self.backend = f'{backend}/window/control'
        self.gpio = gpio
        self.automatic = 0
        self.open = 0

    def __str__(self):
        s = f'Window: {self.id}\n'
        s += f'Backend: {self.backend}\n'
        s += f'Automatic: {self.automatic}\n'
        s += f'Open: {self.open}\n'
        return s

    def get_update(self):
        log.info(f'Get update for window {self.id}')
        params = {'token': self.room_id,}
        resp = requests.get(self.backend, params=params, json={'id':self.id,})
        if resp.status_code == 200:
            body = resp.json()
            self.automatic = int(body.get('automatic_enable', 0))
        else:
            log.error(f'Update for window {self.id} not possible')

    def set_update(self):
        log.info(f'Set update for window {self.id}')
        params = {'token': self.room_id}
        window = {}
        window['id'] = self.id
        window['is_open'] = self.open
        resp = requests.put(self.backend, params=params, json=window)
        if resp.status_code != 200:
            log.error(f'Cannot set update for window {self.id}')

    def change_state(self, to_state):
        if to_state == self.open:
            log.info(f'State {self.open} already set to window {self.id}.')
            return
        if self.automatic == 1:
            self.open = 1 if self.open == 0 else 0
            if self.open == 1:
                log.info(f'Window {self.id} will be opened.')
                open_window(self.gpio)
            else:
                log.info(f'Window {self.id} will be closed.')
                close_window(self.gpio)
        else:
            log.info(f'Window {self.id} automatic disabled')
            
    def get_configuration(self, index):
        return f'window_{index},{self.id},{self.gpio}\n'

def register_new_window(backend, room_id, gpio):
    params = {'token': room_id}
    resp = requests.post(f'{backend}/window/control', params=params)
    if resp.status_code == 201:
        body = resp.json()
        if body is not None:
            id = int(body.get('id', 0))
            log.info(f'New window with id: {id} registerd.')
            return Window(id, room_id, backend, gpio)
    log.error('Register new window failed.')
    return None

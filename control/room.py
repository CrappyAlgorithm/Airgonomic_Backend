
import requests
import json
import logging as log
from window import Window
from sensors.read_t6613_co2 import read_co2

class Room:

    def __init__(self, id, backend):
        self.id = id
        self.backend_raw = backend
        self.backend = f'{backend}/room/control'
        self.co2 = 0
        self.humidity = 0.0
        self.automatic = 1
        self.open = 0
        self.force = 0
        self.windows = []
        self.override = False

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

    def get_id(self):
        return self.id

    def get_update(self):
        log.info(f'Get update for room {self.id}')
        params = {'token': self.id,}
        resp = requests.get(self.backend, params=params)
        if resp.status_code == 200:
            body = resp.json()
            self.automatic = int(body.get('automatic_enable', 0))
            self.force = int(body.get('is_open', 0))
            for window in self.windows:
                window.get_update()
            new_co2 = read_co2()
            if new_co2 is not None:
                self.co2 = new_co2
                log.info(f'New co2 value for room {self.id} is: {self.co2}ppm')
        else:
            log.info(f'Update of room {self.id} not possible.')

    def set_update(self):
        log.info(f'Set update for room {self.id}')
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

    def check_status(self):
        threshold = self.get_threshold()
        if self.force != self.open:
            self.override = not self.override
            self.open = 1 if self.open == 0 else 0
            log.info(f'Called force change for room: {self.id}')
            for window in self.windows:
                window.change_state(self.force)
        elif self.override:
            log.info('No change, override is active')
        elif self.automatic == 1 and int(threshold.get('automatic_enable')) == 1:
            log.info('Starting air value check.')
            change = False
            if self.open == 0:
                if self.co2 > int(threshold['co2']):
                    log.info('Co2 is over threshold')
                    change = True
                """
                if self.humidity > int(threshold['humidity']):
                    log.info('Humidity is over threshold')
                    change = True
                """
            elif self.open == 1:
                if self.co2 < int(threshold['co2']):
                    log.info('Co2 is under threshold')
                    change = True
                """
                if self.humidity < int(threshold['humidity']):
                    log.info('Humidity is under threshold')
                    change = True
                """
            if change:
                self.open = 1 if self.open == 0 else 0
                for window in self.windows:
                    window.change_state(self.open)
            else:
                log.info('No change required.')
        else:
            log.info('Automatic is disabled')

    def get_threshold(self):
        ret = {}
        params = {'token': self.id}    
        resp = requests.get(f'{self.backend_raw}/configuration/control', params=params)
        body = resp.json()
        if body is None:
            log.error(f'Cannot get threshold')
        return body

    def get_configuration(self):
        ret = f'backend,{self.backend_raw},\n'
        ret += f'room,{self.id},\n'
        id = 1
        for window in windows:
            ret += window.get_configuration(id)
            id += 1
        return ret

def register_new_room(backend, duration):
    resp = requests.post(f'{backend}/room/control')
    if resp.status_code == 201:
        body = resp.json()
        if body is not None:
            id = int(body.get('token', 0))
            log.info(f'New room with id: {id} registerd.')
            return Room(id, backend, duration)
    log.error('Register new room failed.')
    return None


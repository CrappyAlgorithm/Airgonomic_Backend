## @package control.window
#  @author Sebastian Steinmeyer
#  Handles the class Window and a funtion to register new windows.
import requests
import json
import logging as log
from led_handler import open_window, close_window

## Handles the functionality of a window.
#  This include getting and setting updates and open and close it.
class Window:

    ## Standart constructor to initiate a window with default values.
    #  Please call get_update after creating a window.
    #  @param self the object pointer
    #  @param id the window id in the backend
    #  @param room_id the id of the room which contains the window
    #  @param backend the ip and port of the used backend
    #  @param gpio the gpio pin for the led which simbolize the window
    def __init__(self, id, room_id, backend, gpio):
        self.id = id
        self.room_id = room_id
        self.backend = f'{backend}/window/control'
        self.gpio = gpio
        self.automatic = 0
        self.open = 0

    ## Get the window as string representation.
    #  @param self the object pointer
    #  @return the window as string
    def __str__(self):
        s = f'Window: {self.id}\n'
        s += f'Backend: {self.backend}\n'
        s += f'Automatic: {self.automatic}\n'
        s += f'Open: {self.open}\n'
        return s

    ## Updates the window with the data from the given backend.
    #  @param self the object pointer.
    def get_update(self):
        log.info(f'Get update for window {self.id}')
        params = {'token': self.room_id,}
        resp = requests.get(self.backend, params=params, json={'id':self.id,})
        if resp.status_code == 200:
            body = resp.json()
            self.automatic = int(body.get('automatic_enable', 0))
        else:
            log.error(f'Update for window {self.id} not possible')

    ## Pushes the window values to the given backend.
    #  @param self the object pointer
    def set_update(self):
        log.info(f'Set update for window {self.id}')
        params = {'token': self.room_id}
        window = {}
        window['id'] = self.id
        window['is_open'] = self.open
        resp = requests.put(self.backend, params=params, json=window)
        if resp.status_code != 200:
            log.error(f'Cannot set update for window {self.id}')

    ## Changes the window into the given state.
    #  If the state is already set or automatic is disabled, nothing will happen.
    #  @param self the object pointer
    #  @param to_state the targeted state
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

    ## Get the configuration of the window.
    #  @param self the object pointer
    #  @param index the window index related to the room
    #  @return the configuration as string       
    def get_configuration(self, index):
        return f'window_{index},{self.id},{self.gpio}\n'

## Registers a new window at the given backend.
#  @param backend the ip and port of the target backend as string
#  @param room_id the id of the window containing room
#  @param gpio the gpio pin of the used led
#  @return the created Window object or None in case of error
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

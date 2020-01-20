import csv
from room import Room, register_new_room
from window import Window, register_new_window
import requests

filename = 'config.txt'
target = ''

def parse_file(columns):
    conf = {}
    try:
        with open(filename) as csv_file:
            file = csv.reader(csv_file, delimiter=',')
            for row in file:
                val = []
                for i in range(1,columns):
                    val.append(row[i])
                conf[row[0]] = val
    except IndexError:
        print('To few columns in configuration file.')
    except FileNotFoundError:
        print(f'Configuration file "{filename}" not found.')
    return conf

def load_configuration():
    conf = parse_file(3)
    print(conf)
    backend = conf.get('backend', None)
    room = conf.get('room', None)
    window_count = conf.get('window_count', None)
    duration = conf.get('duration', None)
    sleep_duration = conf.get('sleep_duration', None)
    if backend is None:
        # start failed
        pass
    target = backend[0]
    if window_count is None:
        #missing window count
        pass
    window_count = int(window_count[0])
    if duration is None:
        # missing duration
        pass
    duration = int(duration[0])
    if sleep_duration is None:
        # missing sleep_duration
        pass
    sleep_duration = int(sleep_duration[0])
    if room is None:
        room = register_new_room(backend[0], duration)
        for i in range(1,window_count+1):
            window = register_new_window(backend[0], room.get_id())
            room.add_window(window)
            
    else:
        room_id = room[0]
        room = Room(int(room[0]), backend[0], int(duration))
        for i in range(1,window_count+1):
            window = conf.get(f'window_{str(i)}', None)
            if window is None:
                # error in config window_i
                print(f'window_{i} was not found.')
                pass
            else:
                window = Window(window[0], room_id, backend[0])
                room.add_window(window)
        
    return sleep_duration, room

def get_threshold(room_id):
    ret = {}
    params = {'token': room_id}    
    resp = requests.get(f'{target}/configuration/control', params=params)
    body = resp.json()
    if body is None:
        # error 
        pass
    return body
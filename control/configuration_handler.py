import csv
from room import Room, register_new_room
from window import Window, register_new_window
import logging as log
import sys

filename = 'config.txt'

def parse_file(columns):
    conf = {}
    try:
        with open(filename, "r") as csv_file:
            file = csv.reader(csv_file, delimiter=',')
            for row in file:
                val = []
                for i in range(1,columns):
                    val.append(row[i])
                conf[row[0]] = val
    except IndexError:
        log.error('To few columns in configuration file.')
        return None
    except FileNotFoundError:
        log.error(f'Configuration file "{filename}" not found.')
        return None
    return conf

def load_configuration():
    conf = parse_file(3)
    if conf is None:
        sys.exit(1)
    backend = conf.get('backend', None)
    room = conf.get('room', None)
    window_count = conf.get('window_count', None)
    sleep_duration = conf.get('sleep_duration', None)
    if backend is None:
        log.error('Parameter "backend" not found in configuration file.')
        sys.exit(1)
    target = backend[0]
    if window_count is None:
        log.error('Parameter "window_count" not found in configuration file.')
        sys.exit(1)
    window_count = int(window_count[0])
    if sleep_duration is None:
        log.error('Parameter "sleep_duration" not found in configuration file.')
        sys.exit(1)
    sleep_duration = int(sleep_duration[0])
    if room is None:
        log.info('Parameter "room" not found in configuration file. A new room will be created.')
        room = register_new_room(backend[0])
        for i in range(1,window_count+1):
            window = register_new_window(backend[0], room.get_id())
            room.add_window(window)
    else:
        room_id = room[0]
        room = Room(int(room[0]), backend[0])
        for i in range(1,window_count+1):
            window = conf.get(f'window_{str(i)}', None)
            if window is None:
                log.error(f'Parameter "window_{i}" not found in configuration file.')
                sys.exit(1)
            else:
                window = Window(window[0], room_id, backend[0])
                room.add_window(window)  
    return sleep_duration, room

def save_configuration(sleep_duration, room):
    with open(filename, "w") as file:
        file.write(f'sleep_duration,{sleep_duration},')
        file.write(room.get_configuration)


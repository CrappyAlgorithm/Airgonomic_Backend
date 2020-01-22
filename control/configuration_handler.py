## @package control.configuration_handler
#  @author Sebastian Steinmeyer
#  Handles the load and safe of configurations from file.
import csv
from room import Room, register_new_room
from window import Window, register_new_window
import logging as log
import sys

## The filename of the configuration file.
filename = 'config.txt'

## Read the configuration as a map with lists from file.
#
#  The seperator ist defined to ",".
#  @param columns the number of columns to read in each row.
#  @return a dictionary with a list of parsed values
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

## Parse the configuration and create rooms and windows based on it.
#
#  The values backend, window_count, sleep_duration and the window gpios
#  in form of window_i,,[gpio] need to be definded in the configuration file.
#  In case room is not given, a new room with given windows will be created.
#  Sample structure of the configuration file:
#  backend,<ip:port>:int,None
#  sleep_duration,<duration>:int,None
#  window_count,<count>:int,None
#  room,<id in the backend>:int,None
#  window_i,<is in the backend>:int,<gpio>:int
#
#  @return the parsed Room with the parsed Windows
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
            window_gpio = int(conf.get(f'window_{i}')[1])
            if window_gpio is None:
                log.error(f'No gpio for window_{i} found in configuration file')
                sys.exit(1)
            window = register_new_window(backend[0], room.get_id(), window_gpio)
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
                window = Window(window[0], room_id, backend[0], int(window[1]))
                room.add_window(window)  
    return sleep_duration, room

## Saves the configuration into configuration file.
#  @param sleep_duration the defined duration
#  @param room the room of type Room to get the configuration from
def save_configuration(sleep_duration, room):
    if sleep_duration is None or room is None:
        log.error('Configuration cannot be saved')
        return
    with open(filename, "w") as file:
        file.write(f'sleep_duration,{sleep_duration},\n')
        file.write(f'window_count,{room.get_window_count()},\n')
        file.write(room.get_configuration())


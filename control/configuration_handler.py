import csv
from room import Room

filename = 'control/config.txt'

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
    if backend is None:
        # start failed
        pass
    if window_count is None:
        #missing window count
        pass
    window_count = int(window_count[0])
    if duration is None:
        # missing duration
        pass
    duration = int(duration[0])
    if room is None:
        #register room and windows in backend
        pass
    else:
        room = Room(int(room[0]), backend[0], int(duration))
        """
        for i in range(0,window_count):
            window = conf.get(f'window_{str(i)}', None)
            if window is None:
                # error in config window_i
            window = Window(window[0], window[2], backend)
            room.add_window(window)
        """
    return room
    

room = load_configuration()
print(room)
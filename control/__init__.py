## @package control.__init__
#  Handles the start, close and runtime of the window control.
from time import sleep
import logging as log
import signal
from configuration_handler import load_configuration, save_configuration
from room import Room

log.basicConfig(filename='control.log', format='%(asctime)s-(%(process)d)-"Window-Control"-%(levelname)s: %(message)s', level=log.INFO)
sleep_duration, room = load_configuration()

## Handles the shutdown of the programm.
#
#  Saves the configuration and close all open windows.
def close(signum, frame):
    log.info('Programm will be terminated.')
    save_configuration(sleep_duration, room)
    room.close_all()
    exit(0)

signal.signal(signal.SIGINT, close)

## Handles the runtime of the programm.
def run():
    log.info('Window control started')
    while True:
        room.get_update()
        room.check_status()
        room.set_update()
        sleep(sleep_duration)

run()
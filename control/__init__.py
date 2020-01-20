from time import sleep
from configuration_handler import load_configuration
from room import Room
import logging

def run():
    logging.basicConfig(filename='control.log', format='%(asctime)s-%(process)d-%(message)s', level=logging.INFO)
    sleep_duration, room = load_configuration()
    while True:
        room.get_update()
        room.check_status()
        room.set_update()
        #sleep(sleep_duration)
        print('wait for input')
        input()

run()
## @package control.led_handler
#  Handles the functionallity to turn a led on and off. 
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## Turn on a led.
#  @param gpio the gpoi pin which should turn on.
def open_window(gpio):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)

## Turn off a led.
#  @param gpio the gpoi pin which should turn off.
def close_window(gpio):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.LOW)
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def open_window(gpio):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)

def close_window(gpio):
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.LOW)
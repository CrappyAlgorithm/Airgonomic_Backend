## @package control.sensors.read_bme280_hum
#  Handles the functionality to read the bme280 sensor
import bme280
import smbus2

port = 1
address = 0x77
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

## Reads the humidity of the bme280.
#  @return the humidity as floating point number
def read_humidity():
    bme280_data = bme280.sample(bus,address)
    return bme280_data.humidity
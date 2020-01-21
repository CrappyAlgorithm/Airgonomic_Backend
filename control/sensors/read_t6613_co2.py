## @package control.sensors.read_t6613_co2
#  Handles the functionality to read the t6613 sensor
from time import sleep
import serial
import struct

## Reads the co2 value of the t6613.
#  @return the co2 value as integer
def read_co2():
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    ser.isOpen()
    ser.write(bytes(b'\xFF\xFE\x02\x02\x03'))
    sleep(1)
    out=b''
    while ser.inWaiting() > 0:
        out += ser.read(5)
        if out != b'':
            value = struct.unpack_from(">h", out, offset=3)
            ser.close()
            return value[0]
    ser.close()
    return None

from serial.serialutil import SerialException
from xbee import ZigBee
import serial
import serial.serialutil
import sys
import time


def listen(response):
    try:
        print response
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as error:
        print error
        
    


try:
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600
    )
    xbee_conn = ZigBee(ser, callback=listen, error_callback=listen)
    print "connected"
    
    string = ''
    xbee_data = ''
    while True:
        
        
        try:
            #xbee_conn.wait_read_frame()
            time.sleep(0.001)
        #     character = ''
        #     character = ser.read()
        #     if character == '|':
        #         string += character
        #         xbee_data = string
        #         string = ''
        #         print xbee_data
        # print "loop"
        except KeyboardInterrupt:
            print "Keyboard Interrupt"
            break
        except Exception as error:
            print error
except SerialException as error:
    print error


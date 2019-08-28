from serial.serialutil import SerialException
from xbee import ZigBee
import serial
import serial.serialutil
import sys

def hex_to_ascii(hex_string):
	"""
	Used to convert hex string to ascii string
	:param hex_string:
	:return: ascii_string
	"""
	ascii_string = ''
	x = 0
	y = 2
	l = len(hex_string)
	while y <= l:
		ascii_string += chr(int(hex_string[x:y], 16))
		x += 2
		y += 2
	return ascii_string


try:
	ser = serial.Serial(
		port='/dev/ttyUSB0',
		baudrate=9600
	)
	xbee_conn = ZigBee(ser)
	
	ascii_receiver_mac_id = hex_to_ascii(str('0013A20041085E40').upper())
	response = xbee_conn.tx(frame_id="A", dest_addr_long=ascii_receiver_mac_id, dest_addr=b'\xFF\xFE', data=b'TEST_FRAME')
	xbee_conn.halt()
	ser.close()
	print "connected"
except SerialException as error:
	print error

# while True:
# 	try:
# 		print xbee_conn.wait_read_frame()
# 	#               time.sleep(0.001)
# 	# print "loop"
# 	except KeyboardInterrupt:
# 		print "Keyboard Interrupt"
# 		break
# 	except Exception as error:
# 		print error

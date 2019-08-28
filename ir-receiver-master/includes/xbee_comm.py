"""
To use this logger file
`from includes import xbee_comm`
"""
from serial.serialutil import SerialException
from includes.r2s_actions import tx_status, node_id_indicator, r2g_data_received, status
from xbee import ZigBee
import serial
import serial.serialutil
import sys
from includes import logger

import traceback
from config.global_config import global_config

ser = None
xbee_conn = None
log = logger.set_logger('xbee_comm')
		

def listen(response):
	global ser
	global xbee_conn
	try:
		# ser.flush()
		# ser.flushInput() # flush input buffer, discarding all its contents
		# ser.flushOutput() # flush output buffer, aborting current output and discard all that is in buffer
		
		switcher = {
			'tx_status': tx_status,
			'node_id_indicator': node_id_indicator,
			'rx': r2g_data_received,
			'status': status,
			'status1': status
		}
		
		devices = {}
		if global_config['simulator'] is True:
			from time import sleep
			response = {'id': 'rx', 'source_addr_long': '0013A2004104FF2B', 'rf_data': '  R101'}
			sleep(5)
		
		# Get the function from switcher dictionary
		func = switcher.get(response['id'], lambda: 'nothing')
		# Execute the function
		func(response)
	except KeyboardInterrupt:
		sys.exit(1)
	except Exception as error:
		log.error(traceback.format_exc())


class XBeeComm:
	def __init__(self, serial_port=global_config['serial_port'], baud_rate=global_config['serial_boud_rate']):
		global ser
		global xbee_conn
		try:
			ser = serial.Serial(
				port=serial_port,
				baudrate=baud_rate
			)
			# ser.flush()
			# ser.flushInput()  # flush input buffer, discarding all its contents
			# ser.flushOutput()  # flush output buffer, aborting current output and discard all that is in buffer
			xbee_conn = ZigBee(ser, callback=listen)
		except SerialException as error:
			log.error("Please check your serial connection with '" + serial_port + "'")
		# TODO: Tell server that something wrong with /dev/ttyUSB0
		except Exception as error:
			log.error(traceback.format_exc())
			sys.exit(1)
	
	def get_serial_data(self, data):
		pass
	
	def disconnect(self):
		global ser
		global xbee_conn
		if xbee_conn is not None:
			xbee_conn.halt()
		if ser is not None:
			ser.close()
			
	def disconnect_only_xbee(self):
		global xbee_conn
		if xbee_conn is not None:
			xbee_conn.halt()
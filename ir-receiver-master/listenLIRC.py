from includes import logger
from includes import xbee_comm
from includes.r2s_actions import tx_status, node_id_indicator, r2g_data_received, status
import serial
import serial.serialutil
from serial.serialutil import SerialException
from config.global_config import global_config
import traceback
import sys
import os
import time

log = logger.set_logger('listenLIRC')


def listen(response):
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

if global_config['simulator'] is False:
	try:
		ser = serial.Serial(
			port=global_config['serial_port'],
			baudrate=global_config['serial_boud_rate']
		)
		log.debug('Connected to XBee')
	except Exception as error:
		log.error(traceback.format_exc())

buffer = ''
while True:
	try:
		buffer += ser.read(ser.inWaiting())  # read all char in buffer
		while '|' in buffer:  # split data pipe by pipe and store it in var
			xbee_data, buffer = buffer.split('|', 1)
			xbee_data += '|'
			response = {'id': 'rx', 'source_addr_long': '000000000', 'rf_data': xbee_data}
			listen(response)
			print xbee_data
		time.sleep(0.01)
	except Exception as error:
		log.error(error.message)
		log.debug("re-initializing...")
		cmdstring = "sudo supervisorctl reload"
		os.system(cmdstring)
		break


if global_config['simulator'] is False:
	if ser is not None:
		ser.close()

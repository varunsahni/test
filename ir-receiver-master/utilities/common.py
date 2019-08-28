from includes import logger

log = logger.set_logger('utils.common')
"""
to use import
`from utilities.common import *`
"""


def trace(message, do_exit=True):
	import sys
	print(message)
	if do_exit:
		sys.exit(0)


def unicode_to_string(unicode_string):
	import unicodedata
	unicodedata.normalize('NFKD', unicode_string).encode('ascii', 'ignore')


def merge_two_dicts(x, y):
	"""Given two dicts, merge them into a new dict as a shallow copy."""
	z = x.copy()
	z.update(y)
	return z


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


def g2r_button_update_frame_generate(devices):
	import traceback
	try:
		g2r_frame = ''
		for device in devices:
			g2r_frame += g2r_button_update_single_frame_generate(device)
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def g2r_button_update_frame_generate_new(devices):
	import traceback
	try:
		g2r_frame = ''
		for device in devices:
			g2r_frame += g2r_button_update_single_frame_generate_new(device)
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def g2r_sensor_update_frame_generate(devices):
	import traceback
	try:
		g2r_frame = ''
		for device in devices:
			g2r_frame += g2r_sensor_update_single_frame_generate(device)
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def g2r_button_update_single_frame_generate(device):
	"""
	Generate appropriate device update status frame to send it to receiver

		Frame Format                    Validations     Example

		Frame start identifier          %               %
		Frame start identifier          %               %
		Switch Number Decimal Place     0-9             2
		Switch Number Unit Place        0-9             4
		Status Flag                     0,1             1
		Speed Decimal Place             0,1             5
		Speed Unit Place                0-9             3
		Child Lock Flag                 0-9             0
		Acknowledgement Flag            0,1             0
		Reserved Bit                    0               0
		Reserved Bit                    0               0
		Reserved Bit                    0               0
		Reserved Bit                    0               0
		Parity                          0,1             1
		Frame End Identifier            @               @
		Frame End Identifier            @               @

	:param device: Json object
	:return: g2r_frame: %%2415301@@
	"""
	import traceback
	try:
		if 'speed' not in device['desired_settings']:
			device['desired_settings']['speed'] = 100
		
		if 'child_lock' not in device['desired_settings']:
			device['desired_settings']['child_lock'] = False
		
		device['desired_settings']['speed'] = 99 if int(device['desired_settings']['speed']) is 100 else int(device['desired_settings']['speed'])
		device['ack_flag'] = device['ack_flag'] if 'ack_flag' in device else True
		
		g2r_frame_array = ['%', '%', '', '', '', '', '', '', '', '', '', '', '', '', '@', '@']
		g2r_frame_array[2] = str(int(device['number']) / 10)
		g2r_frame_array[3] = str(int(device['number']) % 10)
		g2r_frame_array[4] = str(int(device['desired_settings']['status']))
		g2r_frame_array[5] = str(int(device['desired_settings']['speed']) / 10)
		g2r_frame_array[6] = str(int(device['desired_settings']['speed']) % 10)
		g2r_frame_array[7] = str(int(device['desired_settings']['child_lock']))
		g2r_frame_array[8] = str(int(device['ack_flag']))
		g2r_frame_array[9] = str(0)
		g2r_frame_array[10] = str(0)
		g2r_frame_array[11] = str(0)
		g2r_frame_array[12] = str(0)
		
		sum = int(g2r_frame_array[2]) + int(g2r_frame_array[3]) + int(g2r_frame_array[4]) + int(g2r_frame_array[5]) + int(g2r_frame_array[6]) + int(g2r_frame_array[7]) + int(g2r_frame_array[8]) + int(g2r_frame_array[9]) + int(g2r_frame_array[10]) + int(g2r_frame_array[11]) + int(g2r_frame_array[12])
		g2r_frame_array[13] = str(1 if sum % 2 else 0)
		g2r_frame = ''.join(g2r_frame_array)
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def g2r_button_update_single_frame_generate_new(device):
	"""
	Generate appropriate device update status frame to send it to receiver

		Frame Format                    Validations     Example

		Frame start identifier          SW|DM           SW
		Device Number                   Number          1
		Delimiter                       .               .
		Status Bit                      0,1             1
		Delimiter                       .               .
		Speed                           0-100           98
		Delimiter                       .               .
		Child Lock Bit                  0,1             1
		Delimiter                       .               .
		Acknowledgement Bit             0,1             1
		Frame End Identifier            |               |
		

	:param device: Json object
	:return: g2r_frame: SW.1.1.98.1.1|
	"""
	import traceback
	try:
		device_type = 'SW'
		if device['type'] == 'smooth_dimmer' or device['type'] == 'step_dimmer':
			device_type = 'DM'
		
		if 'speed' not in device['desired_settings']:
			device['desired_settings']['speed'] = 100
		
		if 'child_lock' not in device['desired_settings']:
			device['desired_settings']['child_lock'] = False
		
		device['desired_settings']['speed'] = 99 if int(device['desired_settings']['speed']) is 100 else int(device['desired_settings']['speed'])
		device['ack_flag'] = device['ack_flag'] if 'ack_flag' in device else True
		
		g2r_frame = device_type + '.' + str(device['number']) + '.ACT.' + str(int(device['desired_settings']['status'])) + '.' + str(int(device['desired_settings']['speed'])) + '.' + str(int(device['desired_settings']['child_lock'])) + '|'
		
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def g2r_sensor_update_single_frame_generate(device):
	"""
	Generate appropriate device update status frame to send it to receiver

		Frame Format                    Validations         Example

		Frame start identifier          GS|SM|TM|MT|LD|IR   GS
		Device Number                   Number              1
		Delimiter                       .                   .
		Status Bit                      0,1                 1
		Delimiter                       .                   .
		Sensitivity                     0-10                9
		Delimiter                       .                   .
		Time Interval                   0-9999999           5000 (In milliseconds)
		Frame End Identifier            |                   |


	:param device: Json object
	:return: g2r_frame: GS.1.1.10|
	"""
	import traceback
	try:
		device_type = ''
		if device['type'] == 'gas_sensor':
			device_type = 'GS'
		elif device['type'] == 'smoke_sensor':
			device_type = 'SM'
		elif device['type'] == 'temperature_sensor':
			device_type = 'TM'
		elif device['type'] == 'motion_sensor':
			device_type = 'MT'
		elif device['type'] == 'light_sensor':
			device_type = 'LD'
		elif device['type'] == 'ir_blaster':
			device_type = 'IR'
		
		if device['type'] != 'ir_blaster':
			g2r_frame = device_type + '.' + str(device['number']) + '.ACT.' + str(int(device['desired_settings']['status'])) + '.' + str(int(device['desired_settings']['sensitivity'])) + '.' + str(int(device['desired_settings']['time_interval'])) + '|'
		else:
			g2r_frame = device_type + '.' + str(device['number']) + '.ACT.' + str(int(device['desired_settings']['status'])) + '|'
		
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())
		return ''


def g2r_live_status_frame_generate():
	"""
	Generate appropriate frame to get live status of all devices from receiver

		Frame Format                    Validations     Example

		Frame start identifier          %               %
		Frame start identifier          %               %
		Switch Number Decimal Place     0               0
		Switch Number Unit Place        x               x
		Status Flag                     0               0
		Speed Decimal Place             0               0
		Speed Unit Place                0               0
		Child Lock Flag                 0               0
		Acknowledgement Flag            0               0
		Reserved Bit                    0               0
		Reserved Bit                    0               0
		Reserved Bit                    0               0
		Reserved Bit                    0               0
		Parity                          0               0
		Frame End Identifier            @               @
		Frame End Identifier            @               @

	:return: g2r_frame: %%0x00000@@
	"""
	import traceback
	try:
		
		g2r_frame_array = ['%', '%', '0', 'x', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '@', '@']
		g2r_frame = ''.join(g2r_frame_array)
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def live_status_parsing(r2g_frame):
	import re
	import traceback
	devices = {}
	r2g_frame_array = []
	temp_frame = r2g_frame = r2g_frame.replace(" ", "").upper()
	
	try:
		# Generated from https://regex101.com/
		regex = r"([=%](.*?)[=@])"
		live_status_matches = re.findall(regex, r2g_frame)
		
		if len(
				live_status_matches) is not 0:  # This means %blahblah@ pattern matched. Means live device status of all devices
			for live_status_full_match, live_status_match in live_status_matches:
				regex = r"([=GR]+[0,1])"
				r2g_frame_array = re.findall(regex, live_status_match)
				
				if len(r2g_frame_array) is not 0:
					# Parsing individual 'G1' string
					switch_number = 1
					for single_r2g_frame in r2g_frame_array:
						single_r2g_frame_array = list(single_r2g_frame)
						
						if str(switch_number) not in devices:
							updated_by = 'user' if single_r2g_frame_array[0] is 'G' else 'receiver'
							devices[str(switch_number)] = {'device': 'SW', 'number': switch_number, 'settings': {'status': bool(int(single_r2g_frame_array[1])), 'speed': 100, 'updated_by': updated_by}}
						switch_number += 1
				r2g_frame = r2g_frame.replace(live_status_full_match, "")
			# In case string is like this %G1R1G0R0@GXXYGXXY
			temp_devices = single_device_status_parsing(r2g_frame)
			devices = merge_two_dicts(devices, temp_devices)
	except Exception as error:
		log.error("Error in parsing '" + temp_frame + "'. See error details -> " + traceback.format_exc())
	
	return devices


def single_device_status_parsing(r2g_frame):
	import re
	import traceback
	
	devices = {}
	r2g_frame_array = []
	temp_frame = r2g_frame = "".join(r2g_frame.split()).upper()
	
	try:
		# Generated from https://regex101.com/
		regex = r"([=GR]+[0,1][0-9][0-9])"
		single_status_matches = re.findall(regex, r2g_frame)
		if len(single_status_matches) is not 0:  # this means GXXYRXXY string matched. Means individual device status
			for match in single_status_matches:
				r2g_frame_array.append(match)
				r2g_frame = r2g_frame.replace(match, "")
			
			# Parsing individual 'G241' string
			for single_r2g_frame in r2g_frame_array:
				single_r2g_frame_array = list(single_r2g_frame)
				switch_number = int(single_r2g_frame_array[2] + single_r2g_frame_array[3])
				if str(switch_number) not in devices:
					updated_by = 'user' if single_r2g_frame_array[0] is 'G' else 'receiver'
					frame_type = 'ACTACK' if single_r2g_frame_array[0] is 'G' else 'ACT'
					devices[str(switch_number)] = {'device': 'SW_OLD', 'number': switch_number, 'frame_type': frame_type, 'settings': {'status': bool(int(single_r2g_frame_array[1])), 'speed': 100, 'child_lock': False}, 'updated_by': updated_by, 'ack_status': 'DONE'}
			
			# Sometimes frame missing initial letter. e.g expected = G241 but received = 241. Considering, that frame is receiving because of user pressed button on app.
			# So handeling that condition. Need fix from receiver side.
			# r2g_frame = r2g_frame.replace(" ", "").upper()
			if r2g_frame is not '' and len(r2g_frame) == 3:
				single_r2g_frame_array = list(r2g_frame)
				switch_number = int(single_r2g_frame_array[1] + single_r2g_frame_array[2])
				if str(switch_number) not in devices:
					updated_by = 'user'
					frame_type = 'ACTACK'
					devices[str(switch_number)] = {'device': 'SW_OLD', 'number': switch_number, 'frame_type': frame_type, 'settings': {'status': bool(int(single_r2g_frame_array[0])), 'speed': 100, 'child_lock': False}, 'updated_by': updated_by, 'ack_status': 'DONE'}
			
			elif r2g_frame is not '':
				log.error("Invalid frame received : '" + r2g_frame + "'")
	except Exception as error:
		log.error("Error in parsing '" + temp_frame + "'. See error details -> " + traceback.format_exc())
	
	return devices


def r2g_frame_parse(r2g_frame_raw):
	"""
		A. Frame received for individual device update acknowledgement from receiver

			Frame Format                    Validations     Example

			Initiator                       G,R             G
			Status Flag                     1               1
			Switch Number Decimal Place     0-9             2
			Switch Number Unit Place        0-9             4
			
			
		B. Frame received for live status of all devices acknowledgement from receiver

			Frame Format                    Validations     Example

			Frame start identifier          %               %
			Initiator1                      G,R             G
			Status Flag1                    1               1
			Initiator(n)                    G,R             G
			Status Flag(n)                  1               0
			Frame End Identifier            @               @
			
		Frame Format                    Validations     Example

			Initiator                       XX             GS
			Delimiter                       .               .
			Value1                          1               1
			Delimiter                       .               .
			Value2                          100             100
			Frame End Identifier            |               |

		:return: devices: {
			"24" : {"device": "SW|DM|GS|SM|TM|MT|LD", "number": 24, "settings": {"status": True, ...}},
			"25" : {"device": "SW|DM|GS|SM|TM|MT|LD", "number": 24, "settings": {"status": True, ...}}
		}
	"""
	
	import re
	import traceback
	import string
	from includes import xbee_comm
	
	log.debug("Raw frame received: " + r2g_frame_raw)
	devices = {}
	r2g_frame_raw = ''.join([x for x in r2g_frame_raw if x in string.printable])  # removing non printable characters.
	temp_frame = r2g_frame_raw = "".join(r2g_frame_raw.split()).upper()
	
	"""
		There are two types are string to parse
		A. G142
		B. %G1R0R1G0@
		
		Parsing logic
		1. First check whether string matches pattern %blahblah@
		2. If found then parse it with live_status_parsing
		3. Else check whether string matches pattern 'GXXY' where X means switch number and Y means status
		4. If found then parse it with single_device_status_parsing
		5. Else log Invalid frame found
	"""
	
	try:
		# Generated from https://regex101.com/
		regex = r"([=%](.*?)[=@])"
		live_status_matches = re.findall(regex, r2g_frame_raw)
		
		if len(live_status_matches) is not 0:  # This means %blahblah@ pattern matched. Means live device status of all devices
			temp_devices = live_status_parsing(r2g_frame_raw)
			devices = merge_two_dicts(devices, temp_devices)
		else:
			regex = r"([=GR]+[0,1][0-9][0-9])"
			single_status_matches = re.findall(regex, r2g_frame_raw)
			if len(single_status_matches) is not 0:  # this means GXXYRXXY string matched. Means individual device status
				temp_devices = single_device_status_parsing(r2g_frame_raw)
				devices = merge_two_dicts(devices, temp_devices)
			else:
				# Check for (|) pipe in the string SW.1.R.4|AB.2.R.1|GS.2.R.100
				r2g_frames = r2g_frame_raw.split('|')
				for i, r2g_frame in enumerate(r2g_frames):
					if r2g_frame == "":
						r2g_frames.pop(i)
						continue
					
					parts = r2g_frame.split('.')
					for j, part in enumerate(parts):
						if part == "":
							parts.pop(j)
					
					if len(parts) == 0:
						continue
					if len(parts) < 3:
						log.error("Invalid frame received : '" + r2g_frame + "'")
						continue
					
					# Switch ( SW.<device_number>.ACT.<status>.<child_lock> )
					# Switch ( SW.<device_number>.ACTACK.<status>.<child_lock> )
					# Dimmer ( DM.<device_number>.ACT.<status>.<speed>.<child_lock> )
					# Dimmer ( DM.<device_number>.ACTACK.<status>.<speed>.<child_lock> )
					# Gas Sensor ( GS.<device_number>.READ.<value> )
					# Gas Sensor ( GS.<device_number>.ACTACK.<status>.<value>.<sensitivity>.<time_interval> )
					# Smoke Sensor ( GS.<device_number>.READ.<value> )
					# Smoke Sensor ( SM.<device_number>.ACTACK.<status>.<value>.<sensitivity>.<time_interval> )
					# Temperature Sensor ( SM.<device_number>.READ.<value> )
					# Temperature Sensor ( TM.<device_number>.ACTACK.<status>.<value>.<sensitivity>.<time_interval> )
					# Motion Sensor ( TM.<device_number>.READ.<value> )
					# Motion Sensor ( MT.<device_number>.ACTACK.<status>.<value>.<sensitivity>.<time_interval> )
					# LDR Sensor ( LD.<device_number>.READ.<value> )
					# LDR Sensor ( LD.<device_number>.ACTACK.<status>.<value>.<sensitivity>.<time_interval> )
					# IR Blaster ( IR.<device_number>.ACTACK.<status> )
					# IR Blaster ( IR.<device_number>.RBACTACK.<remote_id>.<button_number> )
					# IR Blaster ( IR.<device_number>.RBPAIRACK.<remote_id>.<button_number> )
					# IR Blaster ( IR.<device_number>.RDELACK.<remote_id> )
					
					device = parts[0]
					switch_number = parts[1]
					frame_type = parts[2]
					devices[str(switch_number)] = {'device': device, 'number': switch_number, 'frame_type': frame_type, 'settings': {}, 'ack_status': 'DONE', 'updated_by': ''}
					
					# if device == 'SW':
					# 	if frame_type == 'ACT':
					# 		if len(parts) != 5:
					# 			del devices[str(switch_number)]
					# 			log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
					# 			continue
					# 		devices[str(switch_number)]['settings'] = {
					# 			'status': True if int(parts[3]) > 0 else False,
					# 			'speed': 100 if int(parts[3]) > 0 else 0,
					# 			'child_lock': True if int(parts[4]) > 0 else False,
					# 		}
					# 		devices[str(switch_number)]['updated_by'] = 'receiver'
					# 	elif frame_type == 'ACTACK':
					# 		if len(parts) != 5:
					# 			del devices[str(switch_number)]
					# 			log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
					# 			continue
					# 		devices[str(switch_number)]['settings'] = {
					# 			'status': True if int(parts[3]) > 0 else False,
					# 			'speed': 100 if int(parts[3]) > 0 else 0,
					# 			'child_lock': True if int(parts[4]) > 0 else False,
					# 		}
					# 		devices[str(switch_number)]['updated_by'] = 'gateway'
					# elif device == 'DM':
					# 	if frame_type == 'ACT':
					# 		if len(parts) != 6:
					# 			del devices[str(switch_number)]
					# 			log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
					# 			continue
					# 		devices[str(switch_number)]['settings'] = {
					# 			'status': True if int(parts[3]) > 0 else False,
					# 			'speed': int(parts[4]),
					# 			'child_lock': True if int(parts[5]) > 0 else False,
					# 		}
					# 		devices[str(switch_number)]['updated_by'] = 'receiver'
					# 	elif frame_type == 'ACTACK':
					# 		if len(parts) != 6:
					# 			del devices[str(switch_number)]
					# 			log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
					# 			continue
					# 		devices[str(switch_number)]['settings'] = {
					# 			'status': True if int(parts[3]) > 0 else False,
					# 			'speed': int(parts[4]),
					# 			'child_lock': True if int(parts[5]) > 0 else False,
					# 		}
					# 		devices[str(switch_number)]['updated_by'] = 'gateway'
					# elif device == 'GS' or device == 'SM' or device == 'TM' or device == 'MT' or device == 'LD':
					# 	if frame_type == 'READ':
					# 		if len(parts) != 4:
					# 			del devices[str(switch_number)]
					# 			log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
					# 			continue
					# 		devices[str(switch_number)]['settings'] = {
					# 			'status': True,
					# 			'value': int(parts[3])
					# 		}
					# 		devices[str(switch_number)]['updated_by'] = 'receiver'
					# 	elif frame_type == 'ACTACK':
					# 		if len(parts) != 7:
					# 			del devices[str(switch_number)]
					# 			log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
					# 			continue
					# 		devices[str(switch_number)]['settings'] = {
					# 			'status': True if int(parts[3]) > 0 else False,
					# 			'value': int(parts[4]),
					# 			'sensitivity': int(parts[5]),
					# 			'time_interval': int(parts[6])
					# 		}
					# 		devices[str(switch_number)]['updated_by'] = 'gateway'
					if device == 'IR':
						if frame_type == 'ACTACK':
							if len(parts) != 4:
								del devices[str(switch_number)]
								log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
								continue
							devices[str(switch_number)]['settings'] = {
								'status': True if int(parts[3]) > 0 else False
							}
							devices[str(switch_number)]['updated_by'] = 'gateway'
						elif frame_type == 'RBACT' or frame_type == 'RBACTACK':
							if len(parts) != 5:
								del devices[str(switch_number)]
								log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
								# xbee_comm.ser.flush()
								# xbee_comm.ser.flushInput()
								# log.debug("Serial input flushed")
								continue
							devices[str(switch_number)]['settings'] = {
								'remote_int_id': int(parts[3]),
								'button_number': parts[4]
							}
							devices[str(switch_number)]['updated_by'] = 'gateway'
						elif frame_type == 'RBPAIRACK' or frame_type == 'RBPAIR':
							if len(parts) != 5:
								del devices[str(switch_number)]
								log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
								# xbee_comm.ser.flush()
								# xbee_comm.ser.flushInput()
								# log.debug("Serial input flushed")
								continue
							devices[str(switch_number)]['settings'] = {
								'remote_int_id': int(parts[3]),
								'button_number': parts[4]
							}
							devices[str(switch_number)]['updated_by'] = 'gateway'
						elif frame_type == 'RDELACK' or frame_type == 'RDEL':
							if len(parts) != 4:
								del devices[str(switch_number)]
								log.error("Invalid " + device + " frame received : '" + r2g_frame + "'")
								# xbee_comm.ser.flush()
								# xbee_comm.ser.flushInput()
								# log.debug("Serial input flushed")
								continue
							devices[str(switch_number)]['settings'] = {
								'remote_int_id': int(parts[3])
							}
							devices[str(switch_number)]['updated_by'] = 'gateway'
					else:
						del devices[str(switch_number)]
						log.error("Invalid frame received : '" + r2g_frame + "'")
						# xbee_comm.ser.flush()
						# xbee_comm.ser.flushInput()
						# log.debug("Serial input flushed")
	
	except Exception as error:
		log.error("Error in parsing '" + temp_frame + "'. See error details -> " + traceback.format_exc())
	return devices


def g2r_remote_update_frame_generate(remotes):
	import traceback
	try:
		g2r_frame = ''
		for remote in remotes:
			g2r_frame += g2r_remote_update_single_frame_generate(remote)
		return g2r_frame
	
	except Exception as error:
		log.error(traceback.format_exc())


def g2r_remote_update_single_frame_generate(remote):
	"""
	Generate appropriate remote pair button status frame to send it to receiver

		Frame Format                    Validations     Example

		Initiator                       IR              IR
		Delimiter                       .               .
		Device Number                   0-99            1
		Delimiter                       .               .
		Remote Id                       0-99            1
		Delimiter                       .               .
		Action                          P|A|D           P
		Delimiter                       .               .
		Button Number                   0-99            1
		Frame End Identifier            |               |

	:param remote: Json object
	:return: g2r_frame: IR.1.1.P.20|
	"""
	import traceback
	try:
		if remote['action'] == 'pair':
			return 'IR.' + str(remote['device_number']) + '.RBPAIR.' + str(remote['remote_int_id']) + '.' + str(remote['button_number']) + '|'
		elif remote['action'] == 'action':
			return 'IR.' + str(remote['device_number']) + '.RBACT.' + str(remote['remote_int_id']) + '.' + str(remote['button_number']) + '|'
		elif remote['action'] == 'delete':
			return 'IR.' + str(remote['device_number']) + '.RDEL.' + str(remote['remote_int_id']) + '.0|'
		else:
			return ''
	
	except Exception as error:
		log.error(traceback.format_exc())


def follow(thefile, sleep=0.1):
	"""
	Live file reading
	:param thefile:
	:return:
	"""
	import time
	thefile.seek(0, 2)
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(sleep)
			continue
		yield line


def get_local_ip():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("google.com", 80))
	return s.getsockname()[0]


def get_pids(name):
	import psutil
	pids = []
	for proc in psutil.process_iter():
		if proc.name() == name:
			pids.append(proc.pid)
	return pids


def is_internet_on():
	"""
	Check whether internet is on or not
	:return: boolean
	"""
	import urllib2
	try:
		urllib2.urlopen('https://www.google.co.in', timeout=5)
		return True
	except Exception as err:
		return False


def get_ip_address():
	ip_address = ""
	import netifaces as ni
	for interface in ni.interfaces():
		if 2 in ni.ifaddresses(interface):
			ip = ni.ifaddresses(interface)[2][0]['addr']
			if ip != "127.0.0.1":
				ip_address = ip
	
	return ip_address

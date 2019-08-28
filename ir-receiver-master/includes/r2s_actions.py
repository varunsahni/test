from utilities.common import *
import json
from includes import logger
from config.global_config import global_config
import subprocess
import traceback
import os
import time

log = logger.set_logger('r2s_actions')

devices_types = {
	'button': 'SW',
	'smooth_dimmer': 'DM',
	'step_dimmer': 'DM',
	'gas_sensor': 'GS',
	'smoke_sensor': 'SM',
	'temperature_sensor': 'TM',
	'motion_sensor': 'MT',
	'light_sensor': 'LD',
	'ir_blaster': 'IR'
}

'''
R2S related actions below
'''


def status(response):
	try:
		log.debug(str(response))
	except Exception as error:
		log.error(traceback.format_exc())


def tx_status(response):
	try:
		pass
	except Exception as error:
		log.error(traceback.format_exc())


def node_id_indicator(response):
	try:
		log.debug(str(response))
	except Exception as error:
		log.error(traceback.format_exc())


def r2g_data_received(response):
	try:
		receiver_mac_id = ''.join('{:02X}'.format(ord(c)) for c in response['source_addr_long'])
		devices = r2g_frame_parse(response['rf_data'])
		log.debug("devices received from parsing : " + json.dumps(devices))
		if len(devices) is not 0:
			process_request(receiver_mac_id, devices)
	except Exception as error:
		log.error(traceback.format_exc())


def pair(cmd=""):
	try:
		
		temp_remote_button = global_config['temp_remote_button_path']
		try:
			os.remove(temp_remote_button)
		except OSError:
			pass
		log.debug(temp_remote_button + " file removed")
		
		cmdstring = "sudo /etc/init.d/lirc stop"
		os.system(cmdstring)
		log.debug("command run : {}".format(cmdstring))
		
		cmdstring = "sudo fuser -k /dev/lirc0"
		os.system(cmdstring)
		log.debug("command sent : {}".format(cmdstring))
		
		time.sleep(1)
		
		try:
			with open(temp_remote_button, 'w') as fileDiscriptor:
				subprocess.Popen(["mode2", "-m", "-d", "/dev/lirc0"], stdout=fileDiscriptor)
				log.debug("command sent : mode2 -m -d /dev/lirc0 > " + temp_remote_button)
		except Exception as error:
			log.error(traceback.format_exc())
		
		delay = 0
		startTime = time.time()
		log.debug('code started on %s ' % startTime)
		button_pressed = False
		while delay < 10:
			currentTime = time.time()
			delay = currentTime - startTime
			log.debug("Press button on remote.")
			time.sleep(0.5)
			if os.path.isfile(temp_remote_button) and os.path.getsize(temp_remote_button) > 0:
				button_pressed = True
				time.sleep(1)
				log.debug('conf file (' + temp_remote_button + ') written in %s time '% str(delay))
				break
			log.debug('Delay completed %s ' % str(delay))
		
		cmdstring = "sudo fuser -k /dev/lirc0"
		os.system(cmdstring)
		log.debug("command sent : {}".format(cmdstring))
	
		fileDiscriptor.close()
		return button_pressed
	except Exception as error:
		log.error(traceback.format_exc())
		
def copy_file_content_clipboard(template_file_path):
	data = ""
	fin = None
	try:
		with open(template_file_path, 'r') as fin:
			data = fin.read()
		fin.close()
	except Exception as error:
		if fin is not None:
			fin.close()
		log.error(traceback.format_exc())
	return data

def write_file(source_file, data):
	try:
		with open(source_file, 'w') as fout:
			fout.write(data)
	except Exception as error:
		log.error(traceback.format_exc())
		fout.close()
	fout.close()


def prepend_to_file(source_file, destination_file):
	try:
		with open(destination_file, 'r+') as f:
			content = f.read()
			f.seek(0, 0)
			data = copy_file_content_clipboard(source_file)
			f.write(data + '\n' + content)
	except Exception as error:
		print error

def copy_to_file(source_file, destination_file):
	import subprocess
	try:
		with open(destination_file, 'a') as fileDiscriptor:
			subprocess.Popen(["cat", source_file], stdout=fileDiscriptor)
			fileDiscriptor.close()
	except Exception as error:
		print error
		fileDiscriptor.close()
	pass

def process_request(receiver_mac_id, devices):
	try:
		for (device_number, ir_device) in devices.iteritems():
			"""
				ir_device variable contains data in following format if frame received IR.2.RBPAIR.1.5|
				
				{
					"updated_by":"gateway",
					"settings":{
						"remote_int_id":1,
						"button_number":"5"
					},
					"frame_type":"RBPAIR",
					"number":"2",
					"ack_status":"DONE",
					"device":"IR"
				}
				
			"""
			
			if ir_device['device'] == 'IR':
				if ir_device['frame_type'] == 'RBPAIR':
					ir_device_number = ir_device['number']
					ir_remote_number = ir_device['settings']['remote_int_id']
					ir_remote_button_number = ir_device['settings']['button_number']
					
					is_paired = pair()
					
					if is_paired:
						remote_button_name = str(ir_device_number) + "_" + str(ir_remote_number) + "_" + str(ir_remote_button_number)
						
						template_button_str = copy_file_content_clipboard(global_config['codebase_path'] + global_config['template_remote_button_file_path'])
						template_button_str = template_button_str.replace("{{file_name}}", remote_button_name)
						
						template_button_str = template_button_str.replace("{{ir_code_base_path}}", global_config['ir_code_path'])
						
						code_str = copy_file_content_clipboard(global_config['temp_remote_button_path'])
						try:
							code_str = code_str.split("\n", 2)[2]
						except IndexError:
							pass
						
						template_button_str = template_button_str.replace("{{code}}", code_str)
						
						if not os.path.exists(global_config['ir_code_path']):
							os.makedirs(global_config['ir_code_path'])
							
						write_file(global_config['ir_code_path'] + remote_button_name + '.conf', template_button_str)
						log.debug("written data into " + global_config['ir_code_path'] + remote_button_name+'.conf')
						
						prepend_to_file(global_config['ir_code_path'] + remote_button_name + '.conf', "/etc/lirc/lircd.conf")
						log.debug("copied content from " + global_config['ir_code_path'] + remote_button_name+'.conf' + ' to /etc/lirc/lircd.conf')
	
						r2g_frame = 'IR.' + str(ir_device_number) + '.RBPAIRACK.' + str(ir_remote_number) + '.' + str(ir_remote_button_number) + '|'
						r2g_send_frame(receiver_mac_id, r2g_frame, retries=1)
						log.debug("Acknowledgement sent : %s" %r2g_frame)
					else:
						log.debug("Button not pressed on remote")
					
					try:
						cmdstring = "sudo /etc/init.d/lirc restart"
						os.system(cmdstring)
						log.debug("command sent : {}".format(cmdstring))
					except Exception as error:
						log.error(traceback.format_exc())
						
					cmdstring = "sudo ps -ef | grep defunct | grep -v grep | cut -b8-20 | xargs kill -9"
					os.system(cmdstring)
					log.debug("command sent : {}".format(cmdstring))
				
				elif ir_device['frame_type'] == 'RBACT':
					ir_device_number = ir_device['number']
					ir_remote_number = ir_device['settings']['remote_int_id']
					ir_remote_button_number = ir_device['settings']['button_number']
					remote_button_name = str(ir_device_number) + "_" + str(ir_remote_number) + "_" + str(ir_remote_button_number)
					remote_button_conf_file_name = global_config['ir_code_path'] + remote_button_name+'.conf'
					cmdstring = "irsend SEND_ONCE {} {}".format(remote_button_conf_file_name, remote_button_name)
					try:
						os.system(cmdstring)
						log.debug("command sent : {}".format(cmdstring))
					except Exception as error:
						print "failed irsend SEND_ONCE : "+error

					print"command sent : %s" % cmdstring
					log.debug('You reached here in IR RBACT')
					r2g_frame = 'IR.' + str(ir_device_number) + '.RBACTACK.' + str(ir_remote_number) + '.' + str(ir_remote_button_number)+'|'
					r2g_send_frame(receiver_mac_id, r2g_frame, retries=1)
			pass
	except Exception as error:
		log.error(traceback.format_exc())


def r2g_send_frame(receiver_mac_id, g2r_frame, retries=global_config['frame_sending_retries']):
	if g2r_frame is None:
		return False
	while retries > 0:
		try:
			if global_config["simulator"] is False:
				import xbee_comm
				xbee_obj = xbee_comm.XBeeComm()
				if xbee_comm.xbee_conn is not None:
					frame_id = "A"
					xbee_comm.ser.write(g2r_frame)
					log.debug("G2R XBee frame (" + frame_id + ") Sent : '" + g2r_frame + "' to receiver : '" + receiver_mac_id + "'. Attempts left : " + str(retries))
					xbee_obj.disconnect_only_xbee()
					return True
				return False
			else:
				frame_id = "S"
				log.debug("SIMULATED : G2R XBee frame (" + frame_id + ") Sent : '" + g2r_frame + "' to receiver : '" + receiver_mac_id + "'. Attempts left : " + str(retries))
				return True
		except Exception as error:
			log.error(traceback.format_exc())
			retries -= 1
			time.sleep(global_config['delay_in_switch_operation'])
			return r2g_send_frame(receiver_mac_id, g2r_frame, retries)
	
	return False

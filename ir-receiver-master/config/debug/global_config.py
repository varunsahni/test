import datetime
import os, time
import logging

os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")

"""
Global Config Dictionary
Need to import like this

`from config.global_config import global_config`
"""

global_config = {
	"serial_port": "/dev/ttyUSB0",
	"serial_boud_rate": 9600,
	
	"simulator": False,
	
	"frame_sending_retries": 1,
	"delay_in_switch_operation": 0.2,
	
	"temp_remote_button_path": "/tmp/temp.txt",
	"codebase_path": "/opt/ir-receiver/",
	"ir_code_path": "/opt/ir-codes/",
	"template_remote_button_file_path": "template.conf",
	
	# "log_file_dir": "/home/pi/",
	"log_file_dir": "/tmp/",
	"log_file_name": "skybot.log",
	"logging_level": logging.DEBUG
}

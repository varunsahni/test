"""
To use this logger file
`from includes import logger`

# log.warn("Hi There, This is warning")
# log.error("Hi There, This is error")
# log.info("Hi There, This is info")
# log.debug("Hi There, This is debug")

"""

import logging
from config.global_config import global_config
from logging.handlers import TimedRotatingFileHandler
import os
import subprocess

if os.path.isdir(global_config["log_file_dir"]) is False:
	subprocess.call(['sudo', 'mkdir', '-p', global_config["log_file_dir"]])

rootlogger = logging.getLogger()
rootlogger.setLevel(global_config["logging_level"])

# create file handler which logs even debug messages
handler = TimedRotatingFileHandler(global_config["log_file_dir"] + global_config["log_file_name"], when="midnight", interval=1, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s (%(lineno)d) - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
handler.suffix = "%Y%m%d.log"
handler.setLevel(global_config["logging_level"])
rootlogger.propagate = False
rootlogger.addHandler(handler)


def set_logger(name):
	return logging.getLogger(name)

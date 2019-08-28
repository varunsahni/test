import os
import sys
import time
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir + "/build/lib.linux-armv6l-3.2/")
import lirc

lirc.init("lirctest", "lircrc.test", blocking=False)

print("Don't press anything yet...")
start_time = time.time()
end_time = start_time + 1  # 1 second in the future
pressed = False
while not pressed and time.time() < end_time:
    pass

print("Press 1 on your remote.")
start_time = time.time()
end_time = start_time + 5  # 5 seconds in the future
pressed = False
while not pressed and time.time() < end_time:
    ircode = lirc.nextcode()
    if len(ircode) is not 0:
        print "IR CODES:"
        print ircode
    
print("Timeout")
lirc.deinit()


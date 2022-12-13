import time
import connect

#sleep to give some boards time to initialize, for example Rpi Pico W
time.sleep(3)

import connect
w=connect.Wifi()

if w.run_mode():
    print("Normal mode activated - for chance to OS-mode type in terminal:")
    print(">>>import os")
    print(">>>os.remove('run_mode.dat'")    
    import main1
else:
    print("OS mode activated")
    import web_os_run
    

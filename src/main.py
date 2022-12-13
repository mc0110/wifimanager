import time
import connect

#sleep to give some boards time to initialize, for example Rpi Pico W
time.sleep(3)

# import set_credentials_encrypt
# import truma_serv
import connect

w=connect.Wifi()
if w.run_mode():
    print("Normal mode activated - for chance to OS-mode type:")
    print(">>>import os")
    print(">>>os.remove('run_mode.dat'")    
    import truma_serv
else:
    print("OS mode activated")
    import web_os_run
    
#import gen_html

#import truma_serv1
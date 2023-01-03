# MIT License
#
# Copyright (c) 2022  Dr. Magnus Christ (mc0110)
#
# This is part of the wifimanager package
# 
import time
import connect
import machine
appname = "wifimanager"


#sleep to give some boards time to initialize, for example Rpi Pico W
time.sleep(3)
w=connect.Wifi()
w.set_appname(appname)
w.set_sta(1)

# this is for the update-process
if w.run_mode() > 1:  
    print("Update-Process startetd")
    import cred
    cred.set_cred_json()
    for i in cred.update_repo():
        print(i)
    w.run_mode(w.run_mode() - 2)     
    machine.reset()
    
else:
    # this is normal run mode   
    if w.creds() and w.set_sta() and w.run_mode():
        print("Normal mode activated - for change to OS-mode type in terminal:")
        print(">>>import os")
        print(">>>os.remove('run_mode.dat'")    
        import main1
    # this is os run mode    
    else:                
        print("OS mode activated")
        import web_os_run
        web_os_run.run(w)
            

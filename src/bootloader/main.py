# MIT License
#
# Copyright (c) 2022  Dr. Magnus Christ (mc0110)
#
# This is part of the inetbox2mqtt package
# 
# 
# After reboot the port starts with boot.py and main.py
#
# This code-segment needs to be named "main.py"
#
#
#
#
# Use this commands to connect to the network 
#
# import network
# s = network.WLAN(network.STA_IF)
# s.active(True)
# s.connect("<yourSSID>","<YourWifiPW>")
# print('network config:', s.ifconfig())
# import mip
# mip.install("github:mc0110/inetbox2mqtt/source/bootloader/main.py","/")
# 
# import main
#
# The last command starts the download-process of the whole suite
# The download overwrites the main-program, so you see this process only once



import time, os
import mip
#sleep to give some boards time to initialize, for example Rpi Pico W
time.sleep(3)

# bootloader for the whole suite
tree = "github:mc0110/inetbox2mqtt"

env = [
    ["/lib/nanoweb.py", "/lib/"],
    ["/src/cred.json", "/"],
    ["/src/connect.py", "/"],
    ["/src/crypto_keys.py", "/"],
    ["/src/gen_html.py", "/lib/"],
    ["/src/main.py", "/"],
    ["/src/main1.py", "/"],
    ["/src/web_os.py", "/"],
    ["/src/web_os_run.py", "/"],
    ]

for i in range(len(env)):
    mip.install(tree+env[i][1]+env[i][0], target= env[i][1])


w=connect.Wifi()
if w.run_mode():
    print("Normal mode activated - for chance to OS-mode type:")
    print(">>>import os")
    print(">>>os.remove('run_mode.dat'")    
    import main1
else:
    print("OS mode activated")
    import web_os_run



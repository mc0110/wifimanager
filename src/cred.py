# MIT License
#
# Copyright (c) 2022  Dr. Magnus Christ (mc0110)
#
# This is part of the wifimanager package
# 
# 
# For the proper functioning of the connect-library, the keys "SSID", "WIFIPW", "HOSTNAME" should be included.
# Any other keys can be added


def set_cred_json():
    import connect

#     j = {
#      "SSID": ["text", "SSID:", "1"],
#      "WIFIPW": ["password", "Wifi passcode:", "2"],
#      "MQTT": ["text", "Boker name/IP:", "3"],
#      "UN": ["text", "Broker User:", "4"],
#      "UPW": ["text", "Broker password:", "5"],
#      "HOSTNAME": ["text", "Hostname:", "6"],
#      "ADC": ["checkbox", "Addon DuoControl :", "7"]
#      "ASL": ["checkbox", "Addon SpiritLevel:", "8"],
#      "OSR": ["checkbox", "OS Web:", "9"],
#      }
    j = {
     "SSID": ["text", "SSID:", "1"],
     "WIFIPW": ["password", "Wifi passcode:", "2"],
     "MQTT": ["text", "Boker name/IP:", "3"],
     "UN": ["text", "Broker User:", "4"],
     "UPW": ["text", "Broker password:", "5"],
     "HOSTNAME": ["text", "Hostname:", "6"],
     }

    w=connect.Wifi()
    w.write_cred_json(j)


def update_repo():
    import time, os
    import mip
    #sleep to give some boards time to initialize, for example Rpi Pico W
    time.sleep(3)

    # bootloader for the whole suite
    tree = "github:mc0110/wifimanager"

    env = [
        ["/lib/", "nanoweb.py", "/test/lib/"],
    #    ["/", "cred.json", "/test/"],
    #    ["/", "connect.py", "/test/"],
        ["/src/", "crypto_keys.py", "/test/"],
    #    ["/", "gen_html.py", "/test/"],
    #    ["/", "main.py", "/test/"],
    #    ["/", "main1.py", "/test/"],
        ["/src/", "web_os.py", "/test/"],
        ["/src/", "web_os_run.py", "/test/"],
        ]

    for i in range(len(env)):
        mip.install(tree+env[i][0]+env[i][1], target= env[i][2])

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
    import json
    CRED_JSON = "cred.json"

#     j = {
#      "SSID": ["text", "SSID:", "1"],
#      "WIFIPW": ["password", "Wifi passcode:", "2"],
#      "MQTT": ["text", "Broker name/IP:", "3"],
#      "UN": ["text", "Broker User:", "4"],
#      "UPW": ["text", "Broker password:", "5"],
#      "HOSTNAME": ["text", "Hostname:", "6"],
#      "ADC": ["checkbox", "Addon DuoControl :", "7"],
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
    with open(CRED_JSON, "w") as f: json.dump(j, f)


def update_repo():
    import time, os
    import mip
    #sleep to give some boards time to initialize, for example Rpi Pico W
    time.sleep(3)

    # bootloader for the whole suite
    tree = "github:mc0110/wifimanager"

    env = [
        ["/lib/", "nanoweb.py", "/lib"],
        ["/lib/", "crypto_keys.py", "/lib"],
        ["/lib/", "connect.py", "/lib"],
        ["/lib/", "gen_html.py", "/lib"],
        ["/lib/", "web_os.py", "/lib"],
        
        ["/src/", "cred.py", "/"],
        ["/src/", "release.py", "/"],
        ["/src/", "main.py", "/"],
        ["/src/", "main1.py", "/"],
        ["/src/", "web_os_run.py", "/"],
        ]

    for i in range(len(env)):
        errno = 1
        while errno and errno<3:
            try:
                mip.install(tree+env[i][0]+env[i][1], target= env[i][2])
                errno = 0
            except:
                errno += 1
            s = env[i][1]
            st = (errno == 0)
            yield (s, st)

def read_repo_rel():
    import mip
    import time
    try:
        mip.install("github:mc0110/wifimanager/src/release.py", target = "/")
    except:
        import machine
        machine.reset()
    time.sleep(1)    
    import release
    q = release.rel_no
    print("Repo relase-no: " + q)
    return q

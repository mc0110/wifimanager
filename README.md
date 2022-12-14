# wifimanager
## micropython nano-os with ota-functionality

This is a very small web manager for different hw ports under micropython, based on [nanoweb](https://github.com/hugokernel/micropython-nanoweb) - tested with ESP32 and RPI pico w. On the basis of the mip-module, the installation process as well as subsequent updates can be carried out over the air (ota).

![grafik](https://user-images.githubusercontent.com/10268240/207604186-1b687d86-4c5b-4c00-9ad8-e96c6fb0194f.png)

### Key features:
  - Automatic establishing of a Wifi connection
    - If a correct credential file is available - as station connection (STA).
    - In fallback, an access point (AP) is opened under 192.168.4.1
  - Input of credentials json-controlled (any number of keys are possible)
  - OTA update of a GITHUB repro possible 
  - Simple filesystem operations are supported
  - Scan of the Wifi-network environment
  - Use of multiple credential files


### Install-process
Use this commands to connect to the network 

     import network
     s = network.WLAN(network.STA_IF)
     s.active(True)
     s.connect("<yourSSID>","<YourWifiPW>")
     print('network config:', s.ifconfig())
     import mip
     mip.install("github:mc0110/wifimanager/bootloader/main.py","/")

     import main


### Credentials

The entry of credentials is json-file controlled and thus also allows the additional possibility of entering mqtt-broker and username or password but also clickboxes for entering control flags.

![grafik](https://user-images.githubusercontent.com/10268240/207604232-6f174b29-db72-4010-8b7f-aacdb80795ee.png)


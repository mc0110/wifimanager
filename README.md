<div align = center>

# wifimanager

## micropython nano-os with ota-functionality

[![Badge License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)
 &nbsp;
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

</div>

This is a very small web manager for different hw ports under micropython, based on [nanoweb](https://github.com/hugokernel/micropython-nanoweb) - tested with ESP32 and RPI pico w. 

On the basis of the mip-module, the installation process as well as subsequent updates can be carried out over the air (ota).

The wifimanager can be integrated into own projects and thus complement wifi-support as well as ota-function. An example of integration is demonstrated in [inetbox2mqtt](https://github.com/mc0110/inetbox2mqtt).



<div align = center>

![grafik](https://user-images.githubusercontent.com/10268240/211166613-1f8b4c54-7194-41f0-b4bb-104eb1022d2f.png)


</div>

### Key features:
  - Automatic establishing the Wifi connection
    - an access point (AP) is opened under 192.168.4.1
    - additionally, if a correct credential file is available - as station connection (STA) with dhcp-ip-address.
  - Input of credentials json-controlled (any number of keys are possible)
  - OTA update of a GITHUB repro possible 
  - Simple filesystem operations are supported
  - Scan of the Wifi-network environment
  - Use of multiple credential files


## Install-process

### Alternative 1: 

The installation process requires a terminal-based connection once after microPython has been installed on the port. The few lines must be entered to establish a Wifi internet connection. This will then automatically load all programme parts and reboot the port.

Use this commands to connect to the network and to start the download-process

     import network
     s = network.WLAN(network.STA_IF)
     s.active(True)
     s.connect("<yourSSID>","<YourWifiPW>")
     print('network config:', s.ifconfig())
     import mip
     mip.install("github:mc0110/wifimanager/bootloader/main.py","/")

     import main

After the software download, the normal start procedure starts, as shown in the diagram.

### Alternative 2: With esptool - only works with the ESP32

The .bin file (pls unzip the doc from bin-dictionary) contains both the python and the .py files. This allows the whole project to be flashed onto the ESP32.

For this, you can use the esptool. In my case, it finds the serial port of the ESP32 automatically, but the port can also be specified. The ESP32 must be in programming mode (GPIO0 to GND at startup). The command to flash the complete .bin file to the ESP32 is:

    esptool.py write_flash 0 flash_esp32_wifimanager_v101_4M.bin

This is not a partition but the full image for the ESP32 and only works with the 4MB chips. The address 0 is not a typo.

After flashing, please reboot the ESP32. An access point should be opened and you can use a browser to communicate via http://192.168.4.1
I recommend using the OTA update function once after flashing to download the latest version of the software.

<div align = center>

![grafik](https://user-images.githubusercontent.com/10268240/211199402-8dc93e2e-7478-46f3-90b2-e0a04cfcc316.png)


</div>

The port (ESP32/ RPI pico w) starts with an AP on ***ip: 192.168.4.1*** (at port 80).  (AccessPoint on ESP32 is without password, on RPI pico w SSID: 'PICO', password: 'password') Therefore, the connection must first be established with the mobile phone or computer. The page can be called after that. 

After you have opened the portal, the first thing you should do is enter the credentials for access to your Wifi network. Out of the box, you can use the predefined mask (see next figure) for this. After storing, you can check the network access with the button *"Start STA Connect "*.


## Credentials formular

The entry of credentials is json-file controlled and thus also allows the additional possibility of entering mqtt-broker and username or password but also clickboxes for entering control flags.

You find the definition in ***cred.py***. During the start-up process, the file cred.json is generated from it if this file is missing. Accordingly, cred.py can be adapted as required and thus enables the addition of project-specific input fields. 


<div align = center>

![grafik](https://user-images.githubusercontent.com/10268240/211166706-a5043be5-bba3-49a5-a8c7-a2c2f4ef56b2.png)

</div>


    j = {
     "SSID": ["text", "SSID:", "1"],
     "WIFIPW": ["password", "Wifi passcode:", "2"],
     "MQTT": ["text", "Boker name/IP:", "3"],
     "UN": ["text", "Broker User:", "4"],
     "UPW": ["text", "Broker password:", "5"],
     "HOSTNAME": ["text", "Hostname:", "6"],
     }
     
   
You can use all html form-types (text, password, checkbox) for the input-fields. The last number is the ordering-number for the form-entry.
If you change something, you have to call the routine cred.set_cred_json() once.

Remark: For the proper functioning of the ***connect-module***, the keys ***"SSID", "WIFIPW", "HOSTNAME"*** should be included.


## Operating modes

ESP32 or RP2 pico w can be working in different operating modes. 

When the chip is started for the first time and whenever it cannot establish a Wifi connection during restart, it is reset to OS mode (operation system mode). In this mode, the access point is activated and the browser can establish a connection to the portal on 192.168.4.1.

The operation mode can be changed via the browser:

      OS Run -> Normal Run -> Update-Mode -> OS Run


 Switching to ***normal run*** mode deactivates the web frontend at the next system start and starts normal operation, provided that the prerequisites are met (credentials have been created, Wifi connection is established). Since the web OS modules are not loaded in this case, all resources (especially RAM) are fully available for the original application.

Switching to ***Update-Mode*** starts the update process for the set repository at the next system start. The release number in main.py (on the chip) is compared with the release number in release.py in the GITHUB repository and an update is carried out if the release number does not match. 

On the ESP32, the repo update can also be carried out directly via the browser (without changing the operating mode), but this is not possible on the RP2 pico w at the moment. Here, the update can only be done by changing the operating mode.

The update mode can also be triggered from the normal run. To do this, the operating mode must be increased by 2. After the update (at the next system start), the port returns to normal run mode.


## OTA-support

If you want to use the OTA function for your own repos, you only need an adapted ***cred.py*** that points to your repo. You can also pull the files from several repos.

The download repo and the desired py-modules are also to be adapted in ***cred.py***.

Please also note the release numbers in main.py and release.py. If you want the repo to always be updated, the numbers just have to be different.




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






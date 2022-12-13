import os, sys
import json
import machine, time
import connect
import uasyncio as asyncio
from nanoweb import HttpError, Nanoweb, send_file
from mqtt_async import MQTTClient, config
import gc
#from crypto_keys import fn_crypto as crypt
#from tools import set_led
#from lin import Lin
#from duo_control import duo_ctrl
    
JSON = {
        1: ["SSID", "text", "SSID:"],
        2: ["WIFIPW", "password", "Wifi passcode:"],
        3: ["MQTT", "text", "Boker name/IP:"],
        4: ["UN", "text", "Broker User:"],
        5: ["UPW", "text", "Broker password:"],
        6: ["HOSTNAME", "text", "Hostname:"],
        7: ["ADC", "checkbox", "Addon DuoControl :"],
        8: ["ASL", "checkbox", "Addon SpiritLevel:"],
        }

CR_M    = "    (c) Magnus Christ (2022) "

w = connect.Wifi()
w.connect()
CONNECT_STATE = ""

HLP_TXT = {
        "root": '''This manager allows the administration of microPython devices via Wifi connection. The data of Wifi and MQTT broker can be stored in a credentials file even without internet access.
Individual files can also be deleted or uploaded/downloaded. The data is stored encrypted on the device. 
With an existing internet connection, software can be updated from GITHUB via OTA. The websuite is optimized for small devices. In consideration of size and performance, jQuery and bootstrap have been omitted.

''',
        "files": 'Filemanager with full access to the ports filesystem. You see the sub-directories as links',
        "": 'No help description available',
    }

def refresh_connect_state():
    global CONNECT_STATE
    CONNECT_STATE = w.get_state()
    gc.collect()
    CONNECT_STATE["mem_free"] = str(gc.mem_free())
    json = {}
    a = max(JSON.keys())
    for i in JSON.keys():
        json[JSON[i][0]] = "0"       
    a = w.read_creds(json)
    for key, val in a.items():
        CONNECT_STATE["cred_" + key] = val
    

def head():
    tmp = '''
        <!DOCTYPE html>
        <html lang='en'>
        
        <head>
            <meta charset='UTF-8'>
            <meta name= viewport content='width=device-width, initial-scale=1.0,'>
            <meta Content-Type='application/x-www-form-urlencoded'>
                <style type='text/css'>
                    .body_style {background-color: rgb(197, 209, 227); font-size:100%; margin-left: 10%;margin-right: 10%;}
                    .label_style {margin: 5px; font-size: 100%;}
                    .help {background-color: white;color: darkgray;width: 100%;margin-left: auto;margin-right: auto;padding: 2%;justify-content: left;font-size:80%;margin-bottom:3%;}
                    .status {background-color: rgb(4, 4, 78);color: rgb(228, 223, 223);width: 100%;margin-left: auto;margin-right: auto;padding: 2%;justify-content: left;font-size:80%;margin-bottom:3%;}
                    .status_title {font-size: 140%;padding-bottom: 1%;}
                    .message {display: flex; background-color:aliceblue; justify-content: center; font-size:120%; margin:5%; padding: 3%;}
                    .center {display: flex; justify-content: center; font-size:100%;}
                    .entry {font-size:12px; margin: 10px;}
                    .entry_s {margin: 5px; font-size: 10px;}
                    .button {height: 32px;%; width:45%; font-size:100%; background-color: rgb(206, 206, 225);margin-top: 1%;border-radius:10%;}
                    .button_s {height:21px; width:80px; font-size:90%; background-color: rgb(206, 206, 206); margin-top: 1%;}
                </style>
        </head>
    '''
    return tmp

def handleHeader(title, hlpkey):
    def str_keys(pre):
        s = ""
        ap_k = []
        for key in CONNECT_STATE.keys():
            if key.startswith(pre):
                ap_k.append(key)
        ap_k.sort()
        for key in ap_k:
            s += "&nbsp;(" + key + " = " + str(CONNECT_STATE[key]) + ")&nbsp;"
        return s
    
    tmp = head()
    tmp += "<body class='body_style'><div class='center'>"
    tmp += "<h2>" + "   " + title + "</h2>"
    tmp += "</div>"
    tmp += "<div class='help'>" + HLP_TXT.get(hlpkey) + "</div>"
    tmp += "<div class='status'><div class='status_title'>Port insights:<br></div>"
    tmp += str_keys("ap_st") + str_keys("ap_ssid") + "<br>"
    tmp += str_keys("sta_st") + str_keys("sta_ssid") + str_keys("sta_ip") + str_keys("sta_ga") + str_keys("sta_dns") + "<br>"
    tmp += str_keys("cred") + "<br>"
    tmp += str_keys("run") + "<br>"
    tmp += str_keys("mem") + "<br>"
    tmp += "</div>"
    return tmp;


def handleFooter(link, name):
    tmp = ""
    tmp += "<div>"+handleGet(link,name)+"</div>"
#    tmp += "<script src='/jquery224.js'></script>"
#    tmp += "<script src='/gh.js'></script>"
    tmp += '<br><div class="center">This&nbsp; <span>' + CONNECT_STATE["port"] + '</span>&nbsp;  is running on&nbsp; <span>' + CONNECT_STATE["python"] + '</span></div>'
    tmp += " </body></html>"
    #print(tmp)
    return tmp

def handleGet(lnk, name):
    tmp = "<form class='center' action='" + lnk + "' method='GET'>"
    tmp += "<input name='ButtonName' type='submit' class='button' value='" + name + "'></form> \n"
    return tmp

def handleFileAction(link, dir, fn):
    tmp = "<form action='" + link + dir + " 'method='GET'>"
    tmp += "<input name='dir' type='hidden' value='" + dir + "'>"
    tmp += "<input name='fn' type='hidden' value='" + fn + "'>"
    tmp += "<input name='button' type='submit' class='button_s' value='Download'>"
    tmp += "<input name='button' type='submit' class='button_s' value='Delete'>"
    tmp += "<label class='label_style'>" + fn + "</label>"
    tmp += "</form> \n"
    return tmp

def handlePost(path, name, txt, val): 
  tmp = "<div>"
  tmp += "<form action='" + path + "' method='POST'>" + txt + "<input type='text' name='message' placeholder='" + name + "' required>"
  tmp += "<input type='submit' class='button' name= '" + val + "' value='"+ val + "'>"
  tmp += "</form>"
  tmp += "</div> \n"
  return tmp

def handleMessage(message, blnk, bttn_name):
    tmp = handleHeader("OS-Manager Message ","")
    tmp += "<div class='message'>" + message + "</div>"
    tmp += handleFooter(blnk,bttn_name)
    return tmp


# Main Page
def handleRoot(Comment):
    tmp = handleHeader("OS-Manager  " + Comment, "root")
    tmp += handleGet("/ta","AccessPoint")
    tmp += handleGet("/ts","STA_Mode")
    tmp += handleGet("/wc","Credentials")
    tmp += handleGet("/dir/__","Filemanager")
    tmp += handleGet("/ur","Update Repo") + "<p>"
    if w.run_mode():
        tmp += handleGet("/rm", "Normal Run")+"<p>"
    else:    
        tmp += handleGet("/rm", "OS-Run")+"<p>"
    tmp += handleGet("/rb","Reboot") + "<p> \n"
    tmp += handleFooter("/","Back")
    return tmp

def handleUpload(dir):
    dir1 = dir
    if dir == "/":
        dir1 = "/__/"
    
    tmp = "File-Upload<br><div><form  id='form' action='/upload' method = 'POST'><input type='file' id='file' name='file'> <input type='submit' class='button_s' value='Upload'> </form>"
    tmp += " <script>async function upload(ev) { const file = document.getElementById('file').files[0]; if (!file) {return;}"
    tmp += "await fetch('/upload" + dir1 + "',"
    tmp += "{method: 'POST', credentials: 'include', body: file, headers: {'Content-Type': 'application/octet-stream', 'Content-Disposition': `attachment; filename=${file.name}`,},}).then(res => {console.log('Upload accepted');"
    tmp += "//alert('upload completed'); \n window.location.href = '/dir" + dir + "';}); ev.preventDefault();}"
    tmp += "document.getElementById('form').addEventListener('submit', upload); \n </script> </div> \n"
    return tmp

def handleFiles(dir):  
    def gen_dir_href(i):
        tmp = ""
        tmp += "<a href ='/dir"
        tmp +=  dir + i
        tmp += "' <text>"
        tmp +=  "(" + i + ")"
        tmp += "</text></a> "
        tmp += "<br>"
        return tmp

    def gen_dir_back_href():
        tmp = ""
        a2 = 1
        a1 = 0
        while a2>0:
            a = a1
            a1 = a2 - 1
            a2 = dir.find("/",a2) + 1
        if a1 == 0:
            return ""
        i = dir[:a]
        if i == "":
            i = "/__"
        tmp += "<a href ='/dir"
        tmp +=  i
        tmp += "' <text class='label_style'>"
        tmp +=  "(..)"
        tmp += "</text></a> "
        tmp += "<br>"
        return tmp
    
    print("handleFiles dir=", dir)
    if dir[-1] != "/":
        dir = dir + "/"
    if dir[0] != "/":
        dir = "/" + dir
    f = open("tmp/fm.html","w")    
    f.write(handleHeader("Filemanager  '" + dir + "'", ""))
    f.write("<div><div>")
    f.write(gen_dir_back_href())
    s = os.ilistdir(dir)   # directories
    for i in s:
        if i[1] == 0x4000:
            f.write(gen_dir_href(i[0]))
    s = os.ilistdir(dir)   # files
    for i in s:
        if i[1] == 0x8000:
            f.write(handleFileAction("/fm", dir, i[0]))
    if dir == '/':
        dir = '/__/'
    f.write("</div></div>")
    f.write("<br><br>" + handleUpload(dir) + "<br><br>") 
    f.write(handleFooter("/","Back"))
    f.close()
    return "./tmp/fm.html"


def handleScan_Networks():
    tmp = handleHeader("Wifi-Networks", "");
    tmp += w.scan_html()  
    tmp += "<br>" + handleGet("/scan", "Rescan") + handleGet("/wc", "Back to Input")
    tmp += handleFooter("/","Back")
    return tmp


def handleCredentials(json):
    tmp = handleHeader("Credentials", "");
    tmp += "<p>"+ handleGet("/scan","Scan Wifis") + "</p> \n"
    if w.creds():
        tmp +="<p>" + handleGet("/dc","Delete Credentials") + "\n"
        if w.creds_bak():
            tmp += handleGet("/sc","Swap Credentials")
    else:
        tmp += "<p> Credential-File doesn't exist </p><br> \n"
        if w.creds_bak():
            tmp += handleGet("/rc","Restore Credentials")
            
    
    tmp += "<p><form action='/creds_processing' method='POST'> \n"
    a = max(json.keys())
    for i in range(1,a+1):
        if json[i][1] == "checkbox":
            tmp += "<label for='" + json[i][0] + "'>" + json[i][2] + "</label> <input type='" + json[i][1] + "' name='" + json[i][0] +"' placeholder='" + json[i][0] + "' value='True'><br><br> \n"
        else:    
            tmp += "<label for='" + json[i][0] + "'>" + json[i][2] + "</label> <input type='" + json[i][1] + "' name='" + json[i][0] +"' placeholder='" + json[i][0] + "' value=''> <br><br> \n"
    tmp += "<input type='submit' class='button' name='SUBMIT' value='Store Creds'></form>"
    tmp += "</p>"    
    tmp += handleFooter("/","Back")
    return tmp


#EXAMPLE_ASSETS_DIR = '/example-assets'
naw = Nanoweb(80, debug=False)
#, dir=EXAMPLE_ASSETS_DIR)
# naw.assets_extensions += ('ico',)
#naw.STATIC_DIR = EXAMPLE_ASSETS_DIR
naw.STATIC_DIR = "/"
refresh_connect_state()


# Declare route directly with decorator
@naw.route('/')
async def hello(r):
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleRoot(""))
    
# Declare route directly with decorator
@naw.route('/ta')
async def toggle_ap(r):
    if not(w.set_sta()):
        await r.write("HTTP/1.1 200 OK\r\n\r\n")
        await r.write(handleMessage("You couldn't release both (AP, STA), then you loose the connection to the port", "/", "Back"))
    else:
        w.set_ap(not(w.set_ap()))
        refresh_connect_state()
        await r.write("HTTP/1.1 200 OK\r\n\r\n")
        await r.write(handleRoot(""))
    
# Declare route directly with decorator
@naw.route('/ts')
async def toggle_sta(r):
    if not(w.set_ap()):
        await r.write("HTTP/1.1 200 OK\r\n\r\n")
        await r.write(handleMessage("You couldn't release both (AP, STA), then you loose the connection to the port", "/", "Back"))
    else:    
        w.set_sta(not(w.set_sta()))
        refresh_connect_state()
        await r.write("HTTP/1.1 200 OK\r\n\r\n")
        await r.write(handleRoot(""))
        
# Declare route directly with decorator
@naw.route('/rm')
async def toggle_run_mode(r):
        w.run_mode(not(w.run_mode()))
        refresh_connect_state()
        await r.write("HTTP/1.1 200 OK\r\n\r\n")
        await r.write(handleRoot(""))

@naw.route('/wc')
async def creds(r):
#     print(r.url)
#     print(r.route)
#     print(r.headers)
#     print(r.param)
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleCredentials(JSON))

@naw.route('/scan')
async def scan_networks(r):
#     print(r.url)
#     print(r.route)
#     print(r.headers)
#     print(r.param)
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleScan_Networks())

@naw.route('/creds_processing')
async def creds_processing(r):
#    print(r.path, r.args)
#     print(r.url)
#     print(r.route)
#     print(r.headers)
#     print(r.args)
#     print(r.param)

    json = {}
    a = max(JSON.keys())
    for i in JSON.keys():
        json[JSON[i][0]] = "0"       
    for i in r.args.keys():
        if r.args[i]=="True":
            json[i] = "1"
        else:    
            json[i] = r.args[i]
    print(json)    
    w.store_creds(json)
    refresh_connect_state()
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleRoot(""))


@naw.route('/dc')
async def del_cred(r):
    w.delete_creds()
    print("Credentials moved to bak")
    refresh_connect_state()
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleCredentials(JSON))

@naw.route('/sc')
async def del_cred(r):
    w.swap_creds()
    print("Credentials swapped")
    refresh_connect_state()
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleCredentials(JSON))
    
@naw.route('/rc')
async def del_cred(r):
    w.restore_creds()
    refresh_connect_state()
    print("Credentials restored")
    await r.write("HTTP/1.1 200 OK\r\n\r\n")
    await r.write(handleCredentials(JSON))


@naw.route('/rb')
async def reboot(r):
    machine.reset()
    return handleRoot(""), 201

@naw.route('/upload/*')
async def upload(r):
#     print("UPLOAD-API")
#     print(r.headers)
#     print(r.url)
#     print(r.route)
#     print(r.param)
#     print(r.args)
    dir = r.url.strip("/upload/")
#     print("dir: " + dir)
    if dir == "__":
        dir = "/"
    else:
        dir = "/" + dir.strip("/") + "/"    

    if r.method == "POST":
#        raise HttpError(request, 501, "Not Implemented")

        # obtain the filename and size from request headers
        filename = r.headers['Content-Disposition'].split('filename=')[1].strip('"')
        size = int(r.headers['Content-Length'])
        # sanitize the filename
        # write the file to the files directory in 1K chunks
#         print("Upload: ", dir + filename, size) 
        with open(dir + filename, 'wb') as f:
            while size > 0:
                chunk = await r.read(min(size, 1024))
                f.write(chunk)
                size -= len(chunk)
            f.close()        
        print('Successfully saved file: ' + dir + filename)
        await r.write("HTTP/1.1 201 Upload \r\n" )
    else:
        rp = handleFiles(dir)
        await r.write("HTTP/1.1 200 OK\r\n")
        await send_file(r, rp)

# @naw.route('/download*')
# async def static(r, fn):
#     print("download: <" + fn + ">")
#     return send_file(r, fn)

# fm = filemgmt -> download or delete
@naw.route('/fm*')
async def fm(r):
#     print(r.url)
#     print(r.route)
#     print(r.param)
#     print(r.args)
    filename = r.param["fn"]
    direct = r.param["dir"]

    if r.param["button"]=="Delete":
        print("delete file: " + direct+filename)
        try:
            os.remove(direct+filename)
        except OSError as e:
            raise HttpError(r, 500, "Internal error")
        rp = handleFiles(direct)
        await r.write("HTTP/1.1 200 OK\r\n")
        await send_file(r, rp)
    elif r.param["button"]=="Download":
        print("download file: " + filename)
        await r.write("HTTP/1.1 200 OK\r\n") 
        await r.write("Content-Type: application/octet-stream\r\n")
        await r.write("Content-Disposition: attachment; filename=%s\r\n\r\n" % filename)
        await send_file(r, direct+filename)
        rp = handleFiles(direct)
        await r.write("HTTP/1.1 200 OK\r\n")
        await send_file(r, rp)


@naw.route('/dir*')
async def set_dir(r):
    print(r.url)
    print(r.route)
    new_dir = r.url[5:]
    if new_dir.startswith("__"):
        rp = handleFiles("/")
        await r.write("HTTP/1.1 200 OK\r\n")
        await send_file(r, rp)
    else:
        rp = handleFiles(new_dir)
        await r.write("HTTP/1.1 200 OK\r\n")
        await send_file(r, rp)


@naw.route('/assets/*') 
async def assets(request):
    await request.write("HTTP/1.1 200 OK\r\n")
    print("assets")
    print(request.url)
    print(request.route)
    print(request.param)
    print(request.args)
    filename = request.url.split('/')[-1]
    if filename.endswith('.png'):
        args = {'binary': True}
    await request.write("\r\n")
    await send_file(
        request,
        './%s/%s' % (EXAMPLE_ASSETS_DIR, filename),
#        **args,
    )



loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()

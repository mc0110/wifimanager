import web_os
from nanoweb import Nanoweb
import uasyncio as asyncio

# debug=True for debugging
naw = Nanoweb(80)

naw.STATIC_DIR = "/"
naw.routes = {
     '/': web_os.index,
     '/ta': web_os.toggle_ap,
     '/ts': web_os.toggle_sta,
     '/rm': web_os.toggle_run_mode,
     '/wc': web_os.creds,
     '/scan': web_os.scan_networks,
     '/creds_processing': web_os.creds_processing,
     '/dc': web_os.del_cred,
     '/sc': web_os.swp_cred,
     '/rc': web_os.res_cred,
     '/rb': web_os.reboot,
     '/upload/*': web_os.upload,
     '/fm*': web_os.fm,
     '/dir*': web_os.set_dir,
 }


loop = asyncio.get_event_loop()
loop.create_task(naw.run())
loop.run_forever()        


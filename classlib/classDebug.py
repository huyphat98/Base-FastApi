import sys, os,json,time, string
from cnnmongodb import mongodb
import pymongo
from datetime import datetime
## Debug mode de check error 
debug = 0

## File luu tru debug de kiem tra loi trong qua trinh thao tac
path_debug = "/tmp/broadcast_audio.log"

############################################################
#Debug modules
############################################################
def Log(module, err):
    if debug:
        time_debug = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        debug_msg = "{}:::{}:::{}:::{}\n".format(module, time_debug, err.message, err.args)
        os.system("echo {} >> {}".format(debug_msg,path_debug))

import datetime
import subprocess,psutil
from schema import Schema, And, Use, Optional, SchemaError

construct = {
  "user":str,
  "pid":str,
  "cpu_percent":str,
  "mem_percent":str,
  "vsz":str,
  "rss":str,
  "tty":str,
  "stat":str,
  "start":str,
  "time":str,
  "cmd":str
}

## Parse now time to str to save db
def ParseNowTimeToStr():
    currentDT = datetime.datetime.now()
    # print (currentDT.strftime("%Y-%m-%d %H:%M:%S"))
    # print (currentDT.strftime("%Y/%m/%d"))
    # print (currentDT.strftime("%H:%M:%S"))
    # print (currentDT.strftime("%I:%M:%S %p"))
    # print (currentDT.strftime("%a, %b %d, %Y"))
    return currentDT.strftime("%Y%m%d%H%M%S")

## Change
def TimestampVal(str_time, time_format):
    """
    Desc:
        Parse string time to timestamp for compare
    Args:
        str_time (_type_): string time with format follow time_format
            Example: time_format = "%Y-%m-%d", str_time = 2022-05-02
        time_format (_type_): example "%Y%m%d%H%M": 202205021028 
                                            or "%Y%m%d": 20220502
    Returns:
        _type_: float
    """
    #element = datetime.datetime.strptime(str_time,"%Y%m%d%H%M")
    element = datetime.datetime.strptime(str_time,time_format)
    timestamp = datetime.datetime.timestamp(element)    
    return float(timestamp)

def ChangeStrTime2Format(strtime, time_format):
    """
    Desc:
        Change time from string (backend use it) to format request (web use it)
    Args:
        strtime (_type_): time string. Example: 202205021100
        time_format (_type_): time_format. Example = "%Y-%m-%d", result function 
            will be:2022-05-02 or if "%d/%m/%Y" will be 02/05/2022
    Returns:
        _type_: time with format follow time_format type
    """
    element = datetime.datetime.strptime(strtime,time_format) 
    return element

def ReturnCode(code_name, msg, status):
    code = {
        "code":code_name,
        "msg": msg,
        "status": bool(status)
    }
    return dict(code)

def help():
    print ("[1]. ParseNowTimeToStr")
    print ("[2]. TimestampVal")
    print ("[3]. ChangeStrTime2Format")
    key = ("--> Chose function: ").strip()
    if key in [1,"1"]:
        print ("[1]. ParseNowTimeToStr------------------------------")
        print (ParseNowTimeToStr.__doc__)
    elif key in [2,"2"]:
        print ("[2]. TimestampVal------------------------------")
        print (TimestampVal.__doc__)
    elif key in [3,"3"]:
        print ("[3]. ChangeStrTime2Format------------------------------")
        print (ChangeStrTime2Format.__doc__)
############################################################################
########                Parse lenh aux va luu tru thanh construct
############################################################################
def ParseAux(name_of_grep,item):
  cmd = "sudo ps -aux | grep {}".format(name_of_grep)
  pytonProcess = subprocess.check_output(cmd,shell=True).decode()
  pytonProcess = pytonProcess.split('\n')  
  res = []
  for process in pytonProcess:
      #print(process)
      ## Raplaced multi space to one space
      str = ' '.join(process.split())
      #print ("str after cut space: ", str)
      if item not in str:
        continue
      ## Parse ra day du thong so 
      else:
        arr =  str.split(" ")
        construct["user"] = arr[0]
        construct["pid"] = arr[1]
        construct["cpu_percent"] = arr[2]
        construct["mem_percent"] = arr[3]
        construct["vsz"] = arr[4]
        construct["rss"] = arr[5]
        construct["tty"] = arr[6]
        construct["stat"] = arr[7]
        construct["start"] = arr[8]
        construct["time"] = arr[9]
        construct["cmd"] =""
        for each in arr[10: ]:
          construct["cmd"] = construct["cmd"]+ each + " "
        construct["cmd"] = construct["cmd"].strip()         ## Bo khoang trang cuoi cung 
        res.append(dict(construct))
  return (res)







############################################################################
########                Check Proccess is running or stop
############################################################################
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
############################################################################
########                Get PID with name
############################################################################
def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    assert name, name
    ls = []
    for p in psutil.process_iter():
        name_, exe, cmdline = "", "", []
        try:
            name_ = p.name()
            cmdline = p.cmdline()
            exe = p.exe()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except psutil.NoSuchProcess:
            continue
        if name == name_ or name in cmdline  or os.path.basename(exe) == name:
            ls.append(p)
    return ls
############################################################################
########                Kill process by name and item
############################################################################
def KillProccess(name_of_process,item):
    for each in ParseAux(name_of_process,item):   
        cm_check = 'sudo kill -9 {}'.format(each["pid"])
        status = subprocess.run(cm_check, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,\
                                    stderr=subprocess.STDOUT)
    return
############################################################################
########                Kill process by name and item
############################################################################
def KillProccessByPID(pid_num):
    cm_check = 'sudo kill -9 {}'.format(int(pid_num))
    status = subprocess.run(cm_check, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,\
                                    stderr=subprocess.STDOUT)
    return

def CheckStructure(base_schema, request_schema):
    """
    Desc:
        Check schema of list
    Args:
        base_schema (_type_): base schema
        request_schema (_type_): scheme which you must check
    Returns:
        _type_: boolean
        _value_: True or False
    """
    try:
        base_schema.validate(request_schema)
        return True
    #except SchemaError:
    except:
        return False  
    

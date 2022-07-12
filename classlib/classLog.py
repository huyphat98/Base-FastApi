import os
import json
from datetime import datetime
from classMongodb import mongodb
import classDebug
MODULE_NAME="ClassLog"

###### Varialble define ##########
configlog={
   "time":"",
   "timestamp":"",
   "from":"",
   "object":"",
   "operate":"",
   "param": ""
}
systemlog={
   "time":"",
   "timestamp":"",
   "filename":"",
   "log":""
}
listSystemlog=[]

absolute_path=os.path.dirname(os.path.abspath(__file__))
config_file = "{}/config.json".format(absolute_path)
############# Write data to json #############
def write_json(new_data, filename):
    jsonString = json.dumps(new_data)
    jsonFile = open(filename, "w+")
    jsonFile.write(jsonString)
    jsonFile.close()
################################################
#Add log config module
################################################
def logconfigadd(fromm,obj,operate,param):
   try:
       now = datetime.now()
       time = now.strftime("%d-%m-%Y %H:%M")
       configlog["time"]=time
       configlog["timestamp"]=now.timestamp()

       configlog["from"]=fromm
       configlog["object"]=obj
       configlog["operate"]=operate
       configlog["param"]=param

       config = json.loads(open(config_file, 'r').read())
       db = mongodb()
       db.col(config['db']['colLog'])
       x = db.mycol.update_one(configlog,{'$set':configlog},upsert=True)
       db.closedb()
       del db
   except Exception as e :
        classDebug.Log(MODULE_NAME,e)
#############################################################
#System log module
#############################################################
def logsystemadd(filename,fail):
  try:
       config = json.loads(open(config_file, 'r').read())
       pathlog=config['path']['log']
       
       listSystemlog=json.loads(open(pathlog, 'r').read())
       now = datetime.now()
       systemlog["time"]= now.strftime("%Y-%m-%d %H:%M")
       systemlog["timestamp"]=now.timestamp()
       systemlog["filename"]=filename
       systemlog["log"]=fail
       listSystemlog.append(systemlog)
       write_json(listSystemlog,pathlog)
  except Exception as e:
        classDebug.Log(MODULE_NAME,e)
################################################
# Log system module
################################################
def GetConfigLog(time):
   
    list_result=[]
    list_field=[]
    config = json.loads(open(config_file, 'r').read())
    db = mongodb()
    db.col(config['db']['colLog'])
    try:
        time= jsonable_encoder(time)
        timeStampstart=datetime.strptime(time['timeStart'], "%Y-%m-%d %H:%M").timestamp()
        timeStampend=datetime.strptime(time['timeEnd'], "%Y-%m-%d %H:%M").timestamp()
        res=db.mycol.find({},{"_id":0,"timestamp":1,"from":1,"object":1,"operate":1,"param":1,"time":1})
        for x in res:
            list_field.append(x)
        for x in list_field :
           if x['timestamp'] >= timeStampstart and x['timestamp'] <= timeStampend:
              x['param']=str(x['param'])
              list_result.append(x)
    except Exception as e :
       logsystemadd(MODULE_NAME,str(e)) 
    finally:
       logconfigadd("Web","Config Log","Post",time) 
    return list_result
#####################################################
#Log config module
#####################################################
def GetSystemLog(time):
    logResult=[]
    config = json.loads(open(config_file, 'r').read())
    try:
       time= jsonable_encoder(time)
       timeStampstart=datetime.strptime(time['timeStart'], "%Y-%m-%d %H:%M").timestamp()
       timeStampend=datetime.strptime(time['timeEnd'], "%Y-%m-%d %H:%M").timestamp()
       listLog = json.loads(open(config['path']['log'], 'r').read())
       for logs in listLog:
           if logs['timestamp']>=timeStampstart and logs['timestamp'] <=timeStampend:
              logResult.append(logs)
    except Exception as e:
       logsystemadd(MODULE_NAME,str(e))
    finally:
       logconfigadd("Web","System Log","Post",time)
    return logResult
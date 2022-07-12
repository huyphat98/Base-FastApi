from classMongodb import mongodb
from datetime import datetime
from datetime import timedelta
import classCommon
from schema import Schema, And, Use, Optional, SchemaError
from bson.objectid import ObjectId


TEST_CLASS = 0

base_schema = Schema({
    "name": And(Use(str)),
    "time_start": And(Use(str)),
    "date": And(Use(str)),
    "source": And(Use(str)),
    "duration": And(Use(int)),
    "priority": And(Use(int)),
    "type": And(Use(int)),
    "isPlayed": And(Use(int)),
    "format": And(Use(str)),
    "bitrate": And(Use(str)),
    "played_time": And(Use(str)),
    "created_by":And(Use(str))
})

clone_schema_date = Schema({
    "date":And(Use(str)),
    "from_date":And(Use(str)),
     "to_date":And(Use(str))
})

clone_schema_id= Schema({
    "id":And(Use(ObjectId)),
    "from_date":And(Use(str)),
     "to_date":And(Use(str))
})

## Class Schedule : only manage schedule of station id--
class Schedule():
    def __init__(self, db_name="schedule", station_id = "none", debug = False):
        self.debug = debug
        self.db_name = str(db_name)
        self.station_id = str(station_id)                              ## Ma dinh danh duy nhat 
        self.schedule_tbl = "{}".format(station_id)         ## vi du collection jfjruirie

    ## Add Schedule
    def PreCheckSchedule(self,schedule_info):
        ## Khong duoc lap lich phat sau hien tai 
        date = schedule_info["date"]
        time = schedule_info["time_start"]
        time_all = "{}{}".format(date,time)
        info_timestamp=classCommon.TimestampVal(time_all,"%Y%m%d%H%M%S")
        nowtime_timestamp = classCommon.TimestampVal(classCommon.ParseNowTimeToStr(),"%Y%m%d%H%M%S")
        if (info_timestamp < nowtime_timestamp): 
            if self.debug: 
                print ("Err: info_timestamp < nowtime_timestamp: ",info_timestamp, "  ", nowtime_timestamp ) 
            return False
        
        ## Xu ly trung lich (khong duoc cung time voi lich da ton tai) hoac neu trung thi do uu tien phai
        ## khac nhau
        mongo =  mongodb(dbname=self.db_name)
        data_query = {"time_start":str(schedule_info["time_start"])}
        record_schedule = mongo.GetCollection(self.schedule_tbl, condition = data_query) 
        if len(record_schedule) > 0:
            ## Same time and priority
            for each in record_schedule:
                if each["priority"] == schedule_info["priority"]:    
                    if self.debug: 
                        print ("---------------------------------------------------")
                        print ("Err: Schedule duplicated: ", record_schedule) 
                        print ("---------------------------------------------------")
                    return False
        return True

    ## Them noi dung lap lich 
    def ScheduleAdd(self, add_param):
        """
        Desc:
            Add schedule
        Args:
            add_param (_type_):   dict with schema 
           {
               "name": And(Use(str)),
                "time_start": And(Use(str)),
                "date": And(Use(str)),
                "source": And(Use(str)),
                "duration": And(Use(int)),
                "priority": And(Use(int)),
                "type": And(Use(int)),
                "isPlayed": And(Use(int)),
                "format": And(Use(str)),
                "bitrate": And(Use(str)),
                "played_time": And(Use(str)),
                "created_by":And(Use(str))
            }
        Returns:
            _type_: boolean
            _value_: True or False
        """
        schedule_info= add_param
        ## Check schema before add
        if classCommon.CheckStructure(base_schema,schedule_info):
            try:
                if False == self.PreCheckSchedule(schedule_info):
                    return False
                mongo =  mongodb(dbname=self.db_name)
                nowtime = classCommon.ParseNowTimeToStr()
                schedule_info["modify_time"] = nowtime       ## Update time by user 
                return mongo.InsertOneCol(self.schedule_tbl, schedule_info)
            except Exception as e:
                if self.debug: 
                    print ("Debug::", e)
                return False
        else: 
            if self.debug: 
                print ("Check fail CheckStructure")
            return False
    
    ## ------Remove schedule ----
    def ScheduleRemove(self, type = "all", param="none"):
        """
        Desc: 
            Remove Schedule with some param
        Args:
            type (str, optional): _description_. Defaults to "all". 
                + all: get all schedule
                + date: get schedule with date  (format yyyymmdd)
                + id: get schedule with _id mongo
            param (str, optional): _description_. Defaults to "none".
        Returns:
            _type_: boolean
        """
        mongo =  mongodb(dbname=self.db_name)
        if type.lower() in ["all"]:         # Get all
            return  mongo.DocumentDelete(self.schedule_tbl,condition = "all")
        elif type.lower() in ["date"]:  ## Get by date format: yyyymmdd
            data_query = {"date": str(param)}
            return  mongo.DocumentDelete(self.schedule_tbl, condition=data_query)
        elif type.lower() in ["id"]:    # Get by ID mongoDB
            data_query = {"_id": ObjectId(param)}
            return  mongo.DocumentDelete(self.schedule_tbl, condition=data_query)
        return False

    ## Edit schedule 
    def ScheduleEdit(self, obj_id, schedule_info):
        """
        Desc:
            Edit schedule 
        Args:
            obj_id (_type_): object id mongo
            schedule_info (_type_): dictionary, schema:
            {
                "name": And(Use(str)),
                "time_start": And(Use(str)),
                "date": And(Use(str)),
                "source": And(Use(str)),
                "duration": And(Use(int)),
                "priority": And(Use(int)),
                "type": And(Use(int)),
                "isPlayed": And(Use(int)),
                "format": And(Use(str)),
                "bitrate": And(Use(str)),
                "played_time": And(Use(str)),
                "created_by":And(Use(str))
            }
        Returns:
            _type_: boolean
            _value_: True or False
        """
        # Khong cho phep edit thoi gian lui ve truoc hien tai
        date = schedule_info["date"]
        time = schedule_info["time_start"]
        time_all = "{}{}".format(date,time)
        info_timestamp = classCommon.TimestampVal(time_all,"%Y%m%d%H%M%S")
        nowtime_timestamp = classCommon.TimestampVal(classCommon.ParseNowTimeToStr(),"%Y%m%d%H%M%S")
        if (info_timestamp < nowtime_timestamp): 
            if self.debug: 
                print ("Err: edit info_timestamp < nowtime_timestamp: ",info_timestamp, "  ", nowtime_timestamp ) 
            return False 
        mongo =  mongodb(dbname=self.db_name)            
        query ={"_id": ObjectId(obj_id)}
        schedule_info["modify_time"]= str(classCommon.ParseNowTimeToStr())
        return mongo.DocumentUpdate(self.schedule_tbl,query,schedule_info)           

    ## Get schedule with some options
    def ScheduleGet(self, type="all", param="none"):
        """
        Desc: 
            Get Schedule with some param
        Args:
            type (str, optional): _description_. Defaults to "all". 
                + all: get all schedule
                + date: get schedule with date  (format yyyymmdd)
                + id: get schedule with _id mongo
            param (str, optional): _description_. Defaults to "none".
        Returns:
            _type_: list with emty or some elements with schema
            {
                "name": And(Use(str)),
                "time_start": And(Use(str)),
                "date": And(Use(str)),
                "source": And(Use(str)),
                "duration": And(Use(int)),
                "priority": And(Use(int)),
                "type": And(Use(int)),
                "isPlayed": And(Use(int)),
                "format": And(Use(str)),
                "bitrate": And(Use(str)),
                "played_time": And(Use(str)),
                "created_by":And(Use(str)),
                "modify_time":And(Use(str))
            }
        """
        mongo =  mongodb(dbname=self.db_name)
        if type.lower() in ["all"]:         # Get all
            return  mongo.GetCollection(self.schedule_tbl)
        elif type.lower() in ["date"]:  ## Get by date format: yyyymmdd
            data_query = {"date": str(param)}
            return  mongo.GetCollection(self.schedule_tbl, condition=data_query)
        elif type.lower() in ["id"]:    # Get by ID mongoDB
            data_query = {"_id": ObjectId(param)}
            return  mongo.GetCollection(self.schedule_tbl, condition=data_query)
        else: 
            return []

    ## Replication schedule (Nhan ban lap lich phat theo ngay hoac theo mot record)
    def ScheduleReplication(self, type = "date", schedule_clone="none"):
        ## Neu nhan ban lap lich theo date
        if type == "date":
            if False == classCommon.CheckStructure(clone_schema_date, schedule_clone):
                if self.debug:
                    print ("Debug::schedule_clone not support schema: ", schedule_clone)
                return False
            query = schedule_clone["date"]
        elif type == "id":
            if False == classCommon.CheckStructure(clone_schema_id, schedule_clone):
                if self.debug:
                    print ("Debug::schedule_clone not support schema: ", schedule_clone)
                return False
            query = schedule_clone["id"]
        else: 
            return False
        mongo =  mongodb(dbname=self.db_name)     
        ## get all record in day table
        record_in_day = self.ScheduleGet(type="date", param=query)
        if len(record_in_day) <=0:
            if self.debug:
                print ("Debug::Date clone not valid schedule")
            return False

        ## Remove and insert record to clone day
        start = classCommon.ChangeStrTime2Format(schedule_clone["from_date"], "%Y%m%d")
        end =classCommon.ChangeStrTime2Format(schedule_clone["to_date"], "%Y%m%d")
        date_sum=(end-start).days+1
        list_date_duplicate=[]
        date_current = datetime.strptime(schedule_clone["from_date"], "%Y%m%d")
        for i in range (0,date_sum):
            date_next=date_current+timedelta(days=i)
            date_next=date_next.strftime('%Y%m%d')      ## change to yyyymmdd
            list_date_duplicate.append(date_next)

        #Delete db
        for i in range(0,len(list_date_duplicate)):
            data_query ={ "date": list_date_duplicate[i]}
            mongo.DocumentDelete(self.schedule_tbl, condition=data_query)
                
        # Create Schedule -----
        for index in range(0,date_sum): 
            for schedule in record_in_day:
                schedule["date"]=list_date_duplicate[index]
                del schedule["_id"]     ## Xoa vi khong su dung den 
                if False == mongo.InsertOneCol(self.schedule_tbl, schedule):
                    if self.debug:
                        print ("Debug::mongo.InsertOneCol return false")
                    return False
        return True
    
    # Lay tong so trang thai bai hat
    def NumberOfSong(self,date):
        """
        Desc: 
            Total number songs is played, not played or playing
        Args:
            date (_type_): date format yyyymmdd
        Returns:
            _type_: dict, schema:
            {
                "totalPlayed": played, 
                "totalYet": playyet, 
                "playing": playing
            }
        """
        responses = dict()
        mongo =  mongodb(dbname=self.db_name)
        data_query = {"date": date}
        listScheduleOfDay = mongo.GetCollection(self.schedule_tbl, condition=data_query)
        # 0 - chưa, 1 đang, 2 đã
        played = 0
        playing = 0
        playyet = 0
        for data in listScheduleOfDay:
            try:
                if data['isPlayed'] in ['2',2]:
                    played = played + 1
                elif data['isPlayed'] in ['0',0]:
                    playyet = playyet + 1
                elif data['isPlayed'] in ['1',1]:
                    playing = playing + 1
            except Exception as e:
                e = "id: {0} ,không có trường {1}".format(data.get("_id"), e)
                if self.debug:
                    print ("Debug:: ",e)
        responses.update({"totalPlayed": played, "totalYet": playyet, "playing": playing})
        return responses

    def help(self):
        print ("[1]. ScheduleGet------------------------------")
        print (self.ScheduleGet.__doc__)
        print ("[2]. ScheduleAdd------------------------------")
        print (self.ScheduleAdd.__doc__)
        print ("[3]. ScheduleEdit------------------------------")
        print (self.ScheduleEdit.__doc__)
        print ("[4]. ScheduleRemove-------------------------")
        print (self.ScheduleRemove.__doc__) 
        print ("[5]. ScheduleReplication---------------------")
        print (self.ScheduleReplication.__doc__)            
        print ("[5]. NumberOfSong---------------------")
        print (self.NumberOfSong.__doc__) 

if TEST_CLASS:
    schedule = Schedule(station_id="test_schedule_12345", debug = True)
    print ("Add schedule to station")
    print ("\n\n\n\n")
    param = dict({
        "name": "Phát thanh quận Tân Phú", 
        "time_start": "170000",
        "date": "20220503",
        "source": "file_amthanh_tanphu.mp3",
        "duration": 100,
        "priority": 1,
        "type": 1,
        "isPlayed": 0,
        "format": "mp3",
        "bitrate": "128",
        "played_time": 10,
        "created_by":"admin"
    })
    print ("Result add: ", schedule.ScheduleAdd(param))
    print ("Result get: ", schedule.ScheduleGet(type="all",param="626e88f064b26a3c0e4d5845"))
    print ("Result get: ", schedule.ScheduleGet(type="date",param="20220503"))
    clone_date = {
        "date":"20220503",
        "from_date":"20220504",
        "to_date":"20220510",
    }
    print ("Duplicate add: ", schedule.ScheduleReplication(type = "date", schedule_clone=clone_date))
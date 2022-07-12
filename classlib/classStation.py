import subprocess
import os
from classMongodb import mongodb
from datetime import datetime
from schema import Schema, And, Use, Optional, SchemaError
import classCommon

station_schema = Schema({
    "station_id": And(Use(str)),
    "location_id": And(Use(str)),
    "station_name": And(Use(str)),
    "rtsp_port": And(Use(int)),
    "icecast_port": And(Use(int)),
    "rtmp_port": And(Use(int)),
    "rtsp_subpath": And(Use(str)),
    "ices_subpath": And(Use(str)),
    "created_by": And(Use(str))
})

## Truy van vao 2 database cung luc 
class Station():
    def __init__(self, global_db="global", station_db="station", debug = 0):
        self.debug = debug
        self.global_db = str(global_db)
        self.station_db = str(station_db)
    
    # Create station with schema (please remove all schedule with station id)
    def StationCreate(self, param_input):
        if classCommon.CheckStructure(station_schema,param_input):
            # Kiem tra db da ton tai du lieu     
            pass
        else: 
            if self.debug: print ("Debug:: input schema not true!")
            return False
        return True



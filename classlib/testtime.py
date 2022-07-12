import time
import datetime
string = "20220502" 
element = datetime.datetime.strptime(string,"%Y%m%d")
print ("element = ", element)
timestamp = datetime.datetime.timestamp(element)
print("timestamp = ",timestamp)



date_time_str = '18/09/19 01:55:19'
date_time_obj = datetime.datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)
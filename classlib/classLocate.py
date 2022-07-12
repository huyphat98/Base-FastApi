from classlib.classMongodb import mongodb
from datetime import datetime

## Level max to search 
MAXLEVEL_SUPPORT = 5
TEST_CLASS = 0

ADMIN_LEVEL= 0
NATION_LEVEL=1
PROVINCE_LEVEL=2
DISTRICT_LEVEL=3
WARD_LEVEL=4
QUARTER_LEVEL=5

LOG_FILE_PATH = "/var/log/api-gateway/err.log"
class LocationManager: 
    db_name = ""
    debug = 0
    locate_tbl = ""
    province_tbl = ""
    ward_tbl = ""
    quarter_tbl = ""

    ## Init db_name
    def __init__(self, db_name="global", locate_tbl="tbl_location", province_tbl="tbl_province", \
        district_tbl="tbl_district", ward_tbl = "tbl_ward",quarter_tbl = "tbl_quarter", debug = 0):
        self.debug = debug
        self.db_name = str(db_name)
        self.locate_tbl = str(locate_tbl)
        self.province_tbl = str(province_tbl)
        self.district_tbl = str(district_tbl)
        self.ward_tbl = str(ward_tbl)
        self.quarter_tbl = str(quarter_tbl)

    ## Get info from tbl_province
    def ProvinceGet(self, province_id,field = "none"):
        mongo =  mongodb(dbname=self.db_name)
        data_query = {"province_id": str(province_id)}                              ## Cau truc query command 
        if province_id.lower() in ["all"]:
            data_query = "all"
        if field.lower() in ["none", "all"]:
            return mongo.GetCollection(self.province_tbl,condition=data_query)
        else:
            return mongo.GetCollectionDistinct(self.province_tbl,condition=data_query,field=field)           

    ## Get info from tbl_district
    def DistrictGet(self, province_id,district_id="all",field = "none"):
        mongo =  mongodb(dbname=self.db_name)
        if district_id.lower() in ["all"]:
            data_query = {"province_id": province_id}
        else:
            data_query = {"$and": [{"province_id": province_id}, 
                {"district_id": district_id}]}
        if field.lower() in ["none", "all"]:
            return mongo.GetCollection(self.district_tbl,condition=data_query)
        else:
            return mongo.GetCollectionDistinct(self.district_tbl,condition=data_query,field=field)            

    ## Get info from tbl_ward
    def WardGet(self, province_id,district_id,ward_id="all", field = "none"):
        mongo =  mongodb(dbname=self.db_name)
        if ward_id.lower() in ["all"]:
            data_query = {"$and": [{"province_id": province_id}, 
                {"district_id": district_id}]}
        else:
            data_query = {"$and": [{"province_id": province_id}, 
                {"district_id": district_id},{"ward_id": ward_id}]}
        if field.lower() in ["none", "all"]:        
            return mongo.GetCollection(self.ward_tbl,condition=data_query)
        else:
            return mongo.GetCollectionDistinct(self.ward_tbl,condition=data_query, field=field)
       
    ## Get info from tbl_quarter
    def QuarterGet(self, province_id,district_id,ward_id,quarter_id="all", field = "none"):
        mongo =  mongodb(dbname=self.db_name)
        if quarter_id.lower() in ["all"]:
            data_query = {"$and": [{"province_id": province_id}, 
                {"district_id": district_id},{"ward_id": ward_id}]}
        else:
            data_query = {"$and": [{"province_id": province_id}, 
                {"district_id": district_id},{"ward_id": ward_id},
                {"quarter_id": quarter_id}]}            
        if field.lower() in ["none", "all"]:
            return mongo.GetCollection(self.quarter_tbl,condition=data_query)
        else:
            ## Chi get ve thong tin mong  muon---
            return mongo.GetCollectionDistinct(self.quarter_tbl,condition=data_query, field=field)
        
    ## Get info from tbl_location----
    def LocationIDGet(self,location_id):
        mongo =  mongodb(dbname=self.db_name)
        data_query = {"location_id": str(location_id)}
        return mongo.GetCollection(self.locate_tbl,condition=data_query)       
    
    ## Return location_id from other variables -----
    def LocationIDSearch(self,province_id="none", district_id="none",\
            ward_id="none", quarter_id="none", maxlevel="none",field = "none"):
        tmp = []
        try:
            mongo =  mongodb(dbname=self.db_name)
        except Exception as e:
            str_err = ("LocationIDSearch connect mongo err: ",e)
            date = datetime.now()
            ##Bug: Please transfer log to file at here
            
        if province_id!="none":
            tmp.append(dict({"province_id": province_id}))
        if district_id!="none":
            tmp.append(dict({"district_id": district_id}))    
        if ward_id!="none":
            tmp.append(dict({"ward_id": ward_id}))   
        if quarter_id!="none":
            tmp.append(dict({"quarter_id": quarter_id}))    
        if maxlevel != "none":
            tmp.append(dict({"maxlevel": maxlevel}))     
        data_query = {"$and": tmp}  
        if field.lower() in ["none", "all"]:
            return mongo.GetCollection(self.locate_tbl,condition=data_query)
        else:
            ## Chi get ve thong tin mong  muon---
            return mongo.GetCollectionDistinct(self.locate_tbl,condition=data_query, field=field)
                
    ## Get all data from tbl_locate and parse, sample khu phố 1, phường 12, quận Tân Bình, Hồ Chí Minh
    ## Get toan bo cac vung quan ly tuong ung voi location ID ==> Gom chinh ID can tim va cac location con
    def LocationListManage(self, location_id):
        out = []
        tmp_out = {
            "name":"",
            "location_id":""
        }
        if self.debug:
            print ("LocationNameGet is called\n")
        locate_list = self.LocationIDGet(location_id = location_id)
        if  len(locate_list) > 1: 
            if self.debug: print ("localtion_id have more than 1 in {}".format(self.locate_tbl))
            return out
        else: 
            maxlevel = locate_list[0]["maxlevel"]          ## Tim cap quan ly tuong ung localtion ID 
            a = locate_list
            if maxlevel == QUARTER_LEVEL:       ## please note if data records very large
                b = self.QuarterGet(a[0]["province_id"],a[0]["district_id"],\
                    a[0]["ward_id"],a[0]["quarter_id"]) ## Return only one quater
                c = self.WardGet(a[0]["province_id"],a[0]["district_id"],a[0]["ward_id"],field="name")       ## Return only one ward
                d = self.DistrictGet(a[0]["province_id"],a[0]["district_id"],field="name")                              ## Return only one district
                e = self.ProvinceGet(a[0]["province_id"],field="name")                                                          ## Return only one TP
                if len(b) == 1: 
                    tmp_out["name"] = "{},{},{},{}".format(b[0]["name"], c[0], d[0],e[0])
                    tmp_out["location_id"] = self.LocationIDSearch(quarter_id=b[0]["quarter_id"],\
                                            ward_id=b[0]["ward_id"],district_id=b[0]["district_id"],\
                                            province_id=b[0]["province_id"],\
                                            maxlevel = QUARTER_LEVEL,\
                                            field="location_id")
                    if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                    else: tmp_out["location_id"] = "none"
                    out.append(dict(tmp_out))       
                else:
                    if self.debug: 
                        print ("len(e) not value 1", len(e))
                        print ("debug = {}-{}-{}-{}".format(e,d,c,b))
                        print ("len debug = {}-{}-{}-{}".format(len(e),len(d),len(c),len(b)))
                return out
            
            ## Tim cap phuong (1 phuong nhieu khu pho)
            elif maxlevel == WARD_LEVEL:
                b = self.QuarterGet(a[0]["province_id"],a[0]["district_id"],\
                    a[0]["ward_id"],quarter_id="all") ## Return only one quater
                c = self.WardGet(a[0]["province_id"],a[0]["district_id"],a[0]["ward_id"],field="name")       ## Return only one ward
                d = self.DistrictGet(a[0]["province_id"],a[0]["district_id"],field="name")                              ## Return only one district
                e = self.ProvinceGet(a[0]["province_id"],field="name")                                                          ## Return only one TP
                ## neu co khu pho
                if len(b) >= 1: 
                    for each in b:
                        tmp_out["name"] = "{},{},{},{}".format(each["name"], c[0], d[0],e[0])
                        tmp_out["location_id"] = self.LocationIDSearch(quarter_id=each["quarter_id"],\
                                            ward_id=each["ward_id"],district_id=each["district_id"],\
                                            province_id=each["province_id"],\
                                            maxlevel=WARD_LEVEL,field="location_id")
                        if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                        else: tmp_out["location_id"] = "none"                      
                        out.append(dict(tmp_out))     
                        ##[{'name': 'khu phố 1,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'},
                        # {'name': 'khu phố 2,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}]  
                else:  ## Hien thi phuong vi khong co location id trong bang database 
                    c = self.WardGet(a[0]["province_id"],a[0]["district_id"],a[0]["ward_id"])
                    tmp_out["name"] = "{},{}".format(c[0]["name"],d[0],e[0])
                    tmp_out["location_id"] = self.LocationIDSearch(ward_id=c["ward_id"],\
                                                district_id=c["district_id"],maxlevel = WARD_LEVEL,\
                                                province_id=c["province_id"],field="location_id")
                    if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                    else: tmp_out["location_id"] = "none"
                    out.append(dict(tmp_out))  
                    ##Bug : phai doc them id cua ward de lay locationid ---
                return out 

            ## Lay cap quan===========
            elif maxlevel == DISTRICT_LEVEL:
                e = self.ProvinceGet(a[0]["province_id"],field="name")                                                          ## Return only one TP
                d = self.DistrictGet(a[0]["province_id"],a[0]["district_id"],field="name")                              ## Return only one district
                c = self.WardGet(a[0]["province_id"],a[0]["district_id"],ward_id = "all")       ## Return only one ward                    
                if len(c) > 0:
                    for eachward in c:
                        b = self.QuarterGet(a[0]["province_id"],a[0]["district_id"],\
                            eachward["ward_id"],quarter_id="all") ## Return only one quater
                        if len(b)>0:
                            for eachquarter in  b:
                                tmp_out["name"] = "{},{},{},{}".format(eachquarter["name"], eachward["name"], d[0],e[0])   
                                tmp_out["location_id"] = self.LocationIDSearch(quarter_id=eachquarter["quarter_id"],\
                                            ward_id=eachquarter["ward_id"],district_id=eachquarter["district_id"],\
                                            province_id=eachquarter["province_id"],\
                                            maxlevel = QUARTER_LEVEL, field="location_id") 
                                if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]                               
                                else: tmp_out["location_id"] = "none"
                                out.append(dict(tmp_out))
                        # [{'name': 'khu phố 1,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                        # {'name': 'khu phố 2,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                        # {'name': 'khu phố 3,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                        # {'name': 'khu phố 4,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                        # {'name': 'Phường Tân Sơn Nhì,Quận Tân Phú,Thành Phố HCM'}, 
                        # {'name': 'Phường Sơn Kỳ,Quận Tân Phú,Thành Phố HCM'}]
                        else:  ## truong hop phuong khong co chua khu pho, hien thi phuong
                            tmp_out["name"] = "{},{},{}".format(eachward["name"], d[0],e[0])  
                            tmp_out["location_id"] = self.LocationIDSearch(ward_id=eachward["ward_id"],\
                                                district_id=eachward["district_id"],maxlevel = WARD_LEVEL,\
                                                province_id=eachward["province_id"],field="location_id")
                            if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                            else: tmp_out["location_id"] = "none"
                            out.append(dict(tmp_out))            
                
                else: ## only district and province
                    d = self.DistrictGet(a[0]["province_id"],a[0]["district_id"])
                    tmp_out["name"] = "{},{}".format(d[0]["name"],e[0])   
                    tmp_out["location_id"] = self.LocationIDSearch(
                            district_id=d[0]["district_id"],maxlevel = DISTRICT_LEVEL,\
                            province_id=d[0]["province_id"],field="location_id")
                    if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                    else: tmp_out["location_id"] = "none"
                    out.append(dict(tmp_out))                                             
                return out
            
            ## Lay cap thanh pho----> lay tat ca quan neu khong co phuong, khu pho
            elif maxlevel == PROVINCE_LEVEL:
                e = self.ProvinceGet(a[0]["province_id"],field="name")                      ## Return only one TP
                d = self.DistrictGet(a[0]["province_id"],district_id = "all")                    ## Return only one district
                if len(d)>0:
                    for eachdistrict in d:
                        c = self.WardGet(a[0]["province_id"],district_id=eachdistrict["district_id"],ward_id = "all")  
                        if len(c) > 0:
                            for eachward in c:
                                b = self.QuarterGet(a[0]["province_id"],eachdistrict["district_id"],\
                                    eachward["ward_id"],quarter_id="all") ## Return only one quater
                                if len(b)>0:
                                    for eachquarter in  b:
                                        tmp_out["name"] = "{},{},{},{}".format(eachquarter["name"], eachward["name"], eachdistrict["name"],e[0])   
                                        tmp_out["location_id"] = self.LocationIDSearch(district_id=eachquarter["district_id"],\
                                                maxlevel = QUARTER_LEVEL,\
                                                province_id=eachquarter["province_id"],\
                                                ward_id=eachquarter["ward_id"],\
                                                quarter_id=eachquarter["quarter_id"],\
                                                field="location_id")
                                        if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]   
                                        else: tmp_out["location_id"] = "none"                                         
                                        out.append(dict(tmp_out))
                                # [{'name': 'khu phố 1,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                # {'name': 'khu phố 2,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                # {'name': 'khu phố 3,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                # {'name': 'khu phố 4,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                # {'name': 'Phường Tân Sơn Nhì,Quận Tân Phú,Thành Phố HCM'}, 
                                # {'name': 'Phường Sơn Kỳ,Quận Tân Phú,Thành Phố HCM'}]
                                else:  ## truong hop phuong khong co chua khu pho, hien thi phuong
                                    tmp_out["name"] = "{},{},{}".format(eachward["name"], eachdistrict["name"],e[0]) 
                                    tmp_out["location_id"] = self.LocationIDSearch(ward_id=eachward["ward_id"],\
                                                district_id=eachward["district_id"],maxlevel = WARD_LEVEL,\
                                                province_id=eachward["province_id"],field="location_id")
                                    if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                                    else: tmp_out["location_id"] = "none"                                          
                                    out.append(dict(tmp_out))         
                        else: 
                            tmp_out["name"] = "{},{}".format(eachdistrict["name"],e[0])   
                            tmp_out["location_id"] = self.LocationIDSearch(
                                    district_id=d[0]["district_id"],maxlevel = DISTRICT_LEVEL,\
                                    province_id=d[0]["province_id"],field="location_id")
                            if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                            else: tmp_out["location_id"] = "none"
                            out.append(dict(tmp_out))                                                                                                 
                
                else: ## only return city
                    e = self.ProvinceGet(a[0]["province_id"])
                    tmp_out["name"] = "{}".format(e[0]["name"])   
                    tmp_out["location_id"] = self.LocationIDSearch(
                                    maxlevel = PROVINCE_LEVEL,\
                                    province_id=d[0]["province_id"],\
                                    field="location_id")
                    if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]
                    else: tmp_out["location_id"] = "none"
                    out.append(dict(tmp_out))                                
                return out        
            
            ### LEVEL lon nhat quoc gia + admin ======
            elif maxlevel <= NATION_LEVEL:
                ## lay toan bo province
                e = self.ProvinceGet(province_id="all")                                          ## Return only one TP
                for eachprovince in e:
                    d = self.DistrictGet(eachprovince["province_id"],district_id = "all")            ## Return only one district
                    if len(d)>0:
                        for eachdistrict in d:
                            c = self.WardGet(eachprovince["province_id"],district_id=eachdistrict["district_id"],ward_id = "all")  
                            if len(c) > 0:
                                for eachward in c:
                                    b = self.QuarterGet(eachprovince["province_id"],eachdistrict["district_id"],\
                                        eachward["ward_id"],quarter_id="all") ## Return only one quater
                                    if len(b)>0:
                                        for eachquarter in  b:
                                            tmp_out["name"] = "{},{},{},{}".format(eachquarter["name"], eachward["name"], eachdistrict["name"],eachprovince["name"])   
                                            tmp_out["location_id"] = self.LocationIDSearch(district_id=eachquarter["district_id"],\
                                                    maxlevel = QUARTER_LEVEL,\
                                                    province_id=eachquarter["province_id"],\
                                                    ward_id=eachquarter["ward_id"],quarter_id=eachquarter["quarter_id"],\
                                                    field="location_id")
                                            if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]   
                                            else: tmp_out["location_id"] = "none"                                                   
                                            out.append(dict(tmp_out))
                                    # [{'name': 'khu phố 1,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                    # {'name': 'khu phố 2,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                    # {'name': 'khu phố 3,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                    # {'name': 'khu phố 4,Phường Phú Thạnh,Quận Tân Phú,Thành Phố HCM'}, 
                                    # {'name': 'Phường Tân Sơn Nhì,Quận Tân Phú,Thành Phố HCM'}, 
                                    # {'name': 'Phường Sơn Kỳ,Quận Tân Phú,Thành Phố HCM'}]
                                    else:  ## truong hop phuong khong co chua khu pho, hien thi phuong
                                        tmp_out["name"] = "{},{},{}".format(eachward["name"],\
                                                                        eachdistrict["name"],eachprovince["name"])   
                                        tmp_out["location_id"] = self.LocationIDSearch(district_id=eachward["district_id"],\
                                                maxlevel = WARD_LEVEL,\
                                                province_id=eachward["province_id"],\
                                                ward_id=eachward["ward_id"],\
                                                field="location_id")
                                        if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]   
                                        else: tmp_out["location_id"] = "none"                                                                         
                                        out.append(dict(tmp_out))         
                            else:
                                tmp_out["name"] = "{},{}".format(eachdistrict["name"],eachprovince["name"])  
                                tmp_out["location_id"] = self.LocationIDSearch(district_id=eachdistrict["district_id"],\
                                                maxlevel = DISTRICT_LEVEL,\
                                                province_id=eachdistrict["province_id"],\
                                                field="location_id")
                                if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]   
                                else: tmp_out["location_id"] = "none"   
                                out.append(dict(tmp_out))                                                                                                 
                    
                    else: ## only return city
                        tmp_out["name"] = "{}".format(eachprovince["name"])  
                        tmp_out["location_id"] = self.LocationIDSearch(maxlevel = PROVINCE_LEVEL,\
                                                province_id=eachprovince["province_id"],\
                                                field="location_id")
                        if len(tmp_out["location_id"] ) ==1: tmp_out["location_id"] = tmp_out["location_id"][0]   
                        else: tmp_out["location_id"] = "none"  
                        out.append(dict(tmp_out))      
                return out      

    ## Lay chinh xac thong tin cua 1 location ID, khong lay vung quan ly ##
    def GetLocInfo(self, location_id):
        out = []
        tmp_out = {
            "name":""
        }
        if self.debug:
            print ("GetLocInfo is called\n")
        locate_list = self.LocationIDGet(location_id = location_id)
        if  len(locate_list) > 1: 
            if self.debug: print ("localtion_id have more than 1 in {}".format(self.locate_tbl))
            return out
        else: 
            maxlevel = locate_list[0]["maxlevel"]               ## Tim cap quan ly tuong ung localtion ID 
            a = locate_list
            b = self.QuarterGet(a[0]["province_id"],a[0]["district_id"],\
            a[0]["ward_id"],a[0]["quarter_id"],field="name") ## Return only one quater
            c = self.WardGet(a[0]["province_id"],a[0]["district_id"],a[0]["ward_id"],field="name")       ## Return only one ward
            d = self.DistrictGet(a[0]["province_id"],a[0]["district_id"],field="name")                              ## Return only one district
            e = self.ProvinceGet(a[0]["province_id"],field="name")                                                          ## Return only one TP                                    
            if maxlevel == QUARTER_LEVEL:               ## please note if data records very large
                if len(b) == 1:
                    tmp_out["name"] = "{},{},{},{}".format(b[0], c[0], d[0],e[0])
                    out.append(dict(tmp_out)) 
            elif maxlevel == WARD_LEVEL:               ## please note if data records very large
                if len(c) == 1:
                    tmp_out["name"] = "{},{},{}".format(c[0], d[0],e[0])
                    out.append(dict(tmp_out)) 
            elif maxlevel == DISTRICT_LEVEL:               ## please note if data records very large
                if len(d) == 1:
                    tmp_out["name"] = "{},{}".format( d[0],e[0])
                    out.append(dict(tmp_out))      
            
            ## Level quoc gia va admin va province vai tro nhu nhau, quoc gia gom nhieu province nhung khi lay 1 doi 
            ## tuong truc tiep thi chi co mot truong hop duy nhat 
            elif  maxlevel <= PROVINCE_LEVEL:               ## please note if data records very large     
                if len(e) == 1:
                    tmp_out["name"] = "{}".format(e[0])
                    out.append(dict(tmp_out))   
        return out        
    
    ## Add them khu vuc ==> Phan nay chua can, nap san demo cho khach hang la duoc=====
    def LocationAdd(self, type_of_request="none"):
        print ("Do not support")
        pass

## Doan chuong trinh test class
if TEST_CLASS:
    out_test = []
    province="79"
    district= "767"
    ward = "001"
    quarter = "001"

    # ## ======In thong tin =====
    print ("run test class name: locations")
    loc = LocationManager(debug = 1)
    # print ("============================")
    # out_test = loc.ProvinceGet("all")
    # print ("Get all province{}:{}".format(province,out_test))
    
    # print ("============================")
    # out_test = loc.ProvinceGet(province)
    # print ("Province get id {}:{}".format(province,out_test))
    
    # print ("============================")
    # out_test = loc.DistrictGet("79","767")
    # print ("DistrictGet get id {}:{}.{}".format(province, district, out_test) )
    
    # print ("============================")
    # out_test = loc.WardGet(province,district,ward)
    # print ("DistrictGet get id {}:{}:{}:{}".format(province, district,ward, out_test) )
    
    # print ("============================")
    # out_test = loc.QuarterGet(province,district,ward,quarter)
    # print ("DistrictGet get id {}:{}:{}:{}:{}".format(province, district,ward, quarter, out_test) )
    print (loc.LocationListManage(location_id="8479767001001"))
    print ("\n\n------------------------------------------------------------------")
    print (loc.GetLocInfo(location_id="8479767001001"))

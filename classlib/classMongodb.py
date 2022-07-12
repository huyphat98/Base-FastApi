import pymongo
import os
import json


class mongodb():
    match_list=[]
    host = "localhost"
    port = 27017
    dbname = ""

    ## Thong tin ket noi 
    def __init__(self,host="localhost", port=27017, dbname = "", debug = False):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.debug = debug
    
    ### Neu khong quan tam du lieu can lay 
    def all_query(self, collection):
        self.mycol = self.mydb[collection]

    def connect(self):
        self.myclient = pymongo.MongoClient(self.host,self.port)
        pass

    def closedb(self):
        self.myclient.close()
        pass
    
    ## Lay database
    def dbget(self):
        self.db = self.myclient[self.dbname]
        pass
    
    ## Tra ve toan bo collection trong database va close connect 
    def GetCollection(self,collection_name, condition ="none"):
        out = []
        try:
            self.connect()          ## Opendb
            self.dbget()            ## choose db 
            if condition in ["none", "null",0,"all"]:
                res = self. db[collection_name].find()
            else:
                res = self. db[collection_name].find(condition)
            for each in res:
                out.append(each) 
            self.closedb()       ##Closedb
        except Exception as e:
            if self.debug: print ("Debug: mongo fail: ", e)
            self.closedb()       ##Closedb
        return out

# db.Collection_name.distinct(
#     field : <string>,
#     query : <document>,
#     collation : <document> 
# )
    def GetCollectionDistinct(self,collection_name,condition ="none",field=""):
        out = []
        try:
            self.connect()          ## Opendb
            self.dbget()            ## choose db 
            if condition in ["none", "null",0,"all"]:
                res = self. db[collection_name].distinct(key=field)
            else:
                res = self. db[collection_name].distinct(query=condition,key=field) 
            for each in res:
                out.append(each)
            self.closedb()       ##Closedb
        except:
            self.closedb()       ##Closedb
        return out

    ## insert 1 du lieu ---------------
    def InsertOneCol(self,collection, data):
        try:
            self.connect()          ## Opendb
            self.dbget()            ## choose db         
            self. db[collection].insert_one(data)
            self.closedb()       ##Closedb
            return True
        except:
            return False

    ## insert nhieu du lieu-------------
    def InsertMultiCol(self,collection, data):
        try:
            self.connect()          ## Opendb
            self.dbget()            ## choose db         
            self. db[collection].insert_many(data)
            self.closedb()       ##Closedb
            return True
        except:
            self.closedb()       ##Closedb
            return False
    
    ## Count all document, return integer number
    def DocumentCount(self,collection, condition="all"): 
        count = 0
        try:
            self.connect()          ## Opendb
            self.dbget()            ## choose db   
            if condition in ["none","null","all"]:    
                count = self. db[collection].count_documents({})
            else: 
                count = self. db[collection].count_documents(condition)         ## sample: {"author": "Mike"}
            self.closedb()       ##Closedb         
        except:
            self.closedb()       ##Closedb
        return  count
    
    ## Remove document, return True or False
    def DocumentDelete(self,collection, condition): 
        try:
            self.connect()          ## Opendb
            self.dbget()            ## choose db         
            if condition == "all":
                self. db[collection].delete_many({})
            else:
                self. db[collection].delete_one(dict(condition))
            self.closedb()       ##Closedb
            return True
        except:
            self.closedb()       ##Closedb
            return False   
    
    ## Update document---
    def DocumentUpdate(self,collection, query, newdata={}) : 
        """
        Desc: update document with new value is newdata and with matching query
        Args:
            collection (_type_): name of collection
            query (_type_): must be dictionary
            newdata (dict, optional): must be dictionary. Defaults to {}.
        Returns:
            _type_: boolean
            _value_: True or False
        Example:
            query={"node_id":"123456"}
            newdata={"location_id":"8472694759"}
        """
        value2db ={"$set":newdata}
        try:
            self.connect()          ## Opendb
            self.dbget()             ## choose db         
            self. db[collection].update(query,value2db)
            self.closedb()          ##Closedb
            return True
        except:
            self.closedb()          ##Closedb
            return False          

    ## Remove all document in collection
    def DocumentDeleteAll(self,collection) :
        try:
            self.connect()          ## Opendb
            self.dbget()             ## choose db         
            self. db[collection].remove({})
            self.closedb()          ##Closedb
            return True
        except:
            self.closedb()          ##Closedb
            return False                  

    ## Huong dan cac ham 
    def help(self):
        print ("[1]. DocumentUpdate------------------------------")
        print (self.DocumentUpdate.__doc__)
        pass

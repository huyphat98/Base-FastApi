############################################################################
########            Truy van du lieu trong database
########            Create Date: 2021-12-18
############################################################################
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

HOST_DB = os.getenv('HOST_DB')
DB_NAME = os.getenv('DB_NAME')
############################################################################
########                Xu ly toan bo chuong trinh ket noi voi database
############################################################################
class mongodb():
    def __init__(self):
        self.myclient = pymongo.MongoClient(HOST_DB)
        self.mydb = self.myclient[DB_NAME]
    def col(self, collection):
        self.mycol = self.mydb[collection]
    def closedb(self):
        self.myclient.close()

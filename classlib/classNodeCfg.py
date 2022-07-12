import subprocess
import os
from classMongodb import mongodb
from datetime import datetime
import classCommon

DEBUG_CLASS = 0
HELP_CLASS = 0

## Gia tri mac dinh
default_node={
    "node_id":"none",
    "location_id":"none",
    "speaker": "off", 
    "stream_play": "stop",
    "stream_src":"null",
    "stream_name": "null",
    "lat": "10.780208387270775",
    "long": "106.62658445419603",
    "server_default": "171.244.236.208:2183",
    "server_mgt": "171.244.236.208:2183",
    "keep_alive": "60",
    "group_id": "1",
    "volume": "0",
    "serial":"none",
    "created_by":"noname", 
    "modify_time":"none"
}

class NodeCfg():
    db_name = "global"
    node_tbl = "tbl_nodes_cfg"
    debug = 0
    ## Init db_name
    def __init__(self, db_name="global", node_tbl="tbl_nodes_cfg", debug = 0):
        self.debug = debug
        self.db_name = str(db_name)
        self.node_tbl = str(node_tbl)
    
    ## Lay list mac dinh tat ca cac tham so, khi lay xong chi update lai cac tham so nao can dung 
    def DefaultConfigParam(self):
        return default_node

    ## List all node 4G ----
    def NodeList(self,location_id="none"):
        """
        Desc: get list of nodes in database
        Args:
            location_id (str, optional): _description_. Defaults to "none".
        Returns:
            _type_: list
            _values_: [] or multi elements
        """
        if location_id.lower() in ["none", "null"]: 
            return []
        mongo =  mongodb(dbname=self.db_name)
        ## Don't care location id 
        if location_id.lower() in ["all"]:
            data_query = "all"     ## Cau truc query command 
            return mongo.GetCollection(self.node_tbl,condition=data_query)
        ## Search node in location id 
        else: 
            data_query = {"location_id": str(location_id)}
            return mongo.GetCollection(self.node_tbl,condition=data_query)
    
    ## Total 4G node ---------
    def TotalofNode(self,location_id="none"):
        """
        Desc: Get total of node in database
        Args:
            location_id (str, optional): _description_. Defaults to "none".
        Returns:
            _type_: integer
            _value_: 0 or bigger
        Note:
            + If database not valid data, return 0
        """
        if location_id.lower() in ["none", "null"]: 
            return 0
        mongo =  mongodb(dbname=self.db_name)
        if location_id.lower() in ["all"]:  
            return mongo.DocumentCount(self.node_tbl)
        else: 
            data_query = {"location_id": str(location_id)}
            return mongo.DocumentCount(collection = self.node_tbl, condition = data_query)

    ## Add Node ---------key = localtionid and nodeid
    def AddOneNode(self, info_of_node):
        """
        Desc
            Add one node to database
        Args:
            info_of_node (list, optional): _description_. Defaults to [].
                    Please create variable using DefaultConfigParam, after that change 
                    variable (location_id, node_id from users )
        Returns:
            _type_: Boolean
            _value_: True or False
        """
        if not info_of_node:
           return False
        ## Check result 
        if info_of_node["location_id"] in ["none"] or  info_of_node["node_id"] in ["none"]:
            return False   
        ## Connect db
        mongo =  mongodb(dbname=self.db_name)
        
        ## Check Duplicated 
        allnode = mongo.GetCollection(self.node_tbl, condition ="none")
        for eachnode in allnode:
            if str(eachnode["node_id"]).lower() == str(info_of_node["node_id"]).lower() or\
                str(eachnode["serial"]).lower() == str(info_of_node["serial"]).lower():
                return False
        ## Add new node 4G 
        nowtime = classCommon.ParseNowTimeToStr()
        info_of_node["modify_time"] = nowtime       ## Update time by user 
        return mongo.InsertOneCol(self.node_tbl, info_of_node)
    
    ## Remove one node from databases
    def RemoveOneNode(self, node_id="none"):
        """
        Des:
            Remove one node with input node_id from user\n
        Args:
            node_id (str, optional): node_id value from user. Defaults to "none".
        Returns:
            _type_: Boolean 
            _value_: True or False
        """
        if node_id in ["none"]:
            return False        
        mongo =  mongodb(dbname=self.db_name)            
        query = {"node_id":str(node_id)}
        return mongo.DocumentDelete(self.node_tbl,query)
    
    ## Remove all node from databases
    def RemoveAllNode(self):
        """
        Desc:
            Remove all node in databases
        Returns:
            _type_: Boolean
            _value_: True or False
        """
        mongo =  mongodb(dbname=self.db_name)            
        query = "all"
        return mongo.DocumentDelete(self.node_tbl,query)    

    ## Thay doi thong tin Node
    def UpdateNodeInfo(self,node_id,info_update):
        mongo =  mongodb(dbname=self.db_name)            
        query ={"node_id":str(node_id)}
        info_update["modify_time"]= str(classCommon.ParseNowTimeToStr())
        return mongo.DocumentUpdate(self.node_tbl,query,info_update)    

    ## Print danh sach huong dan cac function trong class 
    def help(self):
        print ("[1]. RemoveAllNode------------------------------")
        print (self.RemoveAllNode.__doc__)
        print ("[2]. RemoveOneNode-----------------------------")
        print (self.RemoveOneNode.__doc__)
        print ("[3]. AddOneNode----------------------------------")
        print (self.AddOneNode.__doc__)  
        print ("[4]. TotalofNode----------------------------------")
        print (self.TotalofNode.__doc__)  
        print ("[5]. NodeList----------------------------------")
        print (self.NodeList.__doc__)  

## Debug class 
if DEBUG_CLASS:
    print("Debug class node ready")
    node = NodeCfg(debug=True)
    while True:
        type_from_user = input("Please node location: all or none or id: ")
        if type_from_user.strip() in ["all"]:
            print("Total node: ",node.TotalofNode(location_id="all"))
            print("Detail of nodes: ",node.NodeList(location_id="all"))
        elif len(type_from_user) > 3:
            print("Total node with ID {}:{}".format(type_from_user,\
                    node.TotalofNode(location_id=type_from_user.strip())))
            print("Detail of nodes {}:\n".format(type_from_user),\
                     node.NodeList(location_id=type_from_user.strip()))
        print ("Ready create random node 4G: ")
        node_id = "dsjdjsj80fkjfgkf"
        location_id = "8479767001001"
        serial = "dn7640969"
        createdbyuser = "admin"
        node_dict = node.DefaultConfigParam()
        node_dict["location_id"] = location_id
        node_dict["node_id"] = node_id
        node_dict["serial"] = serial
        node_dict["created_by"] = "admin"
        print ("Result add node: ",node.AddOneNode(dict(node_dict)))
        type_from_user = input("Type command d to remove node, or a to all or u to update ")
        if type_from_user.strip() == 'd':
            print ("result: ", node.RemoveOneNode(node_id=node_id))
        elif type_from_user.strip() == 'a':
            print ("result: ", node.RemoveAllNode())
        elif type_from_user.strip() == 'u':
            print ("Result of update node: ",\
                node.UpdateNodeInfo(node_id=node_id,info_update={"location_id":"1234567890", "speaker":"off"}))

if HELP_CLASS:
    print("Document for all function")
    node = NodeCfg()
    node.help()
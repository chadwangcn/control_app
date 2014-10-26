#coding=utf-8

import sqlite3


class dbEngine(object):
    '''
    data base Engine
    '''
    def __init__(self, _dbtype='file',_fileDbPath="./controllerghost.db"):
        '''
        Constructor
        '''
        self.fileDbPath = _fileDbPath
        self.dbtype = _dbtype   
        
    def InitEngine(self):
        try:
            if self.dbtype == 'mem':
                self.dbCx = sqlite3.connect(":memory:")    # create memory db for tmp data 
            else:
                self.dbCx = sqlite3.connect(self.fileDbPath) # create file db for config data
            
            # initial db Table
            dbSql = "CREATE TABLE \"main\".\"realtimedata\" (\"id\" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \"temperature_ch_0\" INTEGER NOT NULL,\"dsp\" INTEGER,\"data2\" INTEGER)"  
            if self.FindDbTable(self.dbFileCx,"realtimedata") == False:                
                self.ExcuteSql(dbSql)              
            
        except:
            pass
    
    def UInitEngine(self):
        pass   
   
        
    def FindDbTable(self,_tableName):
        try:
            dbSql = "select count(*)  from sqlite_master where type='table' and name=\'"+ _tableName+"\'"
            [status,content] = self.SearchSql(dbSql)     
            count = content[0][0]
            if count > 0 :
                return True
            else:
                return False
        except:
            return False
    
    def ExcuteSql(self,_tableSql):
        try:
            cu = self.dbCx.cursor()
            cu.execute(_tableSql)
            self.dbCx.commit()
            return True
        except:
            return False
    
    def SearchSql(self,_tableSql):
        try:
            cu = self.dbCx.cursor()
            cu.execute(_tableSql)
            content= cu.fetchall()
            return [True,content]
        except:
            return [False,None]
    
    def UpdateSql(self,_tableSql):
        try:
            self.SearchSql(_tableSql)
            self.ExcuteSql(_tableSql)
            return True
        except:
            return False
            
    
        
    
'''  
SOLUTION_DB_SQL_STRING = 
'CREATE TABLE "main"."Solution" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "author" TEXT NOT NULL DEFAULT ('admin'),
    "create_time" TEXT NOT NULL,
    "modify_time" TEXT NOT NULL,
    "control_type" TEXT NOT NULL,
    "control_data_id" INTEGER NOT NULL,
    "detect_type" TEXT NOT NULL
);

CREATE TABLE "main"."RealTimeData" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "temperature_ch_0" INTEGER NOT NULL,
    "dsp" INTEGER,
    "data2" INTEGER
);

insert into realtimedata (temperature_ch_0,dsp,data2) values(1,2,3)

select * from realtimedata where id =2 

'''
    
    
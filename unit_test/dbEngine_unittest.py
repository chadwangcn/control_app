'''
Created on May 25, 2014

@author: root
'''
import unittest
from   engine.dbEngine import *
import sqlite3


class Test(unittest.TestCase):


    def setUp(self):
        self.dbObject = dbEngine.dbEngine()
        self.dbObject.InitEngine()
      
        pass


    def tearDown(self):
        self.dbObject.UInitEngine()
        pass


    def testUsage(self):
        print("Usage")
        pass
    
    def testMemDbCase(self):
        print("testMemDbCase")
        pass
    
    def testFileDbCase(self):
        print("testFileDbCase")
        INPUT_MSG = "realtimedata"
        if self.dbObject.FindDbTable(INPUT_MSG):
            print("find table:"+ INPUT_MSG)
        return False
    
    def testTableAddAndDel(self):
        #check table
        print("=============>")
        tableName = "NewYork"
        if self.dbObject.FindDbTable(tableName):
            print(tableName+" Find")
        else:
            print(tableName+" Not Find")
            
        dbSql = "CREATE TABLE \"main\".\""+tableName+ "\" (\"id\" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \"temperature_ch_0\" INTEGER NOT NULL,\"dsp\" INTEGER,\"data2\" INTEGER)"  
        self.dbObject.ExcuteSql(dbSql)  
        
        if self.dbObject.FindDbTable(tableName):
            print(tableName+" Find")
        else:
            print(tableName+" Not Find")
        
        print("<=============")
        
    def testTableAddNewYork(self):
        #check table
        print("=============>")
        tableName = "NewYork"
        if self.dbObject.FindDbTable(tableName):
            print(tableName+" Find")
        else:
            print(tableName+" Not Find")
            
        dbSql = "CREATE TABLE \"main\".\""+tableName+ "\" (\"id\" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \"temperature_ch_0\" INTEGER NOT NULL,\"dsp\" INTEGER,\"data2\" INTEGER)"  
        self.dbObject.ExcuteSql(dbSql)  
        
        if self.dbObject.FindDbTable(tableName):
            print(tableName+" Find")
        else:
            print(tableName+" Not Find")
        
        print("<=============")
        
    def testInsertData(self):
        tableName = "NewYork"
        i = 1
        dbSql = "insert into "  + tableName + " (temperature_ch_0,dsp,data2) values(" + str(i)+","+str(i+1)+","+str(i+2)+")"
        if self.dbObject.ExcuteSql(dbSql):
            print(dbSql + " OK")
        else:
            print(dbSql + " Fail")
              
        
        i = 4
        dbSql = "insert into "  + tableName + " (temperature_ch_0,dsp,data2) values(" + str(i)+","+str(i+1)+","+str(i+2)+")"
        if self.dbObject.ExcuteSql(dbSql):
            print(dbSql + " OK")
        else:
            print(dbSql + " Fail")
        
        i = 8
        dbSql = "insert into "  + tableName + " (temperature_ch_0,dsp,data2) values(" + str(i)+","+str(i+1)+","+str(i+2)+")"
        if self.dbObject.ExcuteSql(dbSql):
            print(dbSql + " OK")
        else:
            print(dbSql + " Fail")
        
    def testDumpData(self):
        tableName = "NewYork"
        dbSql = "select * from "+tableName 
        [status,content] = self.dbObject.SearchSql(dbSql)
        if status:
            print "Dump Info"
            print content
        else:
            print "No Data"
    
  
        
            
 
        
        
    
    def testTableDelNewYork(self):
        #check table
        pass
            
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
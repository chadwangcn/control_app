#-*- coding:utf-8 -*-
import unittest
from engine.RecorderCenter import *
from engine.DataCenter import *
from engine.UdpMonitor import  *
from engine.UartMonitor import *
from engine.cvs_parse import *
import time
from UdpMonitor import  *
from  cvs_parse import *

'''
def DataReceive(data):
    print(data)
    
def Subcriber(data):
    pass
    #print(""+data)
    

class DataEngine(object):
    def EngineSubcribe(self,data):
        print(data)

class Test(unittest.TestCase):
    def setUp(self):
        self.DataCenterObject = DataCenter.DataCenter("")
       
        
    def tearDown(self):
        pass
    
    def testUartMonitor(self):
        return;
        self.DataCenterObject = DataCenter.DataCenter("")
        object_uart =UartMonitor.UartMonitor("/dev/ttyUSB0",115200)        
        self.DataCenterObject.Register("UartMonitor", object_uart)           
        print"start ===============> "
        self.DataCenterObject.Subcribe("UartMonitor", "No.1", Subcriber)
        
        ' record the source data'
        RecObject= RecorderCenter.RecorderCenter("/home/lijun/ts/tmp","Uart",1024*1024)
        self.DataCenterObject.Subcribe("UartMonitor", "No.3", RecObject.fillData)
        
        self.DataCenterObject.Start()
        time.sleep(1) 
    
    def testDataEngine(self):       
        return;      
        self.DataCenterObject = DataCenter.DataCenter("")
       
        object2 = DataEngine()
        self.DataCenterObject.Subcribe("UartMonitor", "No.2", object2.EngineSubcribe)
             
        self.DataCenterObject.Start()
        
    def testCvsDataPipeLine(self):        
        self.DataCenterObject = DataCenter.DataCenter("")      
        object_src = UdpMonitor(21563,"127.0.0.1")        
        self.DataCenterObject.Register("UDP", object_src)  
        
        cvs = cvs_comsumer() 
        self.DataCenterObject.Subcribe("UDP", "cvs_read", cvs.stream_buffer)             
        self.DataCenterObject.Start()
        while True:
            time.sleep(30)  
        print "Cvs Data PipeLine end"
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    '''
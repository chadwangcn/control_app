'''
Created on Aug 4, 2014

@author: lijun
'''
import unittest
import threading
import time
from socket import *
from engine import *
from engine.DataCenter import *
from engine.LogAdapter import *
from data_source.UdpMonitor import *


class udp_send(threading.Thread):
    def __init__(self,_strIP,_nPort):
        self.bExit = False        
        self.threadid= 0  
        self.nPort = _nPort
        self.strIP = _strIP      
        threading.Thread.__init__(self)     
        
    def  run(self):        
        while self.bExit == False:            
            self.SendData(" haha  this is a nice tes t")   
            time.sleep(2)
   
        
    def start_send(self):
        self.start()     
        self.bExit = False   
        
    def stop_send(self):        
        self.bExit = True
    
    def reTryConnectUdp(self):
        try:            
            self.udpsocket = socket(AF_INET, SOCK_DGRAM)  
            self.address = (self.strIP,self.nPort)
            'self.udpsocket.bind(self.address)'  
            self.net_status = True          
                   
        except Exception,e:
            self.net_status = False
            print e             
               
        
    def SendData(self,_data):
        error = False
        try:
            self.udpsocket.sendto( _data  ,self.address)            
        except Exception,e:
            print e
            error = True           
           
        if error == True:
            self.net_status = False
            self.reTryConnectUdp()

def test( _data):
    print "==>"+_data
    
class Test(unittest.TestCase):


    def setUp(self):
        self.udpsender = udp_send("127.0.0.1",45232)
        self.udpsender.start_send()    
        
        
    def tearDown(self):
        self.udpsender.stop_send()
        
    def testDataCenter(self):
        self.DataCenterObject = DataCenter.DataCenter()  
        object_src = UdpMonitor(3000,"192.168.11.5")        
        self.DataCenterObject.Register("UDP", object_src)   
        
        
        self.DataCenterObject.Subcribe("UDP", "test", test)          
           
        self.DataCenterObject.Start()
        while True:
            time.sleep(60)  
            

        
       
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
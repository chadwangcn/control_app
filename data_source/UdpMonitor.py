'''
Created on May 25, 2014

@author: lijun
'''
import traceback
from engine import *
import time
from socket import *


class UdpMonitor(DataCenter.BaseDataSource):
    '''
    UdpMonitor: listen on udp port
    '''


    def __init__(self, _nPort,_strIP,):
        '''
        Constructor
        '''
        DataCenter.BaseDataSource.__init__(self)
        self.nPort = _nPort
        self.strIP = _strIP
        'LogAdapter.LogPrint("DEBUG",self.__class__.__name__, self.strIP +":" + str(self.nPort)) '      
        self.retryCnt = 0;
        self.net_status = False
        
    def reTryListenUdp(self):
        try:            
            self.udpsocket = socket(AF_INET, SOCK_DGRAM)  
            self.address = (self.strIP,self.nPort)
            self.udpsocket.bind(self.address)  
            self.net_status = True          
            return True           
        except Exception,e:
            self.net_status = False
            print Exception,":",e
            traceback.print_exc() 
            'LogAdapter.LogPrint("DEBUG",self.__class__.__name__, self.strIP +":" + str(self.nPort)+" reTryListenUdp error")'       
            return False           
        
        
    def startDataSource(self):
        self.reTryListenUdp()
    
    def stopDataSource(self):
        try:
            self.udpsocket.close() 
            self.net_status = False          
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            'LogAdapter.LogPrint("DEBUG",self.__class__.__name__, self.strIP +":" + str(self.nPort)+" stopDataSource") '      
           
     
    
    def GetData(self):  
        error = False        
        while True:  
            try:                
                if(  self.net_status ):                
                    data,address =self.udpsocket.recvfrom(2048)
                    self.retryCnt = 0
                    error = False            
                    return [True,data]
                else:
                    error = True
            except Exception,e:
                print Exception,":",e
                traceback.print_exc()  
                error = True
                'LogAdapter.LogPrint("DEBUG",self.__class__.__name__, self.strIP +":" + str(self.nPort)+" GetDataError") '      
           
                
            if error == True:
                self.retryCnt = self.retryCnt + 1
                self.stopDataSource() 
                self.reTryListenUdp()
                sleep_sec = self.retryCnt*5
                if sleep_sec > 50:
                    sleep_sec  = 50
                
                if sleep_sec <= 0:
                    sleep_sec = 3  
                
                time.sleep(sleep_sec)
                'LogAdapter.LogPrint("DEBUG",self.__class__.__name__, self.strIP +":" + str(self.nPort)+" GetDataError ReTryConnect:"+str(self.retryCnt)) '      
           
            return [False,""]
                
          
     
    
    
    
        
        
        
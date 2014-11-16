#coding=utf-8
import traceback
import DataCenter
import time
from socket import *

class UdpSender(object):
    '''
    UDP SENDER
    '''

    def __init__(self, _nPort,_strIP,):
        '''
        Constructor
        '''
        self.nPort = _nPort
        self.strIP = _strIP             
        self.retryCnt = 0;
        self.net_status = False
        
    def reTryBindUdp(self):
        try:            
            self.udpsocket = socket(AF_INET, SOCK_DGRAM)  
            self.address = (self.strIP,self.nPort)
            self.net_status = True          
            return True           
        except Exception,e:
            self.net_status = False
            print Exception,":",e
            traceback.print_exc()  
            return False   
        
    def start_network(self):
        self.reTryBindUdp()
    
    def stop_network(self):
        try:
            self.udpsocket.close() 
            self.net_status = False          
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
           
    def SendData(self,_data):
        error = False
        try:
            'print "-->"+ _data '           
            self.udpsocket.sendto( _data  ,self.address)  
            self.net_status = True                 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            error = True
            
        if error == True:
            self.net_status = False
            self.reTryBindUdp()
            
    def write(self,_data):
        self.SendData(_data)
        
    def flush(self):
        pass
            
            
            
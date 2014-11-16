'''
Created on Apr 22, 2014

@author: ljwang
'''
import os  
import stat  
import time
import logging
import logging.handlers
from engine import UdpSender

class LogTrace():    
    def __init__(self,_default_level=logging.DEBUG):
        '''
        Constructor
        ''' 
        self.bDebug = True
        
        if self.bDebug == True:
            return 
      
        self.log_level = _default_level 
        self.logtrace = logging.getLogger("EngineUI") 
        
        'self.udp_send = UdpSender.UdpSender(1400,"127.0.0.1")'
        self.udp_send = UdpSender.UdpSender(1400,"0.0.0.0")
        self.udp_send.start_network()
    
        handler=logging.StreamHandler(self.udp_send)
        self.logtrace.addHandler(handler)
        self.logtrace.setLevel(self.log_level)  
        
        
    def info(self,_tag,_info):  
        if self.bDebug == True:
            print _info
            return   
            
        self.logtrace.info(_info )
        
    def debug(self,_tag,_info):
        if self.bDebug == True:
            print _info
            return  
        self.logtrace.debug(_info )
        
    def warning(self,_tag,_info):
        if self.bDebug == True:
            print _info
            return   
        self.logtrace.warning(_info )
        
    def error(self,_tag,_info):
        if self.bDebug == True:
            print _info
            return   
        self.logtrace.error(_info )
    
    def critical(self,_tag,_info):
        if self.bDebug == True:
            print _info
            return   
        self.logtrace.critical(_info )
        
  
        
        
        
 


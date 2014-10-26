#coding=utf-8

import time
class PacketFactory(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Packet Define
        '''        
        pass
    
    def BuildHeartBeat(self):
        '''
        format  the packet
        '''   
          
        return "Tick:" + hex( int(time.strftime( '%m%d%H%M%S',time.localtime(time.time())) ) )[2:]
        
    
    def BuildModeSwitch(self,_value):
        return "Mode:"+hex(_value)[2:]
    
    def BuildSolenoidCtr(self,_value):
        return "Valve:"+ hex(_value)[2:]
    
    def BuildSegmentDataCfg(self, _data):
        pass
    
    def BuildAssistBoxData(self,_data):
        pass
    
    def BuildMainCtrl(self,_data):
        pass
    
    def BuildAssistBoxOutput(self,_data):
        pass
    
    def BuildDoorCtrl(self,_data):
        pass
    
    def BuildFIDCtrl(self,_data):
        pass
    
    def BuildTCDCtrl(self,_data):
        pass
   
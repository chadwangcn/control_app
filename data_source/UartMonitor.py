from engine import *
import serial
import time

class UartMonitor(DataCenter.BaseDataSource):
    '''
    UartMonitor
    '''
    def __init__(self,_port,_bautrate):
        '''
        Constructor
        ''' 
        DataCenter.BaseDataSource.__init__(self)
        self.port = _port
        self.bautrate = _bautrate
        self.bRun = True     
        self.uartObject = None   
        'LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate))'
        
    def startDataSource(self):
        try:
            self.uartObject = serial.Serial(self.port, self.bautrate)
            self.uartObject.close()
            self.uartObject.open()
            if self.uartObject.isOpen():
                'LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate)+" Opened")'
                return True     
            else:
                'LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate)+" Opened error")'
                return False  
                       
        except:
            ' LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate)+" Opened error exception")'
            return False
      
    
    def stopDataSource(self):
        try:
            if self.uartObject.isOpen():
                self.uartObject.close()
                'LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate)+ " Closed")'
            return True            
        except:
            return False
          
    
    def GetData(self):           
        try:
            Msg = "Port"+ self.port + " bauterate="+str(self.bautrate)
            if self.uartObject.isOpen():
                content = self.uartObject.readline()   
                if content:
                    return [True,content]
                else:
                    return [False,"error"]          
            else:
                'LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate)+ "error:"+"Uart not open")'
                return [False,"Uart Port Not Open:" + Msg ]            
        except:
            'LogAdapter.LogPrint("DEBUG","uart","port="+self.port + " bauterate="+str(self.bautrate)+ " read Error")'
            return [False,"Read Error:"+ Msg]
        
          
    
    
        
    
    
        
        
        
        
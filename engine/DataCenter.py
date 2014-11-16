#coding=utf-8

import threading
import time
import traceback

def cvs_parse( _msg ):
    value_status = False
    try:
        new_data = dict()       
        items = _msg.split(',')
        for item in items:
            item_params = item.split(':')
            key = item_params[0]
            value = item_params[-1]
            new_data[key] = int(value,16)
        value_status = True
    except Exception,e:
            print Exception,":",e
            traceback.print_exc()
            value_status = False
    
    if value_status == True:        
        return [True,new_data]        
    else:       
        return [False,None]    

class Queue(object) :
    def __init__(self) :
        self.queue = []
    
    def enqueue(self, item) :
        self.queue.append(item)
        
    def dequeue(self) :
        if self.queue != [] :
            return self.queue.pop(0)
        else :
            return None
            
    def head(self) :
        if self.queue != [] :
            return self.queue[0]
        else :
            return None
    
    def tail(self) :
        if self.queue != [] :
            return self.queue[-1]
        else :
            return None
    
    def length(self) :
        return len(self.queue)
        
    def isempty(self) :
        return self.queue == []
    
    
class DataCenter(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.statemachine = "idle"
        self.DataSourceLst = {}
        self.rwlock = threading.RLock() #
        pass
    
    def Register(self,_sourceName,_object):
        '''
        register source module to data center
        source module will provider data source
        '''
        ret =True
        error_info = ""
        self.rwlock.acquire()
        if self.DataSourceLst.has_key(_sourceName):
            ret = "error"
            error_info = "dataSource exist"            
        else:
            self.DataSourceLst[_sourceName] = _object 
        self.rwlock.release()    
        return [ret,error_info] 
    
    def UnRegister(self,_sourceName):
        '''
        unregister source module to data center
        source module will provider data source
        '''
        ret =True
        error_info = ""
        self.rwlock.acquire()
        if self.DataSourceLst.has_key(_sourceName):
            try:
                del self.DataSourceLst[_sourceName]                
            except:
                ret = "error"
                error_info = "del error"                  
        else:
            ret = "error"
            error_info = "dataSource not exist"             
        self.rwlock.release()    
        return [ret,error_info]        
 
    
    def Subcribe(self,_sourceName,_subcriberOwner,_callBackFunc):
        '''
        any module can subcribe the data,subcribe will
        return a subcribe id
        '''
        ret =True
        error_info = ""
        self.rwlock.acquire()
        
        if self.DataSourceLst.has_key(_sourceName):
            try:
                self.DataSourceLst[_sourceName].Subcribe(_subcriberOwner,_callBackFunc)               
            except:
                ret = "error"
                error_info = "Subcribe error"                
        else:
            ret = "error"
            error_info = "dataSource not exist"          
            
        self.rwlock.release()  
        return [ret,error_info]    
            
        
    
    def UnSubcribe(self,_sourceName,_subcriberOwner):
        '''
        use subcribe id to delete the subcribe
        '''
        ret =True
        error_info = ""
        self.rwlock.acquire()
        
        if self.DataSourceLst.has_key(_sourceName):
            try:
                self.DataSourceLst[_sourceName].UnSubcribe(_subcriberOwner)                           
            except:
                ret = "error"
                error_info = "UnSubcribe error"      
                return ["error","UnSubcribe error"]
        else:
            ret = "error"
            error_info = "dataSource not exist"   
        
        self.rwlock.release()  
        return [ret,error_info]    
            
        
    
    def Start(self):
        self.statemachine = "run"
        
        self.rwlock.acquire()
        for k in self.DataSourceLst.keys():            
            self.DataSourceLst[k].StartDataCollect()
        self.rwlock.release()
        
    
    def Stop(self):
        self.statemachine = "stop"
        self.rwlock.acquire()
        for k in self.DataSourceLst.keys():            
            self.DataSourceLst[k].StopDataCollect()
        self.rwlock.release()   
  
        
    def DumpMap(self):
        print("=============================>")
        for k in self.DataSourceLst.keys():
            print("key="+k+"++++++++++")
            #self.DataSourceLst[k]("test dump data")            
        print("<=============================")
        
        
class BaseDataConsume(threading.Thread):
    '''
    
    '''
    def __init__(self):
        self.bExit = False
        self.Queue = Queue()
        self.threadid= 0        
        threading.Thread.__init__(self)          
        self.rwlock = threading.RLock() #
        pass
    
    def StartBase(self):
        self.bExit = False
        self.start()
        
    
    def StopBase(self):
        self.bExit = True
        self.Stop()
        
    
    
    def  run(self):
        '''
          lock the data queue
          pop the data    
          unlock the data queue       
          process the data
        '''
        while self.bExit == False:  
            
            try:
                bLoop = False
                self.rwlock.acquire()
                if self.Queue.isempty() == True:
                    'sleep 10 ms' 
                    time.sleep(0.01) 
                    bLoop = True  
                    
                if bLoop == True:
                    self.rwlock.release()   
                    continue                  
                    
                
                _data = self.Queue.dequeue()  
                self.rwlock.release()   
                              
                self.Process(_data)
            except Exception,e:
                print e   
                         
                   
      
    def _data_callback(self, _udpData):
                    
        self.rwlock.acquire()
        
        try:            
            self.Queue.enqueue( _udpData)
            pass
        except Exception,e:
            print e   
        self.rwlock.release()
        
    
    def Process(self,_data):
        '''
        will Process the data
        '''
        
        
        
        
        pass 
        
class BaseDataSource(threading.Thread):
    '''
    '''
    def __init__(self):
        self.threadid= 0
        self.statemachine = "idle" 
        threading.Thread.__init__(self)  
        self.SubcriberLst = {}
        self.rwlock = threading.RLock() #
 
    
    def GetData(self):
        '''
        abstract function: child class should implement this function 
        '''
        pass
    
    def Subcribe(self,_subcriberOwner,_callBackFunc):
        '''
        any module can subcribe the data,subcribe will
        return a subcribe id
        '''
        ret = True
        self.rwlock.acquire()
        if self.SubcriberLst.has_key(_subcriberOwner):
            ret = False
        else:
            self.SubcriberLst[_subcriberOwner] = _callBackFunc;
            ret = True
        self.rwlock.release()
        return ret
    
    def UnSubcribe(self,_subcriberOwner):
        '''
        use subcribe id to delete the subcribe
        '''
        ret = True
        self.rwlock.acquire()
        if self.SubcriberLst.has_key(_subcriberOwner):
            del self.SubcriberLst[_subcriberOwner]
        else:
            ret= False;
        self.rwlock.release()
        return ret
      
    def StartDataCollect(self):
        if self.statemachine != "run":
            self.statemachine = "run" 
            self.startDataSource()
            self.start()
        
    
    def StopDataCollect(self):
        self.statemachine = "stop"
        self.stopDataSource()
        self.stop() 
        pass
    
    def startDataSource(self):
        '''
        abstract function: child class should implement this function 
        '''
        pass
    
    def stoptDataSource(self):
        '''
        abstract function: child class should implement this function 
        '''
        pass
    
    def OnCollect(self):
        if self.statemachine != "run":
            return False        
        try:
            [status,data] = self.GetData()          
            if status == True:
                try:
                    self.rwlock.acquire()
                    for k in self.SubcriberLst.keys():
                        self.SubcriberLst[k](data)
                    self.rwlock.release()
                except Exception,e:
                    print Exception,":",e
                    traceback.print_exc() 
                    self.rwlock.release()                          
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            return False           
        
    
    def run(self):
        while self.statemachine == "run":
            self.OnCollect()
        
        
    
       
    
    
    
    
 
    
    
    
    
    
        
#coding=utf-8

import threading
import time
import traceback
from engine import DataCenter
from engine import db_data

class event(object):
    def __init__(self):
        self.expect_value = None
        self.name = None
        self.status = "unkonw"
        self.key_words = None
        self.start_time = None
        self.timeout = 100
    

class async_event(threading.Thread):
    '''
    async_event
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.bExit = False
        self.event_repo = {}
        threading.Thread.__init__(self)          
        self.rwlock = threading.RLock() #
    
    def start_async(self):
        self.start()
    
    def stop_async(self):
        self.bExit = True
        
        
    def add_event(self, _event):
        self.rwlock.acquire()
        try:
            _event.start_time = time.time()
            self.event_repo[_event.name] = _event
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
        self.rwlock.release()
    
    def del_event(self,_event):
        self.rwlock.acquire()
        try:            
            self.event_repo.pop(_event.name)            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
        self.rwlock.release()
        
    def string_cmp(self,_src,_dst):
        try:
            _src = _src.strip().lstrip().rstrip('\n')       
            _dst = _dst.strip().lstrip().rstrip('\n')          
          
            if _src == _dst:               
                return True
            else:               
                return False                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
        return False
      
        
        return True
        
    def update_event(self,_data):     
        self.rwlock.acquire()   
        try:
            [ret, key_value] = DataCenter.cvs_parse(_data)
            if False == ret:
                self.rwlock.release()  
                return
            
            value_db = db_data.db_data()
            value_db.update_value_dict(key_value)
            
            for key,item in self.event_repo.iteritems():
                  
                if _data.find(item.key_words) != -1 :                    
                    if self.string_cmp(_data,item.expect_value):                
                        item.status = "ok"
                        self.update_event_repo(item)
                        continue
                
                [ret,value] = value_db.get_key( item.key_words )  
                if ret == True and item.key_words == "Crc" and None != value:
                    if str( hex(value)[2:])  == item.expect_value:     
                        item.status = "ok"
                        self.update_event_repo(item)
                        print "crc check ok"
                    else:
                        print "crc error,expect:"+ str(item.expect_value) + " raw_value:" + str( hex(value)[2:])
                        continue
                    
                if ret == True and value == item.expect_value :
                    item.status = "ok"
                    self.update_event_repo(item)
                    continue
                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
        self.rwlock.release()    
        
    def update_event_repo(self,_event):
        try:            
            self.event_repo[_event.name] = _event            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()

        
    def get_event_status(self, _event_name):  
        self.rwlock.acquire()      
        try:            
            _event = self.event_repo[_event_name]            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
        self.rwlock.release()
        return _event.status
        
    
    def run(self):
        while self.bExit == False:  
            self.rwlock.acquire()
            try:
                for key, item in self.event_repo.iteritems():
                    if self.bExit == True:
                        break
                    delta = time.time() - item.start_time                     
                    if  delta > item.timeout and item.status == "unkonw":
                        'item.status = "timeout"'
                        continue             
            except Exception,e:
                print Exception,":",e
                traceback.print_exc()
            self.rwlock.release()
            '  100ms '
        

    
    
    
    
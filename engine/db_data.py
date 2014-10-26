#coding=utf-8

from engine import cfg_data
import traceback
import threading


class db_data(object):
    '''
    
    '''
    def __init__(self):
        self.value_table = { }
        self.rwlock = threading.RLock() 
        
        
    def update_value_dict(self,key_value):
        try:
            self.rwlock.acquire()
            for (key,value) in key_value.items():                
                self.update_value_one(key, value)
            self.rwlock.release()
        except Exception,e:
            self.rwlock.release()
            print Exception,":",e
            traceback.print_exc()
            
        
       
                
    def update_value_one(self, key,value):
        try:
            self.value_table[key] = value             
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
           
            
    def get_key(self,key):
        try:
            self.rwlock.acquire()
            value = self.value_table.get(key)
            self.rwlock.release()
            return [True,value]           
        except Exception,e:
            self.rwlock.release()
            print Exception,":",e
            traceback.print_exc()
            return [False,None]
        
 
        
       
        
   
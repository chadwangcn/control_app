#coding=utf-8

import traceback
import threading
import time

'''
self.Init          =  0x00000000
self.Factory       =  0x00000100
self.Auto_Config   =  0x00000201
self.Auto_Ready    =  0x00000202    
self.Auto_Running  =  0x00000205
self.Auto_End      =  0x00000206
        '''
        
        
class St_Engine():
    
    def __init__(self):
        self.st_cur = "UnKnow"
        self.st_last = "UnKnow"
        self.st_remote = "UnKnow"
        
        self.process_table = {"UnKnow":None,"Init_Err":None,    "Init_OK":None,      "Factory":None,      
                              "Auto_Config":None, "Auto_Ready":None,   "Auto_Warmming":None,
                              "Auto_WarmUp":None, "Auto_Running":None, "Auto_End":None  }
        
        self.value_table = {  "Init_Err":0x00000000,    "Init_OK":0x00000001,      "Factory":0x00000100,      
                              "Auto_Config":0x00000201, "Auto_Ready":0x00000202,   "Auto_Warmming":0x00000203,
                              "Auto_WarmUp":0x00000204, "Auto_Running":0x00000205, "Auto_End":0x00000206  }
        
        self.str_table = {  0x00000000:"Init_Err",    0x00000001:"Init_OK",      0x00000100:"Factory",      
                            0x00000201:"Auto_Config", 0x00000202:"Auto_Ready",   0x00000203:"Auto_Warmming",
                            0x00000204:"Auto_WarmUp", 0x00000205:"Auto_Running", 0x00000206:"Auto_End"        }
        
        self.rwlock = threading.RLock() 
    
    def check_state_value(self, state_value):
        ret_value = False
        try:
            state_handle = self.process_table.get(state_value)
            if state_handle != None:
                ret_value = True    
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
            ret_value = False
                    
        return ret_value
        
    def st_strtovalue(self,str_value):
        try:
            num_value = self.value_table.get(str_value)           
            if num_value == None:
                return [False,None]
            else:
                return [True,num_value]
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
            return [False,None]        
    
    def st_valuetostr(self,value):
        try:           
            str_value = self.str_table.get(value)           
            if str_value == None:
                return [False,None]
            else:
                return [True,str_value]
        except Exception,e:
            print Exception,":",e
            return [False,None]     
        
    def change_state(self, new_state):
        if False == self.check_state_value(new_state):
            return False
        
        self.rwlock.acquire()
        self.before_transition(new_state)
        self.st_last = self.st_cur
        self.st_cur = new_state
        self.after_transition(new_state)
        self.rwlock.release()
    
    def before_transition(self,state):
        print "old:"+self.st_last+" new:"+state
    
    def after_transition(self,state):
        print "after_transition " +state
        
    def process(self,data):
        try:
            self.rwlock.acquire()
            handle = self.process_table.get(self.st_remote)           
            if None != handle:
                handle(data)      
            else:
                print "state:"+self.st_cur+" not foud,data will drop-->" + data        
            self.rwlock.release()                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
            self.rwlock.release()            
        
    def register_process(self,state, handle):
        if False ==  self.check_state_value(state):
            pass        
        self.rwlock.acquire()
        self.process_table[state] = handle
        self.rwlock.release()

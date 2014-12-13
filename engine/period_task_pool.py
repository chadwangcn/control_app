#coding=utf-8
import sys
import threading
import  sched,time
import traceback
import datetime

'''
period task pool:

'''

class task_worker():
        def __init__(self,_name,_func,_period):
            self.name = _name
            self.start_time = datetime.datetime.now() 
            self.period = _period
            self.func = _func
            
        def do_run(self):
            try:
                self.start_time = datetime.datetime.now() 
                self.func()
            except Exception,e:
                print Exception,":",e
                traceback.print_exc()
        
        def need_run(self):
            diff = datetime.datetime.now() - self.start_time
            if diff >= self.period:
                return True
            else:
                return False 
            
            
class period_task_pool(threading.Thread):
    def __init__(self,_max_woker=2,_default_sleep=0):
        self.threadid= 0
        self.bExit =False
        self.max_woker = _max_woker
        self.default_sleep = _default_sleep
        threading.Thread.__init__(self)  
        self.SubcriberLst = {}
        self.rwlock = threading.RLock() #
    
    def run(self):
        while self.bExit == False:
            try:
                time.sleep(1)                
                self.rwlock.acquire()
                for k in self.SubcriberLst.keys():
                    if None != self.SubcriberLst[k]:
                        self.SubcriberLst[k]()
                self.rwlock.release()
            except Exception,e:
                print Exception,":",e
                traceback.print_exc() 
                self.rwlock.release()   
            
    def addTask(self,_name,_func,_period):
        ret = False
        try:
            self.rwlock.acquire()
            if self.SubcriberLst.has_key(_name):
                ret = False
            else:
                worker = task_worker.task_worker(_name,_func,_period)
                self.SubcriberLst[_name] = worker;
                ret = True
            self.rwlock.release()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            self.rwlock.release()   
        return ret
    
    def delTask(self,_name):
        try:
            self.rwlock.acquire()
            if self.SubcriberLst.has_key(_name):
                del self.SubcriberLst[_name]
            self.rwlock.release()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            self.rwlock.release()   
    
    def startPool(self):
        try:
            self.rwlock.acquire()
            self.start()
            self.rwlock.release()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            self.rwlock.release()   
    
    def stopPool(self):
        try:
            self.rwlock.acquire()
            self.bExit = True
            self.killAllWorker()
            self.Stop()
            self.rwlock.release()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            self.rwlock.release() 
    
    def creatWorkerPool(self):
        pass
    
    def killAllWorker(self):
        pass
#coding=utf-8
import sys
import threading
import  sched,time
import traceback

class period_task_pool(threading.Thread):
    def __init__(self):
        self.threadid= 0
        self.bExit =False
        threading.Thread.__init__(self)  
        self.SubcriberLst = {}
        self.rwlock = threading.RLock() #
    
    def run(self):
        while self.bExit == False:
            try:
                time.sleep(1)
                print "++++++++++++++"
                self.rwlock.acquire()
                for k in self.SubcriberLst.keys():
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
                self.SubcriberLst[_name] = _func;
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
            self.stop() 
            self.rwlock.release()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            self.rwlock.release() 
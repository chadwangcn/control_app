#coding=utf-8
import sys
from chart import *
from SolutionParamSet import *
from solutionParam import *
from  CreateMethod import *
from segment_setting import *
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic
from data_source.Logtrace import *
from engine.engine_controller import *
from engine.period_task_pool import *
from solution_mrg import *
from threading import Thread
import  sched,time

class transfer_worker(threading.Thread):            
    def __init__(self,_parent,_cb_start=None,_cb_progress=None,_cb_end=None,_cb_error=None):
        '''
        Constructor
        '''
        self._parent = _parent
        self.bExit = False        
        
        'CallBack Func'
        self.cb_start = _cb_start
        self.cb_progress = _cb_progress
        self.cb_end = _cb_end
        self.cb_error = _cb_error 
        
        'Max retry count is 5'
        self.retry_max_cnt = 5
        
        threading.Thread.__init__(self)          
        self.rwlock = threading.RLock() #
        
    def start_async(self):
        self.start()
    
    def stop_async(self):
        self.bExit = True
        
        
    def run(self):
        cnt_run = 0
        while self.bExit == False and cnt_run < self.retry_max_cnt:  
            self.rwlock.acquire()
            try:
                if None != self.cb_start:
                    self.cb_start()
                    
                if True == self._parent.engine.SendCfgData(self._parent.SolutionParamSet,self.cb_progress):
                    print "all cfg Ok"
                    self.bExit = True
                    if None != self.cb_end:
                        self.cb_end()
                    self._parent.emit(SIGNAL("Auto_Ready") ) 
                else:
                    print "all cfg fail"
                    if None != self.cb_error:
                        self.cb_error() 
                    self._parent.emit(SIGNAL("Method_send_error") ) 
                'self._parent.OnTransferCancel()'
                self._parent.IsSendRunning = False 
            except Exception,e:
                print Exception,":",e
                traceback.print_exc()
                if None != self.cb_error:
                    self.cb_error() 
                
            cnt_run = cnt_run +  1
            self.rwlock.release()
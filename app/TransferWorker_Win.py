#coding=utf-8

from SolutionParamSet import *
import sys
from PyQt4 import QtGui, QtCore, uic
import traceback 
from chart import *
from transfer_worker import *
from SolutionParamSet import *
from solutionParam import *
from  CreateMethod import *
from segment_setting import *
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic
from engine.engine_controller import *
from threading import Thread
import  sched,time

UI_PATH = "../res/ui/"
UI_MAIN_WIN = "progress_ctrl.ui"   

class TransferWorker_Win( QtGui.QDialog ):
    def __init__( self,_parent ):
        super( TransferWorker_Win, self ).__init__()
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))        
        self.dlg= uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.default_folder_path = os.getcwd()
        
        self._parent = _parent
        self.worker = transfer_worker(_parent)
        
    def bindUI(self):
        self.connect( self.dlg.pb_cancel,  QtCore.SIGNAL('clicked()'), self.OnCancelTransfer )
        self.ProBar.setRange(0,100)
        '''
        self.connect(self, QtCore.SIGNAL("GenNewSolution"),self.OnGenSolution )
        '''  
    def StartProgress(self):
        self.worker.start_async()
        
    def StopProgress(self):
        self.worker.stop_async()
        
    def OnCancelTransfer(self):
        self.canceled()
    
    def OnUpdateProgressBar(self, _percent):
        self.ProBar.setValue( _percent )
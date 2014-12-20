#coding=utf-8

from SolutionParamSet import *
import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic
import traceback 


UI_PATH = "../res/ui/"
UI_MAIN_WIN = "createmethod.ui"   
 
class CreateMethod( QtGui.QDialog ):
    def __init__( self ):
        super( CreateMethod, self ).__init__()
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))   
        self.dlg= uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.bindUI()
        self.load_data()
        self.filepath = ""
        self.filename = ""
        self.SolutionParamSet = SolutionParamSet()
        self.SolutionParamSet.previousState = "idel"
        self.SolutionParamSet.currentState = "create"
        
        
    def bindUI(self):        
        self.connect( self.dlg.pbNavPath, QtCore.SIGNAL('clicked()'), self.OnNav )
        self.connect( self.dlg.pbCreate,  QtCore.SIGNAL('clicked()'), self.OnCreate )
        self.connect( self.dlg.pbCancel,  QtCore.SIGNAL('clicked()'), self.OnExit )
        self.connect( self.dlg.pbAutoName,QtCore.SIGNAL('clicked()'), self.OnAutoName )        
        '''self.filepath =  QtCore.QCoreApplication.applicationDirPath() +  '/cfg'  '''
        self.dlg.Path.setText( os.getcwd() )
        
        
    def load_data(self):
        self.dlg.MethodType.insertItem(0, "恒温"   )
        self.dlg.MethodType.insertItem(1, "程序升温" )
        self.dlg.MethodType.insertItem(2, "循环程序升温")
        self.filepath = "d:\\"

        
    
    def OnNav(self):
        tmpPath = QtGui.QFileDialog.getExistingDirectory()
        if tmpPath != "":
            self.filepath = tmpPath
        self.dlg.Path.setText(self.filepath)
        
    
    def OnAutoName(self):
        self.filename = "auto_save_cfg"
        self.dlg.FileName.setText(self.filename)
        
    
    def OnCheckValue(self):
        ret = True
        status = ""
        try:
            if self.dlg.FileName.text() == "":
                ret = False
                status = "FileName Empty"
                raise status
            else:
                self.SolutionParamSet.filename = self.dlg.FileName.text() 
                
            
            if self.dlg.Path.text() == "":
                ret = False
                status = "Path Empty"
                raise status
            else:
                self.SolutionParamSet.filepath = self.dlg.Path.text()                 
            
            self.SolutionParamSet.mainctrltype = self.dlg.MethodType.currentIndex()
            self.SolutionParamSet.hasTCD = self.dlg.tcd.isChecked()
            self.SolutionParamSet.hasFID = self.dlg.fid.isChecked()
            self.SolutionParamSet.hasGasBox = self.dlg.gasbox.isChecked()
            self.SolutionParamSet.hasSwitchCtrl = self.dlg.switchctrl.isChecked()
            self.SolutionParamSet.hasAssistantTemp = self.dlg.assistbox.isChecked()
            print self.SolutionParamSet
            
        except Exception,e:
            traceback.print_exc()   
            ret = False
            status = "Get UI Data Error"
        return [ret,status]
        
    
    def GetSolutionParamSet(self):
        return self.SolutionParamSet
        
  
    def OnCreate(self):
        [ret ,status] = self.OnCheckValue()
        print status
        if ret:  
            self.accept()            
        else:
            self.reject()
    
    def OnExit(self):       
        self.reject()
        
    def OnUpData(self):
        pass
      
 
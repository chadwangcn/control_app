#coding=utf-8

from SolutionParamSet import *
import sys
from PyQt4 import QtGui, QtCore, uic
import traceback 
from chart import *
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
UI_MAIN_WIN = "solution_mgr.ui"   
 
class Solution_Mrg( QtGui.QDialog ):
    def __init__( self ):
        super( Solution_Mrg, self ).__init__()
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
        self.SolutionParamSet = None
        self.dlg= uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.default_folder_path = os.getcwd()
        self.bindUI()
        self.load_data()
        self.__FILTER_TAG__ = "Cfg Data (*.jxc)"
        
        
    def bindUI(self):        
        self.connect( self.dlg.pb_new, QtCore.SIGNAL('clicked()'), self.OnNew )
        self.connect( self.dlg.pb_import,  QtCore.SIGNAL('clicked()'), self.OnImport )
        self.connect( self.dlg.pb_edit,  QtCore.SIGNAL('clicked()'), self.OnEdit )
        self.connect( self.dlg.pb_save,QtCore.SIGNAL('clicked()'), self.OnSave )    
        self.connect( self.dlg.pb_save_as,QtCore.SIGNAL('clicked()'), self.OnSaveAs )    
        self.connect( self.dlg.pb_action,QtCore.SIGNAL('clicked()'), self.OnAction ) 
        
        self.connect(self, QtCore.SIGNAL("GenNewSolution"),self.OnGenSolution )
        self.connect(self, QtCore.SIGNAL("GenSegment"),self.OnGenSegment )
        self.connect(self, QtCore.SIGNAL("GenSwitchCtrl"),self.OnGenSwitchCtrl )
        self.connect(self, QtCore.SIGNAL("OnFinished"),self.OnMethodCreateFinished )
        self.connect(self, QtCore.SIGNAL("UpdateMethodCfgView"),self.UpdateMethodTableView )
        
        self.tableViewModel = None        
        self.tableViewModel = QStandardItemModel()
        
        self.tableViewModel.setColumnCount(2)
        
        
        
        self.tableViewModel.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant("Name"))
        self.tableViewModel.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant("Value"))
        
        self.tableView_method.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.tableView_method.setSelectionBehavior(QTableWidget.SelectRows) 
        self.tableView_method.setSelectionMode(QTableWidget.SingleSelection)
        
        
        Item_Index = 0
        self.tableViewModel.setItem(Item_Index,0,QStandardItem("方法") )
        self.tableViewModel.setItem(Item_Index,1,QStandardItem("未配置") )
        
        Item_Index = Item_Index + 1
        self.tableViewModel.setItem(Item_Index,0,QStandardItem("存储路径") )
        self.tableViewModel.setItem(Item_Index,1,QStandardItem("未配置") )
        
        Item_Index = Item_Index + 1
        self.tableViewModel.setItem(Item_Index,0,QStandardItem("控温模式") )
        self.tableViewModel.setItem(Item_Index,1,QStandardItem("未配置") )
        
        Item_Index = Item_Index + 1
        self.tableViewModel.setItem(Item_Index,0,QStandardItem("台阶数") )
        self.tableViewModel.setItem(Item_Index,1,QStandardItem("未配置") )
        
        Item_Index = Item_Index + 1
        self.tableViewModel.setItem(Item_Index,0,QStandardItem("总时间") )
        self.tableViewModel.setItem(Item_Index,1,QStandardItem("未配置") )
        
        
        
        self.tableView_method.setModel(self.tableViewModel)
        
        head = QtGui.QHeaderView(QtCore.Qt.Horizontal, self)  
        #自定义模式，不能拖动  
        head.setResizeMode(QtGui.QHeaderView.Custom)  
        self.tableView_method.setHorizontalHeader(head)  
        #设置0~3列的宽度  
        head.resizeSection(0,100)  
        head.resizeSection(1,404)  
       
        
        pass
    
    def OnNew(self):
        dlg = CreateMethod()
        if dlg.exec_() == 1:
            self.SolutionParamSet = dlg.GetSolutionParamSet()
            self.SolutionParamSet.previousState = self.SolutionParamSet.currentState
            print "Will Create the data"
            self.emit(SIGNAL("GenNewSolution") )
            self.hasCreateMethod = True
            self.emit(SIGNAL("UpdateMenuUI") )
        else:
            print "Cancel create the data"
            
    def OnImport(self):
        try:
            self.SolutionParamSet = SolutionParamSet.SolutionParamSet()
            tmpPath = QtGui.QFileDialog.getOpenFileName(None,"",
                                                        self.default_folder_path,self.__FILTER_TAG__,
                                                        None)
            
            
            if self.SolutionParamSet.ReadCfg(tmpPath):
                self.emit(SIGNAL("UpdateMethodCfgView") )
                self.SolutionParamSet.filename = "xx"
                self.SolutionParamSet.filepath = "xx"
                QtGui.QMessageBox.information( self, "方法", "导入方法成功" )
                
            else:
                print "load error"
                 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    
    def OnEdit(self):
        try:            
            pass
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def OnSave(self):
        print "On OnSave"
        if self.SolutionParamSet != None:
            if self.SolutionParamSet.SaveCfg( self.SolutionParamSet.filepath + self.SolutionParamSet.filename + ".jxc" ):
                print "save ok"
                
                self.hasCreateMethod = True
                self.emit(SIGNAL("UpdateMethodCfgView") )
                self.emit(SIGNAL("UpdateMenuUI") )
                QtGui.QMessageBox.information( self, "方法", "方法保存 成功" )
            else:
                print "save fail"
        else:
            print "OnSave error"
            
    def OnSaveAs(self):
        print "On OnSaveAs"
        tmpPath = QtGui.QFileDialog.getSaveFileName(None,"",
                                                        self.default_folder_path,self.__FILTER_TAG__,
                                                        None)
        if tmpPath != "" and self.SolutionParamSet != None:
            if self.SolutionParamSet.SaveCfg( tmpPath ):
                print "save ok"
                
                self.hasCreateMethod = True
                self.emit(SIGNAL("UpdateMethodCfgView") )
                self.emit(SIGNAL("UpdateMenuUI") )
                self.hasCreateMethod = True 
                QtGui.QMessageBox.information( self, "方法", "方法另保存 成功" )
                print "OnSave As error"
        else:  
            print "save as fail"
            
    def OnAction(self):
        try:         
            self.SolutionParamSet.dump()   
            self.accept()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            
    def OnGenSolution(self):
        print "Gen New Solution "
        if self.SolutionParamSet.previousState == "create":
            if self.SolutionParamSet.mainctrltype == 0 and         \
               self.SolutionParamSet.hasFID == False   and         \
               self.SolutionParamSet.hasTCD == False   and         \
               self.SolutionParamSet.hasAssistantTemp == False and \
               self.SolutionParamSet.hasGasBox == False :
                
                dlg = solutionParam(self.SolutionParamSet)
                if dlg.exec_() == 1:
                    self.SolutionParamSet.previousState = self.SolutionParamSet.currentState 
                    self.SolutionParamSet = dlg.GetSolutionParamSet()         
                    if self.SolutionParamSet.hasSwitchCtrl == True:
                        self.emit(SIGNAL("GenSwitchCtrl") )
                    else:
                        self.emit(SIGNAL("OnFinished") )                    
            elif self.SolutionParamSet.hasFID == False   and         \
                   self.SolutionParamSet.hasTCD == False   and         \
                   self.SolutionParamSet.hasAssistantTemp == False and \
                   self.SolutionParamSet.hasGasBox == False :                
                self.OnGenSegment()
            
            else :
                dlg = solutionParam(self.SolutionParamSet)
                if dlg.exec_() == 1:
                    self.SolutionParamSet.previousState = self.SolutionParamSet.currentState 
                    self.SolutionParamSet = dlg.GetSolutionParamSet()         
                    if self.SolutionParamSet.mainctrltype == 0 :
                        if self.SolutionParamSet.hasSwitchCtrl == True:
                            self.emit(SIGNAL("GenSwitchCtrl") )
                        else:
                            self.emit(SIGNAL("OnFinished") )
                    else:
                        self.emit(SIGNAL("GenSegment") )          
            
        else:
            if self.SolutionParamSet.previousState == "solutionparam":
                if self.SolutionParamSet.mainctrltype != 0:
                    dlg = SegmentSetting(self.SolutionParamSet)
                    dlg.exec_() 
                    self.SolutionParamSet.previousState = self.SolutionParamSet.currentState                
                    self.emit(SIGNAL("GenNewSolution") )  
                else:
                    print "error"
            elif self.SolutionParamSet.previousState == "segmentsetting" and self.SolutionParamSet.hasSwitchCtrl:
                pass
            
    def OnGenSegment(self):
        dlg = SegmentSetting(self.SolutionParamSet)
        if dlg.exec_() == 1:
            self.SolutionParamSet.previousState = self.SolutionParamSet.currentState 
            self.SolutionParamSet = dlg.GetSolutionParamSet()      
            for k,data in self.SolutionParamSet.SegParamSet.iteritems():                
                print "out segid:" + str(data.segid) + " start_temp" +  str(data.start_temp)
            if self.SolutionParamSet.hasSwitchCtrl == True:
                self.emit(SIGNAL("GenSwitchCtrl") )  
            else:
                self.emit(SIGNAL("OnFinished") )
                        
    
    def OnGenSwitchCtrl(self):
        self.emit(SIGNAL("OnFinished") )
        print 'OnGenSwitchCtrl'
        
    
    def OnMethodCreateFinished(self):        
        self.emit(SIGNAL("UpdateMethodCfgView") )
        print 'OnMethodCreateFinished'
  
    def UpdateMethodTableView(self):
        try:
            print "UpdateMethodTableView"          
            Item_Index = 0
            self.tableViewModel.setItem(Item_Index,0,QStandardItem("方法") )
            self.tableViewModel.setItem(Item_Index,1,QStandardItem(self.SolutionParamSet.filename) )
            
            Item_Index = Item_Index + 1
            self.tableViewModel.setItem(Item_Index,0,QStandardItem("存储路径") )
            self.tableViewModel.setItem(Item_Index,1,QStandardItem(self.SolutionParamSet.filepath) )
            
            if self.SolutionParamSet.hasSwitchCtrl:
                Item_Index = Item_Index + 1
                self.tableViewModel.setItem(Item_Index,0,QStandardItem("电磁阀") )
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("使能") )
                
            Item_Index = Item_Index + 1
            self.tableViewModel.setItem(Item_Index,0,QStandardItem("控温模式") )
            if self.SolutionParamSet.mainctrltype == 0 :
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("恒温") )
            elif self.SolutionParamSet.mainctrltype == 1 :
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("程升") )
            elif self.SolutionParamSet.mainctrltype == 2 :
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("循环程升") )
                
            if self.SolutionParamSet.hasFID:
                Item_Index = Item_Index + 1
                self.tableViewModel.setItem(Item_Index,0,QStandardItem("FID") )
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("使能") )
                
            if self.SolutionParamSet.hasTCD:
                Item_Index = Item_Index + 1
                self.tableViewModel.setItem(Item_Index,0,QStandardItem("TCD") )
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("使能") )
                
            if self.SolutionParamSet.hasAssistantTemp:
                Item_Index = Item_Index + 1
                self.tableViewModel.setItem(Item_Index,0,QStandardItem("辅温箱") )
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("使能") )
                
            if self.SolutionParamSet.hasGasBox:
                Item_Index = Item_Index + 1
                self.tableViewModel.setItem(Item_Index,0,QStandardItem("汽化室") )
                self.tableViewModel.setItem(Item_Index,1,QStandardItem("使能") )
                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
        
        
    def load_data(self):
        pass
     
    
  
        
  
    def OnCreate(self):
        [ret ,status] = self.OnCheckValue()
        print status
        if ret:  
            self.accept()            
        else:
            self.reject()
    
    def OnExit(self):       
        self.reject()
        
    def GetSolutionParamSet(self):
        return self.SolutionParamSet
            
      
 
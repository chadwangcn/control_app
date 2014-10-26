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
from engine.engine_controller import *
from threading import Thread
import  sched,time



UI_PATH = "../res/ui/"
UI_MAIN_WIN = "MainWin.ui"  

class mainui( QtGui.QMainWindow ):
    def __init__( self ):
        super( mainui, self ).__init__()      
        self.win = uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.status = self.statusBar()
        self.menu = self.menuBar()
        self.SolutionParamSet = None
        
        self.hasCreateMethod = False
        
        
        self.status.showMessage("This is StatusBar",5000)
        self.bindUI()
        'self.build_engine() '
        self.network_error = False  
        
        
    def bindUI(self):        
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))
        self.connect( self.win.create,QtCore.SIGNAL("triggered()"), self.OnCreate )
        self.connect( self.win.open,QtCore.SIGNAL("triggered()"), self.OnOpen )
        self.connect( self.win.save,QtCore.SIGNAL("triggered()"), self.OnSave )
        self.connect( self.win.saveas,QtCore.SIGNAL("triggered()"), self.OnSaveAs )
        self.connect( self.win.close,QtCore.SIGNAL("triggered()"), self.OnClose )
        
        ' bind solutionParam  '
        self.connect( self.win.action_FID,QtCore.SIGNAL("triggered()"), self.OnParamSetting )
        self.connect( self.win.action_TCD,QtCore.SIGNAL("triggered()"), self.OnParamSetting )
        self.connect( self.win.qihuashi,QtCore.SIGNAL("triggered()"), self.OnParamSetting )
        self.connect( self.win.fuzhuwenxiang,QtCore.SIGNAL("triggered()"), self.OnParamSetting )
        self.connect( self.win.waishimingmin,QtCore.SIGNAL("triggered()"), self.OnParamSetting )
        self.connect( self.win.zhuwenxiang,QtCore.SIGNAL("triggered()"), self.OnParamSetting )
        
        'bind pb button'
        self.connect( self.pb_start,QtCore.SIGNAL("clicked()"),self.OnClickPbStart)
        self.connect( self.pb_stop,QtCore.SIGNAL("clicked()"),self.OnClickPbStop)
        self.connect( self.pb_reset,QtCore.SIGNAL("clicked()"),self.OnClickPbReset)
        self.connect( self.pb_sync,QtCore.SIGNAL("clicked()"),self.OnClickPbSync)
        
        self.connect(self, QtCore.SIGNAL("GenNewSolution"),self.OnGenSolution )
        self.connect(self, QtCore.SIGNAL("GenSegment"),self.OnGenSegment )
        self.connect(self, QtCore.SIGNAL("GenSwitchCtrl"),self.OnGenSwitchCtrl )
        self.connect(self, QtCore.SIGNAL("OnFinished"),self.OnMethodCreateFinished )
        self.connect(self, QtCore.SIGNAL("UpdateMethodCfgView"),self.UpdateMethodTableView )
        self.connect(self, QtCore.SIGNAL("UpdateMenuUI"),self.UpdateMenuUI )
        
        
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
        
        
        
        self.tableView_method.setModel(self.tableViewModel)
        
        head = QtGui.QHeaderView(QtCore.Qt.Horizontal, self)  
        #自定义模式，不能拖动  
        head.setResizeMode(QtGui.QHeaderView.Custom)  
        self.tableView_method.setHorizontalHeader(head)  
        #设置0~3列的宽度  
        head.resizeSection(0,100)  
        head.resizeSection(1,404)  
        
        self.emit(SIGNAL("UpdateMenuUI") )
        
        
        'init data'
        self.label_state.setText('UnKnow')
        self.label_state.setStyleSheet("background-color:red")
        ft = QFont()
        ft.setPointSize(18)
        self.label_state.setFont(ft)
        pe = QPalette()          
        pe.setBrush(QPalette.Base,QBrush(QColor(255,0,0,0)));        
        pe.setColor(QPalette.WindowText,Qt.black)
        self.label_state.setPalette(pe)
        
    
    def build_engine(self):
        try:
            self.engine = engine_controller()
            self.engine.prepare_engine(self.OnNotifyMsg)
            self.engine.start_engine()
            '''self.create_period_check_task()'''
            
                      
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            
    def stop_ui(self):
        self.sched_task.empty()
        self.sched_task.cancel()
        
    def create_period_check_task(self):
        self.sched_task  = sched.scheduler(time.time,time.sleep)
        self.period_check_task()
        t = threading.Thread(target=self.period_check_task)
        t.start()
            
    def period_check_task(self):
        '''
         period check task
         period =  250 ms 
        '''
        
        
        if self.engine.bTimeOut:
            self.label_state.setText('通讯错误')
            self.label_state.setStyleSheet("background-color:red")
            ft = QFont()
            ft.setPointSize(18)
            self.label_state.setFont(ft)
            pe = QPalette()          
            pe.setBrush(QPalette.Base,QBrush(QColor(255,0,0,0)));        
            pe.setColor(QPalette.WindowText,Qt.black)
            self.label_state.setPalette(pe)
        else:
            self.label_state.setText( self.engine.statemachine.st_remote)
            self.label_state.setStyleSheet("background-color:green")
            ft = QFont()
            ft.setPointSize(18)
            self.label_state.setFont(ft)
            pe = QPalette()          
            pe.setBrush(QPalette.Base,QBrush(QColor(255,0,0,0)));        
            pe.setColor(QPalette.WindowText,Qt.black)
            self.label_state.setPalette(pe)
        
        self.sched_task.enter(0.25,1,self.period_check_task,())
        print "22223333"
        self.sched_task.run()
        print "444444444444444"
        
   
        
    def OnNotifyMsg(self, _msg):        
        try:
            if   _msg[0] == "machine_mode":
                self.label_state.setText( _msg[1] )
            elif _msg[0] == "timeout":
                '''self.label_state.setText( "network error" )
                self.network_error = False'''
            pass
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def load_data(self):
        pass
    
    
    
    def UpdateMenuUI(self):
        if self.hasCreateMethod:
            print "disable"
            self.win.create.setEnabled (False)    
            self.win.open.setEnabled (False)    
            self.win.save.setEnabled (True)
            self.win.saveas.setEnabled (True)
            self.win.close.setEnabled (True)
        
        else:
            print "enable"
            self.win.create.setEnabled (True)
            self.win.open.setEnabled (True)
            self.win.save.setEnabled (False)
            self.win.saveas.setEnabled (False)
            self.win.close.setEnabled (False)

                
    
           
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
        
         
    def OnGenSolution(self):
        print "Gen New Solution "
        if self.SolutionParamSet.previousState == "create":
            if self.SolutionParamSet.hasFID == False and self.SolutionParamSet.hasTCD == False and self.SolutionParamSet.hasAssistantTemp == False and self.SolutionParamSet.hasGasBox == False :
                print "Do Nothing"
            else:
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
        self.DumpCfgData(self.SolutionParamSet)
        print 'OnMethodCreateFinished'
        
    def DumpCfgData(self,_object):
        pass 
       
    def OnOpen(self):
        try:
            self.SolutionParamSet = SolutionParamSet.SolutionParamSet()
            tmpPath = QtGui.QFileDialog.getOpenFileName()
            if self.SolutionParamSet.ReadCfg(tmpPath) == False:
                raise Exception("segment cnt", "error") 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            QtGui.QMessageBox.information( self, "Pyqt", "Open Error" )
    
    def OnCreate(self):        
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
        
    def OnSave(self):
        print "On OnSave"
        if self.SolutionParamSet != None:
            if self.SolutionParamSet.SaveCfg( self.SolutionParamSet.filepath + self.SolutionParamSet.filename ):
                print "save ok"
                
                self.hasCreateMethod = True
                self.emit(SIGNAL("UpdateMethodCfgView") )
                self.emit(SIGNAL("UpdateMenuUI") )
                QtGui.QMessageBox.information( self, "Pyqt", "save Ok" )
            else:
                print "save fail"
        else:
            print "OnSave error"
    
    def OnSaveAs(self):
        print "On OnSaveAs"
        tmpPath = QtGui.QFileDialog.getSaveFileName()
        if tmpPath != "" and self.SolutionParamSet != None:
            if self.SolutionParamSet.SaveCfg( tmpPath ):
                print "save ok"
                
                self.hasCreateMethod = True
                self.emit(SIGNAL("UpdateMethodCfgView") )
                self.emit(SIGNAL("UpdateMenuUI") )
                self.hasCreateMethod = True 
                QtGui.QMessageBox.information( self, "Pyqt", "save as ok" )
                print "OnSave As error"
        else:  
            print "save as fail"
        
    def OnClose(self):
        print "On OnClose"
        self.hasCreateMethod = False
        self.emit(SIGNAL("UpdateMenuUI") )

    def OnParamSetting(self):        
        print "On Create"
        
    def OnSwitchCtrlSetting(self):
        pass
    
    def OnMutiSegSetting(self):
        pass
    
   
    
    def OnClickPbStart(self):
        try:            
            self.engine.SendStateAsync( 'Auto_Running' ) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    def OnClickPbStop(self):
        try:
            self.engine.SendStateAsync( 'Auto_End' ) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
   
    def OnClickPbReset(self):
        try:
            self.engine.SendStateAsync( 'Init_Err' ) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    def OnClickPbSync(self):
        try:
            self.engine.SendCfgData(self.SolutionParamSet)
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    
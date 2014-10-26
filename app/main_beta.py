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
from solution_mrg import *
from threading import Thread
import  sched,time

UI_PATH = "../res/ui/"
UI_MAIN_WIN = "main_beta.ui"  

MODULE_TAG = "main_beta_ui"

class main_beta( QtGui.QDialog  ):
    def __init__( self ):
        super( main_beta, self ).__init__()  
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))   
        self.log = LogTrace()
        self.win = uic.loadUi( UI_PATH+UI_MAIN_WIN, self )   
        self.logtrace  = LogTrace()
        self.SolutionParamSet = None
        self.hasCreateMethod = False
        self.hasTimeOut = False
        self.page_normal = 0 
        self.page_factory = 1 
        self.bindUI()
        self.build_engine() 
        
    def bindUI(self):        
        self.label_state.setText('初始化中...')
        self.SetLabelColor(self.label_state,"background-color:green")
        
        self.label_info.setText('初始化中 ...')
        self.SetLabelColor(self.label_info,"background-color:green")
        
        'bind pb button'
        self.connect( self.pb_halt,QtCore.SIGNAL("clicked()"),self.OnClickPbHalt)
        self.connect( self.pb_autotest,QtCore.SIGNAL("clicked()"),self.OnClickPbAutotest)
        self.connect( self.pb_solution_setting,QtCore.SIGNAL("clicked()"),self.OnClickPbSolutionSetting)
        self.connect( self.pb_send,QtCore.SIGNAL("clicked()"),self.OnClickPbSend)        
        self.connect( self.pb_run,QtCore.SIGNAL("clicked()"),self.OnClickPbRun)
        self.connect( self.pb_stop,QtCore.SIGNAL("clicked()"),self.OnClickPbStop)
        self.connect( self.pb_action_1,QtCore.SIGNAL("clicked()"),self.OnClickPbAction1)
        self.connect( self.pb_action_2,QtCore.SIGNAL("clicked()"),self.OnClickPbAction2)
        self.connect( self.pb_action_3,QtCore.SIGNAL("clicked()"),self.OnClickPbAction3)
        self.connect( self.pb_action_4,QtCore.SIGNAL("clicked()"),self.OnClickPbAction4)
        self.connect( self.pb_export,QtCore.SIGNAL("clicked()"),self.OnClickPbExport)
        self.connect( self.pb_factory,QtCore.SIGNAL("clicked()"),self.OnClickPbFactory)
        self.connect( self.pb_auto,QtCore.SIGNAL("clicked()"),self.OnClickPbAuto)
        
        self.connect( self.sw_1,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_2,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_3,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_4,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_5,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_6,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_7,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)
        self.connect( self.sw_8,QtCore.SIGNAL("clicked()"),self.OnSwitchStateChange)        
        self.connect( self.dial_pad,QtCore.SIGNAL("sliderReleased()"),self.OnDialsliderReleased)
        self.connect( self.dial_pad,QtCore.SIGNAL("sliderMoved (int)"),self.OnDialPadsliderMoved )
        
        self.connect(self, QtCore.SIGNAL("TimeOut"),self.OnTimeOut )
        self.connect(self, QtCore.SIGNAL("UpdateUI"),self.OnUpdateUI )
        
        self.connect( self.horizontalScrollBar_1,QtCore.SIGNAL("sliderMoved (int)"),self.OnhorizontalScrollBar_1_sliderMoved )
        self.connect( self.horizontalScrollBar_1,QtCore.SIGNAL("sliderReleased"),self.OnhorizontalScrollBar_1_sliderReleased )
        self.connect( self.horizontalScrollBar_2,QtCore.SIGNAL("sliderMoved (int)"),self.OnhorizontalScrollBar_2_sliderMoved )
        self.connect( self.horizontalScrollBar_2,QtCore.SIGNAL("sliderReleased"),self.OnhorizontalScrollBar_2_sliderReleased )
        self.connect( self.horizontalScrollBar_3,QtCore.SIGNAL("sliderMoved (int)"),self.OnhorizontalScrollBar_3_sliderMoved )
        self.connect( self.horizontalScrollBar_3,QtCore.SIGNAL("sliderReleased"),self.OnhorizontalScrollBar_3_sliderReleased )
        self.connect( self.horizontalScrollBar_4,QtCore.SIGNAL("sliderMoved (int)"),self.OnhorizontalScrollBar_4_sliderMoved )
        self.connect( self.horizontalScrollBar_4,QtCore.SIGNAL("sliderReleased"),self.OnhorizontalScrollBar_4_sliderReleased )
        
        self.display_table = {"UnKnow":"未知","Init_Err":"初始化中",    "Init_OK":"初始化成功",      "Factory":"工厂模式",      
                              "Auto_Config":"等待方法", "Auto_Ready":"就绪",   "Auto_Warmming":"预热",
                              "Auto_WarmUp":"预热完成", "Auto_Running":"运行", "Auto_End":"结束"  }
        
        self.tabWidget.setCurrentIndex(self.page_normal)
        self.tabWidget.setTabEnabled(self.page_factory,False) 
        self.tabWidget.setTabEnabled(self.page_normal,True) 
        
        '  initial lcd pad and lcd number '
        self.dial_pad.setValue(0)
        self.lcdNumber.display(self.dial_pad.value())
        
        ' QlineEdit only  numberi avaiable'
        vl =  QIntValidator(0,100)
        self.lineEdit_1.setValidator(vl) 
        self.lineEdit_1.setText("0")
        self.horizontalScrollBar_1.setValue(0)
        self.progressBar_1.setValue(0)

        self.lineEdit_2.setValidator(vl) 
        self.lineEdit_2.setText("0")
        self.horizontalScrollBar_2.setValue(0)
        self.progressBar_2.setValue(0)
        
        self.lineEdit_3.setValidator(vl) 
        self.lineEdit_3.setText("0")
        self.horizontalScrollBar_3.setValue(0)
        self.progressBar_3.setValue(0)
        
        self.lineEdit_4.setValidator(vl) 
        self.lineEdit_4.setText("0")
        self.horizontalScrollBar_4.setValue(0)
        self.progressBar_4.setValue(0)
        
        self.logtrace.info( MODULE_TAG, "bindUI")
    
    def build_engine(self):
        try:
            self.engine = engine_controller()
            self.engine.prepare_engine(self.OnNotifyMsg)
            self.engine.start_engine()
            self.create_period_check_task()    
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 

        
    def SetLabelColor(self,_label,_color):        
        _label.setStyleSheet(_color)
        ft = QFont()
        ft.setPointSize(18)
        _label.setFont(ft)
        pe = QPalette()          
        pe.setBrush(QPalette.Base,QBrush(QColor(255,0,0,0)));        
        pe.setColor(QPalette.WindowText,Qt.black)
        _label.setPalette(pe)
        
   
        
    def start_period_check_task(self):
        t = threading.Timer(5,self.period_check_task,())
        t.start()
        
    def create_period_check_task(self):
        
        print "Before Start --> 11 "
        self.start_period_check_task()
        
        '''
        self.sched_task  = sched.scheduler(time.time,time.sleep)
        self.sched_task.enter(2, 1, self.period_check_task, ()  )
        self.sched_task.run()   '''
        print "After Run"
            
    def period_check_task(self):
        '''
         period check task
         period =  250 ms 
        '''
        self.emit(SIGNAL("UpdateUI") )     
        self.start_period_check_task()
        '''self.sched_task.enter(0.25,1,self.period_check_task,())        
        self.sched_task.run() '''
       
   
    def OnUpdateUI(self): 
        self.logtrace.info( MODULE_TAG, "----->bindUI")
        if self.engine.bTimeOut:
            self.label_state.setText('通讯错误')
            self.SetLabelColor(self.label_state,"background-color:red")
            
            self.label_info.setText('请检查网络连接...')
            self.SetLabelColor(self.label_info,"background-color:red")
        else:            
            self.SetLabelColor(self.label_state,"background-color:green")
            
            self.label_info.setText('系统正常运行中...')
            self.SetLabelColor(self.label_info,"background-color:green")
    
    def OnTimeOut(self):
        pass
        
        
    def OnNotifyMsg(self, _msg):        
        try:
            if   _msg[0] == "machine_mode":
                state_handle = self.display_table.get(_msg[1])
                if state_handle != None:
                    self.label_state.setText( state_handle )
                else:
                    self.label_state.setText( _msg[1] )                    
                self.hasTimeOut = False
                
            elif _msg[0] == "timeout":
                self.hasTimeOut = True
                self.emit(SIGNAL("TimeOut") )   
                
            self.emit(SIGNAL("UpdateUI") )           
               
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    
    def OnClickPbRun(self):
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
  
    
    def OnClickPbHalt(self):
        try:            
            self.engine.SendStateAsync( 'Init_Err' ) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
            
    def OnClickPbAuto(self):
        try:            
            self.engine.SendStateAsync( 'Init_Err' ) 
            self.tabWidget.setCurrentIndex(self.page_normal)
            self.tabWidget.setTabEnabled(self.page_factory,False) 
            self.tabWidget.setTabEnabled(self.page_normal,True) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
        
        
        
    def OnClickPbFactory(self):
        try:            
            self.engine.SendStateAsync( 'Factory' ) 
            self.tabWidget.setCurrentIndex(self.page_factory)
            self.tabWidget.setTabEnabled(self.page_factory,True) 
            self.tabWidget.setTabEnabled(self.page_normal,False) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def OnSwitchStateChange(self):
        if self.engine.statemachine.st_remote == 'Factory':
            print "xx"
            
    def OnDialPadsliderMoved(self,value):        
        self.lcdNumber.display(self.dial_pad.value())
        
    def OnDialsliderReleased(self):
        print "OnDialsliderReleased value:" +  str(self.dial_pad.value() )
        self.lcdNumber.display(self.dial_pad.value())
        
    def OnhorizontalScrollBar_1_sliderMoved(self,value):
        self.progressBar_1.setValue( self.horizontalScrollBar_1.value() )
        self.lineEdit_1.setText( str(self.horizontalScrollBar_1.value()) )
        
    def OnhorizontalScrollBar_1_sliderReleased(self):
        self.progressBar_1.setValue( self.horizontalScrollBar_1.value() )
        self.lineEdit_1.setText( str(self.horizontalScrollBar_1.value()) )
        
    def OnhorizontalScrollBar_2_sliderMoved(self,value):
        self.progressBar_2.setValue( self.horizontalScrollBar_2.value() )
        self.lineEdit_2.setText( str(self.horizontalScrollBar_2.value()) )
        
    def OnhorizontalScrollBar_2_sliderReleased(self):
        self.progressBar_2.setValue( self.horizontalScrollBar_2.value() )
        self.lineEdit_2.setText( str(self.horizontalScrollBar_2.value()) )
        
    def OnhorizontalScrollBar_3_sliderMoved(self,value):
        self.progressBar_3.setValue( self.horizontalScrollBar_3.value() )
        self.lineEdit_3.setText( str(self.horizontalScrollBar_3.value()) )
        
    def OnhorizontalScrollBar_3_sliderReleased(self):
        self.progressBar_3.setValue( self.horizontalScrollBar_3.value() )
        self.lineEdit_3.setText( str(self.horizontalScrollBar_3.value()) )
        
    def OnhorizontalScrollBar_4_sliderMoved(self,value):
        self.progressBar_4.setValue( self.horizontalScrollBar_4.value() )
        self.lineEdit_4.setText( str(self.horizontalScrollBar_4.value()) )
        
    def OnhorizontalScrollBar_4_sliderReleased(self):
        self.progressBar_4.setValue( self.horizontalScrollBar_4.value() )
        self.lineEdit_4.setText( str(self.horizontalScrollBar_4.value()) )
        
    def OnClickPbAutotest(self):
        try:            
            pass
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    
    def OnClickPbSolutionSetting(self):
        try:            
            dlg = Solution_Mrg()   
            dlg.exec_()     
            self.SolutionParamSet = dlg.GetSolutionParamSet()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    
    def OnClickPbSend(self):
        try:
            self.engine.SendCfgData(self.SolutionParamSet)
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    
    
    
    
    def OnClickPbAction1(self):
        try:            
            self.progressBar_1.setValue( int(self.lineEdit_1.text() ) )
            self.horizontalScrollBar_1.setValue( int(self.lineEdit_1.text() ) )
            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    
    def OnClickPbAction2(self):
        try:            
            self.progressBar_2.setValue( int(self.lineEdit_2.text() ) )
            self.horizontalScrollBar_2.setValue( int(self.lineEdit_2.text() ) )
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    
    def OnClickPbAction3(self):
        try:            
            self.progressBar_3.setValue( int(self.lineEdit_3.text() ) )
            self.horizontalScrollBar_3.setValue( int(self.lineEdit_3.text() ) )
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def OnClickPbAction4(self):
        try:            
            self.progressBar_4.setValue( int(self.lineEdit_4.text() ) )
            self.horizontalScrollBar_4.setValue( int(self.lineEdit_4.text() ) )
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
   
   
    def OnClickPbExport(self):
        try:            
            pass
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
            
    
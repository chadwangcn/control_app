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

UI_PATH = "../res/ui/"
UI_MAIN_WIN = "main_beta.ui"  

MODULE_TAG = "main_beta_ui"

class main_beta( QtGui.QDialog  ):
    class transfer_worker(threading.Thread):            
            def __init__(self,_parent):
                '''
                Constructor
                '''
                self._parent = _parent
                self.bExit = False              
                threading.Thread.__init__(self)          
                self.rwlock = threading.RLock() #
                
            def start_async(self):
                self.start()
            
            def stop_async(self):
                self.bExit = True
                
                
            def run(self):
                while self.bExit == False:  
                    self.rwlock.acquire()
                    try:
                        self._parent.engine.SendCfgData(self._parent.SolutionParamSet) 
                        self._parent.OnTransferCancel()
                        self._parent.IsSendRunning = False 
                    except Exception,e:
                        print Exception,":",e
                        traceback.print_exc()
                    self.rwlock.release()
                    
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
        self.bInitSucess = True
        self.Startup = datetime.datetime.now() 
        self.bStartup = False
        self.job = None
        self.UIDataDb = {}
        self.bindUI()
        
        if self.build_engine() == False:
            self.bInitSucess = False 
        self.ui_rwlock = threading.RLock() #
        
    def closeEvent (self, _event):
        print "closeEvent"
        super( main_beta, self ).closeEvent(_event)
        self.OnQuit()
        
    def OnQuit(self):
        self.stop_engine()
        
    def bindUI(self):        
        self.label_state.setText('开机.. 等待下位机复位')
        self.SetLabelColor(self.label_state,"background-color:green")
        
        self.label_info.setText('系统启动中')
        self.SetLabelColor(self.label_info,"background-color:green")
        
        self.label_ex0tmp.setText('0')
        self.label_ex1tmp.setText('0')
        self.label_ex2tmp.setText('0')
        self.label_main.setText('0')
        self.label_fid.setText('0')
        self.label_tcd.setText('0')
        
        label_color = QColor(255, 122, 30, 127)
        
        self.SetLabelBgColor(self.label_ex0tmp,label_color)
        self.SetLabelBgColor(self.label_ex1tmp,label_color)
        self.SetLabelBgColor(self.label_ex2tmp,label_color)
        self.SetLabelBgColor(self.label_main,label_color)
        self.SetLabelBgColor(self.label_fid,label_color)
        self.SetLabelBgColor(self.label_tcd,label_color)
        
        '''
        self.SetLabelColor(self.label_ex0tmp,label_color)
        self.SetLabelColor(self.label_ex1tmp,label_color)
        self.SetLabelColor(self.label_ex2tmp,label_color)
        self.SetLabelColor(self.label_main,label_color)
        self.SetLabelColor(self.label_fid,label_color)
        self.SetLabelColor(self.label_tcd,label_color)'''
        
        
        'bind pb button'
        self.connect( self.pb_halt,QtCore.SIGNAL("clicked()"),self.OnClickPbHalt)
        self.connect( self.pb_autotest,QtCore.SIGNAL("clicked()"),self.OnClickPbAutotest)
        self.connect( self.pb_solution_setting,QtCore.SIGNAL("clicked()"),self.OnClickPbSolutionSetting)
        self.connect( self.pb_send,QtCore.SIGNAL("clicked()"),self.OnClickPbSend)        
        self.connect( self.pb_run,QtCore.SIGNAL("clicked()"),self.OnClickPbRun)
        
        self.connect( self.pb_ready,QtCore.SIGNAL("clicked()"),self.OnClickPbReady)
        self.connect( self.pb_Warmming,QtCore.SIGNAL("clicked()"),self.OnClickPbWarmming)
        
        
        self.connect( self.pb_stop,QtCore.SIGNAL("clicked()"),self.OnClickPbStop)
        self.connect( self.pb_action_1,QtCore.SIGNAL("clicked()"),self.OnClickPbAction1)
        self.connect( self.pb_action_2,QtCore.SIGNAL("clicked()"),self.OnClickPbAction2)
        self.connect( self.pb_action_3,QtCore.SIGNAL("clicked()"),self.OnClickPbAction3)
        self.connect( self.pb_action_4,QtCore.SIGNAL("clicked()"),self.OnClickPbAction4)
        self.connect( self.pb_export,QtCore.SIGNAL("clicked()"),self.OnClickPbExport)
        self.connect( self.pb_factory,QtCore.SIGNAL("clicked()"),self.OnClickPbFactory)
        self.connect( self.pb_auto,QtCore.SIGNAL("clicked()"),self.OnClickPbAuto)
        
        self.connect( self.pb_dump,QtCore.SIGNAL("clicked()"),self.OnClickPbDump)
        
        
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
        
        self.IsSendRunning = False 
        
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
    
    def build_engine(self):
        try:
            self.build_period_task_pool = period_task_pool()
            self.build_period_task_pool.addTask("timeout_check",self.update_ui,1)
            self.engine = engine_controller()
            self.engine.prepare_engine(self.OnNotifyMsg)
            self.engine.start_engine()    
            self.build_period_task_pool.startPool()
            return True
        except Exception,e:
            print "error here "
            print Exception,":",e
            traceback.print_exc()
            return False 
    
    def stop_engine(self):
        try:
            self.build_period_task_pool.stopPool()
            self.engine.stop_engine() 
            self.build_period_task_pool= None 
            self.engine = None            
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
    
    def SetLabelBgColor(self,_label,_color):    
        ft = QFont()
        ft.setPointSize(18)
        _label.setFont(ft)
        pe = QPalette()          
        pe.setBrush(QPalette.Base,QBrush(_color));        
        pe.setColor(QPalette.WindowText,Qt.black)
        _label.setPalette(pe)
        
    def update_ui(self):       
        self.emit(SIGNAL("UpdateUI") )    
   
    def OnUpdateUI(self):
        if None == self.engine:
            return
        
        if self.engine.bTimeOut:
            self.label_state.setText('通讯错误')
            self.SetLabelColor(self.label_state,"background-color:red")
            self.label_info.setText('请检查网络连接...')
            self.SetLabelColor(self.label_info,"background-color:red")
        elif self.bInitSucess == False:            
            self.SetLabelColor(self.label_state,"background-color:red")
            self.label_info.setText('启动失败')
            self.SetLabelColor(self.label_info,"background-color:red")
        elif self.bStartup == False:
            if (datetime.datetime.now() - self.Startup).seconds > 4:
                self.bStartup = True      
            self.label_state.setText('系统启动中')          
            self.SetLabelColor(self.label_state,"background-color:green")
            self.label_info.setText('')
            self.SetLabelColor(self.label_info,"background-color:green")
        else:
            self.SetLabelColor(self.label_state,"background-color:green")
            self.label_info.setText('系统正常运行中...')
            self.SetLabelColor(self.label_info,"background-color:green")
            self.OnUpdateUI_Data()
            
    
    def OnUpdateUI_Data(self):
        
        self.ui_rwlock.acquire()
        try:
            for(key,value) in self.UIDataDb.items():
                if key == "Door":
                    self.lcdNumber.display(int(value))
                elif key == "Valve":
                    self.UpdateSwStatue( int(value) )
                elif key == "Ex0T":
                    self.label_ex0tmp.setText(str(value))
                elif key == "Ex1T":
                    self.label_ex1tmp.setText( str(value) )
                elif key == "Ex2T":
                    self.label_ex2tmp.setText(str(value))
                elif key == "MainT":
                    self.label_main.setText(str(value))
                elif key == "Ex0C":
                    self.progressBar_1.setValue (int(value))
                elif key == "Ex1C":
                    self.progressBar_2.setValue (int(value))
                elif key == "Ex2C":
                    self.progressBar_3.setValue (int(value))
                elif key == "MainC":
                    self.progressBar_4.setValue (int(value))
            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
              
        self.ui_rwlock.release()
                 
    def UpdateSwStatue(self,data):
        try:
            if  (data & 0b01) == 0b01:
                self.sw_1.setChecked(True)
                self.checkBoxSw1.setChecked(True)
            else:
                self.sw_1.setChecked(False)
                self.checkBoxSw1.setChecked(False)
                
            if  (data & 0b10) == 0b10:
                self.sw_2.setChecked(True)
                self.checkBoxSw2.setChecked(True)
            else:
                self.sw_2.setChecked(False)
                self.checkBoxSw2.setChecked(False)
                
            if  (data & 0b100) == 0b100:
                self.sw_3.setChecked(True)
                self.checkBoxSw3.setChecked(True)
            else:
                self.sw_3.setChecked(False)
                self.checkBoxSw3.setChecked(False)
                
            if  (data & 0b1000) == 0b1000:
                self.sw_4.setChecked(True)
                self.checkBoxSw4.setChecked(True)
            else:
                self.sw_4.setChecked(False)
                self.checkBoxSw4.setChecked(False)
                
            if  (data & 0b10000) == 0b10000:
                self.sw_5.setChecked(True)
                self.checkBoxSw5.setChecked(True)
            else:
                self.sw_5.setChecked(False)
                self.checkBoxSw5.setChecked(False)
                
            if  (data & 0b100000) == 0b100000:
                self.sw_6.setChecked(True)
                self.checkBoxSw6.setChecked(True)
            else:
                self.sw_6.setChecked(False)
                self.checkBoxSw6.setChecked(False)
                
            if  (data & 0b1000000) == 0b1000000:
                self.sw_7.setChecked(True)
                self.checkBoxSw7.setChecked(True)
            else:
                self.sw_7.setChecked(False)
                self.checkBoxSw7.setChecked(False)
                
            if  (data & 0b10000000) == 0b10000000:
                self.sw_8.setChecked(True)
                self.checkBoxSw8.setChecked(True)
            else:
                self.sw_8.setChecked(False)
                self.checkBoxSw8.setChecked(False)
                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
        
        
    
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
                
                if _msg[1] == "Init_OK":
                    print "Board Initial sucess,auto -> config state"
                    self.OnClickPbAutoCfg()
                    
                if _msg[1] == "Auto_Ready":
                    self.pb_Warmming.setEnabled(True)
                else:
                    self.pb_Warmming.setEnabled(False)
                    
                
                if _msg[1] == "Auto_Warmming":
                    pass
                
                if _msg[1] == "Auto_WarmUp":
                    self.pb_run.setEnabled(True)
                else:
                    self.pb_run.setEnabled(False)
                
                
                
            elif _msg[0] == "timeout":
                self.hasTimeOut = True
                self.emit(SIGNAL("TimeOut") )   
            elif _msg[0] == "transfer_percent":
                self.transfer_percent = _msg[1]
            else:
                self.OnConsumeOtherMsg(_msg)
                 
            self.emit(SIGNAL("UpdateUI") )                          
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
    
    def OnConsumeOtherMsg(self,_msg): 
        ''''      
         _tag_list= ["Ex0C","Ex1C","Ex2C","MainC","MainT",
                    "Ex0T","Ex1T","Ex2T","Door","Valve"]
            
        '''
        try:
            self.ui_rwlock.acquire()
            self.UIDataDb[ _msg[0] ] =  _msg[1]
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
        self.ui_rwlock.release()
                
        
    def OnClickPbAutoCfg(self):
        try:            
            self.engine.SendStateAsync( 'Auto_Config' ) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def OnClickPbReady(self):
        try:            
            self.engine.SendStateAsync( 'Auto_Ready' ) 
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
    
    def OnClickPbWarmming(self):
        try:            
            self.engine.SendStateAsync( 'Auto_Warmming' ) 
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
            self.engine.SystemHalt()
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()
              
    def OnClickPbDump(self):
        try:
            self.SolutionParamSet.dump()
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
            print "OnFactory: sw status change"
            pass
            
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
            self.OnTransferCfgToBoard()            
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
            
    '''
    progress dialog bar for data transfer   
    
    '''
            
    def InitProgressBarDialog(self):
        self.progress_bar = QProgressDialog("Operation in progress.", "Cancel", 0, 100);
        self.connect(self.progress_bar, QtCore.SIGNAL("canceled()") ,self.OnTransferCancel );
        self.transfer_t = QTimer()
        self.connect(self.transfer_t, QtCore.SIGNAL("timeout()") ,self.OnUpDateTransferPercent );
        self.transfer_percent = 0
        
   
        
    def OnTransferCancel(self):
        print "Cancel transfer"
        if self.job != None:
            self.job.stop_async()
            self.job = None
            
        "elf.transfer_t.stop()"     
        self.IsSendRunning = False  
        self.progress_bar.reject()
        '''
         clean the task
        '''
        
    def OnTransferOk(self):
        pass
    
    def OnUpDateTransferPercent(self):
        try:
            self.progress_bar.setValue( self.transfer_percent)
            if self.transfer_percent >=100:
                self.transfer_t.stop()
               
            
            self.transfer_t.setInterval(100)
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            
    def StartTransferPercent(self):        
        self.InitProgressBarDialog()
        self.setWindowModality(Qt.WindowModal);
        self.progress_bar.setWindowTitle("方法传输进度")        
        self.progress_bar.setLabelText("传输中")
        self.progress_bar.setCancelButtonText("取消传输")
        self.progress_bar.setRange(0,100)
        self.transfer_t.start(1)        
        self.progress_bar.show()
       
        
    def OnTransferCfgToBoard(self):        
        try:
            if self.IsSendRunning == False:
                print "Begin send"
                self.IsSendRunning = True
                self.StartTransferPercent()
                self.TransferThread()                
            else:
                print "Running, Not need to run again"
        except Exception,e:
            if self.IsSendRunning == True:
                self.IsSendRunning = False
            print Exception,":",e
            traceback.print_exc() 
            
    def TransferThread(self):
        self.job =  self.transfer_worker(self)       
        self.job.start_async()
                   
       
        
 

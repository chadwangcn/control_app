#coding=utf-8

import traceback
import threading
import time
import datetime
from socket import *
from engine import DataCenter
from engine import cfg_data
from engine import db_data
from engine import async_event
from engine.PacketFactory import *
from data_source import Logtrace
from data_source  import UdpMonitor
from data_source  import UartMonitor
from data_source import RecorderCenter
'from data_consume.UdpDataProcess import *'
from engine import st_engine
from engine import UdpSender
from engine.crc import *
from app  import SolutionParamSet
from engine.period_task_pool import *

EngineHost = None

def GetEngineContrllerInstance():
    if None == EngineHost:
        EngineHost = engine_controller()    
    return EngineHost

def task1():
    print "No.1 " +str(datetime.datetime.now())
    
def task2():
    print "No.2 " +str(datetime.datetime.now())
    
def task3():
    print "No.3 " +str(datetime.datetime.now())


class engine_controller(DataCenter.BaseDataConsume):
    '''
    main engine controller
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.bExit = False
        self.state_cnt = 0
        DataCenter.BaseDataConsume.__init__(self)
        
        self.statemachine = st_engine.St_Engine()    
        self.register_handle("UnKnow",self.On_UnKonw)    
        self.register_handle("Init_Err", self.On_Init_Err)
        self.register_handle("Init_OK", self.On_Init_OK)
        self.register_handle("Factory", self.On_Factory)
        self.register_handle("Auto_Config", self.On_Auto_Config)
        self.register_handle("Auto_Ready", self.On_Auto_Ready)        
        self.register_handle("Auto_Warmming", self.On_Auto_Warmming)
        self.register_handle("Auto_WarmUp", self.On_Auto_WarmUp)
        self.register_handle("Auto_Running", self.On_Auto_Running)
        self.register_handle("Auto_End", self.On_Auto_End) 
        
        
        self.async_event_q = async_event.async_event()     
        
        self.sync_handle_table = {  "Mode":self.Sync_Mode,\
                                    "Value":self.Sync_Value,
                                    "Ex0C":self.Sync_Ex,
                                    "Ex1C":self.Sync_Ex,
                                    "Ex2C":self.Sync_Ex,
                                    "Door":self.Sync_Door }   
               
        self.DataCenter = None
        self.udp_src = None
        self.udp_send= None
        self.ui_cb = None
        self.PacketFactory = None
        
        self.cfg_method = None
        self.cfg_db = db_data.db_data()
        self.remote_db = db_data.db_data()            
        self.bTimeOut = False
        
        
        self.db_rwlock = threading.RLock()
        self.first_system_tick = datetime.datetime.now()  
        
        self.current_system_tick = datetime.datetime.now() 
        self.last_system_tick = datetime.datetime.now() 
       
        
        self.current_remote_tick = 0
        self.last_remote_tick = 0
        
        self.build_period_task_pool = period_task_pool()        
        self.build_period_task_pool.addTask("sync_data",self.task_sync_data,1)
        self.build_period_task_pool.addTask("tick",self.task_tick_sync2remote,2)
        self.build_period_task_pool.addTask("task_timeout_check",self.task_timeout_check,2)
        
    def test_task(self):
        print "self.calss"
      
    def prepare_engine(self,_cb):
        try:
            self.ui_cb = _cb
            self.PacketFactory = PacketFactory()
            self.Center = DataCenter.DataCenter()
            
            'log trace'
            
            self.udp_src_log = UdpMonitor.UdpMonitor(1400,"0.0.0.0")                 
            self.Center.Register("networklogtrace", self.udp_src_log)  
            
            'udp hw_maincontroller'        
            self.udp_src = UdpMonitor.UdpMonitor(3000,"192.168.11.5")                 
            self.Center.Register("hw_maincontroller", self.udp_src)
                        
            self.log_record = RecorderCenter.RecorderCenter("d://log","System_Log",10*1024*1024)            
            self.Center.Subcribe("networklogtrace", "networklogtrace", self.log_record.fillData)
            
            
            self.Center.Subcribe("hw_maincontroller", "local_consumer_udp", self._data_callback)  
                  
            self.udp_send = UdpSender.UdpSender(15000,"192.168.11.4")
            self.udp_send.start_network()
            
            self.first_system_tick = datetime.datetime.now() 
            '''
            object_uart =UartMonitor.UartMonitor("/dev/ttyUSB0",115200)        
            self.Center.Register("UartMonitor", object_uart)   
            
            RecObject= RecorderCenter.RecorderCenter("/home/lijun/ts/tmp","Uart",1024*1024)
            self.Center.Subcribe("UartMonitor", "No.3", RecObject.fillData)    '''
                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
            
    def period_check(self):
        pass
       
    
        
    def start_engine(self):
        self.bExit = False         
        self.StartBase()      
        self.Center.Start() 
        self.async_event_q.start_async()        
        self.build_period_task_pool.startPool()
        
    def stop_engine(self):
        self.bExit = True        
        self.StopBase()
        self.async_event_q.stop_async()
        self.Center.Stop()       
        self.build_period_task_pool.stopPool()  
        
    def register_handle(self, _state,_handle):
        try:
            self.statemachine.register_process(_state,_handle)            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def NotifySubcribeData(self):
        '''
        Notify data to UI 
        '''
        _tag_list= ["Ex0C","Ex1C","Ex2C","MainC","MainT",
                    "Ex0T","Ex1T","Ex2T","Door","Valve"]
        for _tag in _tag_list:
            [ret,value] = self.remote_db.get_key(_tag)        
            if True == ret and None != value:
                print(_tag+ " value:" +  str(value) )
                _msg = [_tag,value ] 
                self.NotifyMsg2UI(_msg)
            else:
                print(_tag+" not found") 
            
            
            
    def NotifyMsg2UI(self,_data):
        try:         
            self.ui_cb(_data)            
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
            
    def SystemHalt(self):
        print "system halt"
        'system halt sync state to init'
        self.udp_send.SendData(  self.PacketFactory.BuildModeSwitch(0))
            
    def SendStateCmd(self,_state,_expect_value):      
        self.statemachine.st_cur = _state
        self.Sync_Mode(self.statemachine.st_cur)
            
            
    def SendStateAsync(self,_state):       
        self.statemachine.st_cur = _state
        self.Sync_Mode(self.statemachine.st_cur)
            
    def SendStateSync(self,_state):
        if self.statemachine.st_remote != _state:
            self.statemachine.st_cur = _state
        else:
            return True
    
        bCheckCnt= 5
        bExit = False
        while bExit == False:
            time.sleep(2)
            if self.statemachine.st_remote != _state:
                bCheckCnt = bCheckCnt -1
            else:
                bExit =True
                break;
            
            if bCheckCnt < 0:
                bExit = True
                break;
            
        if self.statemachine.st_remote != _state:
            return False
        else:
            return True
        
    '''
    transfer the whole cfg data to the board
    '''
    def SendCfgData(self,_cfg_data): 
        print "---->"  
        _msg = ["transfer_percent",10 ] 
        self.NotifyMsg2UI(_msg)        
        
        if self.SendStateSync( 'Auto_Config' ) == False:
            return False 
        print "Sync Auto_Config OK"
        
        _msg = ["transfer_percent",20 ] 
        self.NotifyMsg2UI(_msg) 
        if self.SendSegmentData(_cfg_data) == False:
            return False
        print "SendSegmentData Ok"
        
        _msg = ["transfer_percent",60 ] 
        self.NotifyMsg2UI(_msg) 
        if self.SendAssitBoxData( _cfg_data ) == False:
            return False
        print "SendAssitBoxData OK"
       
    def SendAssitBoxData(self,_cfg_data): 
        ret_value = False
        method_data = _cfg_data
        retry_cnt = 2
        
        if method_data == None:
            print "cfg data is empty"
            return False
        
        while retry_cnt > 0 :                      
            retry_cnt = retry_cnt -1             
            _packet_msg = "Ex0T:" + hex( int(method_data.Temp1_AssistBox*10) )[2:] +\
                          ",Ex1T:" +hex( int(method_data.Temp2_AssistBox*10) )[2:] +\
                          ",Ex2T:"+ hex( int(method_data.Temp3_AssistBox*10) )[2:]
                          
          
            _event = async_event.event()
            _event.key_words = "Ex0T:"
            _event.expect_value = _packet_msg  
            _event.name = "assistboxdata"             
            self.async_event_q.add_event(_event)  
            
            self.udp_send.SendData(_packet_msg)
            time.sleep(3)
            event_status = self.async_event_q.get_event_status(_event.name) 
            if event_status == "ok":
                print "box ok"
                ret_value = True
                break;
            else:
                ret_value = False
                print "box error" +event_status
                continue
        return ret_value
            
    def buildCrc(self,_data):
        pass
    
    def SendSegmentData(self,_cfg_data):   
        ret_value = False
        method_data = _cfg_data
        retry_cnt = 2
        
        if method_data == None:
            print "cfg data is empty"
            return False
        print "send segment"
        while retry_cnt > 0 :
            _event = async_event.event()
            _event.key_words = "Crc"
            _event.expect_value = "xxx"   
            _event.name = "segment_cfg"             
            self.async_event_q.add_event(_event)            
            retry_cnt = retry_cnt -1
            max_cnt = 4
            cnt = 0
            
            if method_data.SegParamSet == None:
                print "segment tagble is empty"
                break
            
            crc_str =""            
            _packet_msg = "Ta_N:"+hex(len(method_data.SegParamSet))[2:]
            for k,seg_data in method_data.SegParamSet.iteritems(): 
                if _packet_msg == None:
                    _packet_msg = "Ts_"+str(k) + ":"+ hex( int(seg_data.start_temp*10) )[2:]   
                    crc_str = crc_str+"%08x"%( int(seg_data.start_temp*10) )
                else:
                    _packet_msg = _packet_msg +"," + "Ts_"+str(k) + ":"+ hex( int(seg_data.start_temp*10) )[2:]
                    crc_str = crc_str+"%08x"%( int(seg_data.start_temp*10)  )
                                 
                _packet_msg = _packet_msg+ ",Te_"+str(k) + ":"+ hex( int(seg_data.end_temp*10) )[2:]    
                crc_str = crc_str+"%08x"%( int(seg_data.end_temp*10)  )
                         
                _packet_msg = _packet_msg+ ",Sl_"+str(k) + ":"+ hex( int(seg_data.raise_time*10) )[2:]      
                crc_str = crc_str+"%08x"%( int(seg_data.raise_time*10)  )
                        
                _packet_msg = _packet_msg+ ",t_"+str(k) + ":"+ hex( int(seg_data.hold_time_h*60*60 +seg_data.hold_time_m*60 + seg_data.hold_time_s) )[2:] 
                crc_str = crc_str+"%08x"%( int(seg_data.hold_time_h*60*60 +seg_data.hold_time_m*60 + seg_data.hold_time_s)  )
                
                cnt = cnt+1                
                if cnt >= max_cnt:
                    self.udp_send.SendData(_packet_msg)
                    _packet_msg = None
                    cnt = 0       
           
            if _packet_msg != None:
                self.udp_send.SendData(_packet_msg)
                
            time.sleep(2)
            print "caculate_crc :" + crc_str
            [ status,crc_hex_value ] = caculate_crc(crc_str)
            print [ status,crc_hex_value ]            
            _event.expect_value = (crc_hex_value)[2:] 
            print "_event.expect_value:"+ str(_event.expect_value)
            event_status = self.async_event_q.get_event_status(_event.name) 
            if event_status == "ok" :
                print "send segment ok"
                ret_value = True
                break;
            else:
                print "send segment fail"
                ret_value = False
                continue
            
        return ret_value
    
    def send_tick(self):
        system_delta= datetime.datetime.now() - self.first_system_tick
        'print "-------------> HeartBeat update  now: "  +  str( datetime.datetime.now() ) + " - " + str(self.first_system_tick) + " = " + str(system_delta)'
        _packet_msg = "Tick:" + hex( int(system_delta.total_seconds()) )  
        
        if None != self.udp_send:
            self.udp_send.SendData(_packet_msg)    
       
    def Sync_Mode(self,_state):
        [ret,str_value] = self.statemachine.st_strtovalue(_state)        
        if True == ret:
            self.udp_send.SendData(  self.PacketFactory.BuildModeSwitch(str_value ))
            
    def Sync_Value(self,_value):
        pass
    
    def Sync_Ex(self,_value):
        pass
        
    def Sync_Door(self,_value):
        pass   
            
    def SyncData(self):
        if  self.statemachine.st_remote != "UnKnow" and\
            self.statemachine.st_cur    != "UnKnow" and\
            self.statemachine.st_remote != self.statemachine.st_cur:                        
            self.Sync_Mode(self.statemachine.st_cur)
            
        iterms = ["Value","Door","Ex0C","Ex1C","Ex2C"];
        
        for iterm in iterms:
            try:
                [ret_remote,value_remote] = self.remote_db.get_key(iterm)
                [ret_local, value_local] = self.cfg_db.get_key(iterm)
                if True == ret_local and value_remote != value_local :
                    handle = self.sync_handle_table.get(iterm)           
                    if None != handle:
                        handle(value_local)  
            except Exception,e:
                print Exception,":",e
                traceback.print_exc()
                
    def task_sync_data(self):
        try:
            self.SyncData()
        except Exception,e:
                print Exception,":",e
                traceback.print_exc() 
                
    def task_tick_sync2remote(self):
        try:
            self.send_tick() 
        except Exception,e:
                print Exception,":",e
                traceback.print_exc() 
    
    def task_timeout_check(self):
        self.OnTimeOutCheck()
        try:
            if self.bTimeOut == True:                    
                _msg = ["timeout",None ] 
                self.NotifyMsg2UI(_msg)  
        except Exception,e:
                print Exception,":",e
                traceback.print_exc()   
    '''
            超时检测
    '''
    def OnTimeOutCheck(self):
        
        self.db_rwlock.acquire()
                
        self.current_system_tick = datetime.datetime.now()          
        systime_delta = self.current_system_tick - self.last_system_tick
        
        ' remote system time unit: 10ms '
        remote_delta = (self.current_remote_tick - self.last_remote_tick)/100
        
        
        delta = int(systime_delta.total_seconds()) - remote_delta
        if delta > 5:
            self.bTimeOut = True
        else:
            self.bTimeOut = False
        
        print "sys   -----> " + str(self.current_system_tick) + " - " + str( self.last_system_tick) + " = " + str(systime_delta.seconds)
        print "remote-----> " + str(self.current_remote_tick) + " - " + str(self.last_remote_tick)  + " = " +str( remote_delta )
        print "-----------> " + str(delta)   
        self.db_rwlock.release()
            
        
        
                
    def OnCommonCheck(self):
        try:
            [ret,value] = self.remote_db.get_key("Tick")  
            
            self.db_rwlock.acquire()
            
            self.db_rwlock.release()
            if True == ret:
                tick = int(value)
                if self.current_remote_tick <= 0 and tick >=0 :
                    self.last_remote_tick = tick
                    self.current_remote_tick = tick
                else:
                    self.last_remote_tick = self.current_remote_tick
                    self.current_remote_tick = tick
                    self.last_system_tick = datetime.datetime.now()
                    
        except Exception,e:
                print Exception,":",e
                traceback.print_exc()
                self.db_rwlock.release()
        
            
    def On_UnKonw(self,_data):
        print "On_UnKonw --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)
        
        if False == ret:
            return
        
        self.remote_db.update_value_dict(key_value)  
        self.OnCommonCheck()       
        self.NotifySubcribeData()  
        [ret,value] = self.remote_db.get_key("Mode")
        
        if False == ret:
            return        
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)  
        if ret == True:
            self.statemachine.st_remote = str_value
            self.statemachine.change_state(str_value)
            
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
           
    def On_Init_Err(self,_data):
        print "On_Init_Err --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)
        
        if False == ret:
            return
        
        self.remote_db.update_value_dict(key_value)    
        self.OnCommonCheck()       
        self.NotifySubcribeData()
        [ret,value] = self.remote_db.get_key("Mode")   
        
        if False == ret:
            return         
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if   self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)        
      
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
         

    def On_Init_OK(self,_data):
        print "On_Init_OK --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        
        self.remote_db.update_value_dict(key_value)
        self.OnCommonCheck()
        self.NotifySubcribeData()
        [ret,value] = self.remote_db.get_key("Mode")   
        if False == ret:
            return         
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
        
        if value <= 0x00000001 and self.statemachine.st_cur == "Init_Err" :
            self.statemachine.st_cur = self.statemachine.st_remote 
        elif self.statemachine.st_remote != self.statemachine.st_cur:  
            self.Sync_Mode(self.statemachine.st_cur)
              
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
        
        
    def On_Factory(self,_data):
        print "On_Factory --> "+ _data
        self.async_event_q.update_event(_data)
        
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        self.remote_db.update_value_dict(key_value)  
        self.OnCommonCheck()    
        self.NotifySubcribeData()  
        [ret,value] = self.remote_db.get_key("Mode")   
        if ret == False: 
            print "Factory  xxx"
            return 
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)
                
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
        
    
    def On_Auto_Config(self,_data):
        print "On_Auto_Config --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        
        self.remote_db.update_value_dict(key_value)  
        self.OnCommonCheck()  
        self.NotifySubcribeData()
        [ret,value] = self.remote_db.get_key("Mode")   
        if ret == False: 
            return 
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if   self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)
        
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
        
    def On_Auto_Ready(self,_data):
        print "On_Auto_Ready --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        self.remote_db.update_value_dict(key_value) 
        self.OnCommonCheck() 
        self.NotifySubcribeData() 
        [ret,value] = self.remote_db.get_key("Mode")   
        if ret == False: 
            return 
                
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if   self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)
        
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
    
    def On_Auto_Warmming(self,_data):
        print "On_Auto_Warmming --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        self.remote_db.update_value_dict(key_value) 
        self.OnCommonCheck()  
        self.NotifySubcribeData() 
        [ret,value] = self.remote_db.get_key("Mode")   
        if ret == False: 
            return 
                
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if   self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)
            
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
            
        
    def On_Auto_WarmUp(self,_data):
        print "On_Auto_WarmUp --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        self.remote_db.update_value_dict(key_value)  
        self.OnCommonCheck()  
        self.NotifySubcribeData()
        
        self.statemachine.change_state("Auto_Running") 
        self.Sync_Mode(self.statemachine.st_cur)    
        
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
    
    def On_Auto_Running(self,_data):
        print "On_Auto_Running --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        self.remote_db.update_value_dict(key_value) 
        self.OnCommonCheck()  
        self.NotifySubcribeData()
        [ret,value] = self.remote_db.get_key("Mode")   
        if ret == False: 
            return  
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if   self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)      
      
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
    
    def On_Auto_End(self,_data):
        print "On_Auto_End --> "+ _data
        self.async_event_q.update_event(_data)
        [ret, key_value] = DataCenter.cvs_parse(_data)        
        if False == ret:
            return        
        self.remote_db.update_value_dict(key_value)  
        self.OnCommonCheck()  
        self.NotifySubcribeData()
        
        [ret,value] = self.remote_db.get_key("Mode")   
        if ret == False: 
            return          
        
        [ret,str_value] = self.statemachine.st_valuetostr(value)       
        if ret == True:
            self.statemachine.st_remote = str_value
            
        if   self.statemachine.st_remote != self.statemachine.st_cur:            
            self.Sync_Mode(self.statemachine.st_cur)    
            
        _msg = ["machine_mode",self.statemachine.st_remote ] 
        self.NotifyMsg2UI(_msg)
        
    
    def _data_callback(self, _udpData):
        '''
        will receive data from DataCenter
        1. push the data to the queue
        2. return
        '''
        
        'lock the data queue'               
        DataCenter.BaseDataConsume._data_callback(self, _udpData)        
        'unlock the data queue'
        
    
    def Process(self,_data):
        '''
        will Process the data
        '''
        
        'lock the data queue'
        ' pop the data '        
        'unlock the data queue'
        'process the data'
        try:
            self.statemachine.process(_data)
        except Exception,e:
            print Exception,":",e
            traceback.print_exc()  
               
 

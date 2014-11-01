#coding=utf-8
import xml.dom.minidom
from xml.dom.minidom import parse
from  datetime  import  *  
import  time 
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
import traceback
import threading 
import os 

class SegParam(object):
    def __init__(self):
        self.segid = 0
        self.start_temp = 0.00
        self.end_temp = 0.00
        self.raise_time = 0.00
        self.hold_time_h = 0
        self.hold_time_m = 0 
        self.hold_time_s = 0
            
class SwitchParam(object):
    def __init__(self,param):
        self.switch_name = param
        self.param_id = 0 
        self.timestamp = 0  
        self.action = ""   # close/open
        

class SolutionParamSet(object):
    '''
    
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        '''
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))  '''
        self.uniqueid = ""
        self.filepath = ""
        self.filename= ""
        self.previousState = ""
        self.currentState = ""
        self.action = ""
        
        self.mainctrltype = 0
        self.hasFID = False
        self.hasTCD = False 
        self.hasGasBox = False
        self.hasAssistantTemp = False
        self.hasSwitchCtrl = False
        
        '''
            
        '''
        self.Temp_TCD = 0.0
        self.MaxTemp_TCD = 0.0 
        self.LoadGas_TCD = ""
        self.BridgeCur_TCD = 0.0 
        self.ZoomCoin_TCD  = 0
        self.Polar_TCD = ""
        
        '''
         
        '''
        self.Temp_FID = 0.0 
        self.MaxTemp_FID = 0.0 
        self.Range_FID = 0.0
        
        '''
          
        '''
        self.Temp_GasBox = 0.0 
        self.MaxTemp_GasBox = 0.0
        
        '''
       
        '''
        self.Temp1_AssistBox = 0.0 
        self.Temp2_AssistBox = 0.0 
        self.Temp3_AssistBox = 0.0
        
        '''
    
        '''
        self.Temp_Const = 0.0 
        self.Time_Const = 0.0
        
        '''
   
        '''
    
        self.InitalTemp = 0.0
        self.InitalHoldTime = 0.0
        self.ReHeatTimes = 1
        self.SegParamSet = {}
        
        '''
     
        '''
        self.SwitchParamSet = {}

    def dump(self):       
        try:
            
            print 'mainctrl:' + "type_"+ str(self.mainctrltype) +\
            " InitalTemp_"+ str( self.InitalTemp ) +\
            " InitalHoldTime_"+ str( self.InitalHoldTime) 
            
            if self.mainctrltype == 0:
                print 'const:' +\
                'Temp_Const_'+str(self.Temp_Const) +\
                'Time_Const_'+str(self.Time_Const)
        
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            
    
    def SaveCfg(self,_fileName=None):
        ret_value = True
        try:
            if _fileName == None:
                _fileName =os.path.join( self.filepath , self.filename )
            else:
                _fileName = _fileName  
              
            impl = xml.dom.minidom.getDOMImplementation()
            dom = impl.createDocument(None, "method_cfg_db", None)
            root = dom.documentElement     
            root.setAttribute("author", "unknow" )
            
            main_item = dom.createElement('mainctrl')
            main_item.setAttribute("type", str(self.mainctrltype) )
            main_item.setAttribute("InitalTemp",str( self.InitalTemp ) )
            main_item.setAttribute("InitalHoldTime",str( self.InitalHoldTime) )
            root.appendChild(main_item)
            
            if self.mainctrltype == 0:
                child_item = dom.createElement('const')    
                child_item.setAttribute('Temp_Const',str(self.Temp_Const))
                child_item.setAttribute('Time_Const',str(self.Time_Const))
                root.appendChild(child_item)
            elif self.mainctrltype == 1:
                child_item = dom.createElement('segment')    
                child_item.setAttribute('segment_cnt',str(len(self.SegParamSet) ))
                for k,seg_data in self.SegParamSet.iteritems(): 
                    '''key_str = "segment_"+str(k) '''
                    key_str = "segment_value" 
                    segment_item = dom.createElement( key_str )
                    segment_item.setAttribute( "id", str(k)  )  
                    segment_item.setAttribute( "start_temp", str(seg_data.start_temp)  )  
                    segment_item.setAttribute( "end_temp", str(seg_data.end_temp)  )  
                    segment_item.setAttribute( "raise_time", str(seg_data.raise_time)  )  
                    segment_item.setAttribute( "hold_time_h", str(seg_data.hold_time_h)  )  
                    segment_item.setAttribute( "hold_time_m", str(seg_data.hold_time_m)  ) 
                    segment_item.setAttribute( "hold_time_s", str(seg_data.hold_time_s)  )  
                    child_item.appendChild(segment_item)                
                    
                root.appendChild(child_item)
            elif  self.mainctrltype == 2:
                child_item = dom.createElement('resegment')                    
                child_item.setAttribute('ReHeatTimes',str(self.ReHeatTimes))
                child_item.setAttribute('segment_cnt',str(len(self.SegParamSet) ))
                for k,seg_data in self.SegParamSet.iteritems():                     
                    key_str = "segment_value"
                    segment_item = dom.createElement( key_str )
                    segment_item.setAttribute( "id", str(seg_data.segid)  )  
                    segment_item.setAttribute( "start_temp", str(seg_data.start_temp)  )  
                    segment_item.setAttribute( "end_temp", str(seg_data.end_temp)  )  
                    segment_item.setAttribute( "raise_time", str(seg_data.raise_time)  )  
                    segment_item.setAttribute( "hold_time_h", str(seg_data.hold_time_h)  )  
                    segment_item.setAttribute( "hold_time_m", str(seg_data.hold_time_m)  ) 
                    segment_item.setAttribute( "hold_time_s", str(seg_data.hold_time_s)  )  
                    child_item.appendChild(segment_item)               
                
                root.appendChild(child_item)
                            
            if self.hasTCD:            
                tcd_item = dom.createElement('TCD')    
                tcd_item.setAttribute("Temp_TCD",str(self.Temp_TCD))       
                tcd_item.setAttribute("MaxTemp_TCD",str(self.MaxTemp_TCD))       
                tcd_item.setAttribute("LoadGas_TCD",str(self.LoadGas_TCD))   
                tcd_item.setAttribute("BridgeCur_TCD",str(self.BridgeCur_TCD))   
                tcd_item.setAttribute("ZoomCoin_TCD",str(self.ZoomCoin_TCD))   
                tcd_item.setAttribute("Polar_TCD",str(self.Polar_TCD))       
                root.appendChild(tcd_item)
                
            if self.hasFID:
                fid_item = dom.createElement('FID')    
                fid_item.setAttribute("Temp_FID",str(self.Temp_FID))       
                fid_item.setAttribute("MaxTemp_FID",str(self.MaxTemp_FID))       
                fid_item.setAttribute("Range_FID",str(self.Range_FID))               
                root.appendChild(fid_item)
                
            if self.hasAssistantTemp:
                Assist_item = dom.createElement('AssistBox')    
                Assist_item.setAttribute("Temp1_AssistBox",str(self.Temp1_AssistBox))       
                Assist_item.setAttribute("Temp2_AssistBox",str(self.Temp2_AssistBox))          
                Assist_item.setAttribute("Temp3_AssistBox",str(self.Temp3_AssistBox))          
                root.appendChild(Assist_item)
                
            if self.hasGasBox:
                GasBox_item = dom.createElement('GasBox')    
                GasBox_item.setAttribute("Temp_GasBox",str(self.Temp_GasBox))       
                GasBox_item.setAttribute("MaxTemp_GasBox",str(self.MaxTemp_GasBox))      
                root.appendChild(GasBox_item)
                
            if self.hasSwitchCtrl:
                switch_item = dom.createElement('SwitchCtrl')   
                switch_item.setAttribute("number", str(len(self.SwitchParamSet)))
                root.appendChild(switch_item) 
            
            print root.toprettyxml()
            print dom.toprettyxml()
            
            '''
            _file_path = os.path.dirname(_fileName)
            if os.path.exists(_file_path) == False:
                os.mkdir(_file_path)
               '''
             
            stream = open(_fileName, 'w')  
            dom.writexml( stream,addindent='  ', newl='\n',encoding='utf-8')            
            stream.close()  
            print "save ok :" + _fileName
                
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            ret_value = False
        
        return ret_value
    
    def ReadCfg(self,_fileName):
        bRet = True
        try:
            input = open(_fileName,'r')
            doc = parse(input)
            print doc.toxml()
            root = doc.documentElement
            item_child = root.getElementsByTagName("mainctrl")[0]     
            self.mainctrltype =  int(item_child.getAttribute('type'))
            self.InitalTemp = float( item_child.getAttribute('InitalTemp') )
            self.InitalHoldTime = float( item_child.getAttribute('InitalHoldTime') )
            
            if self.mainctrltype == 0:
                item_child = root.getElementsByTagName("const")[0]   
                self.Temp_Const = float( item_child.getAttribute('Temp_Const') )  
                self.Time_Const = float( item_child.getAttribute('Time_Const') )                  
            elif self.mainctrltype == 1:                
                item_child = root.getElementsByTagName("segment")[0]   
                segment_cnt = int( item_child.getAttribute('segment_cnt') )  
                item_childs = item_child.getElementsByTagName("segment_value")
                
                self.SegParamSet.clear()
                for item_segment  in item_childs:  
                    seg_data = SegParam()
                    seg_data.segid = int( item_segment.getAttribute( "id" ) )
                    seg_data.start_temp = float( item_segment.getAttribute( "start_temp" ) )
                    seg_data.end_temp = float( item_segment.getAttribute( "end_temp" ) )
                    seg_data.raise_time = float( item_segment.getAttribute( "raise_time" ) )
                    seg_data.hold_time_h = int( item_segment.getAttribute( "hold_time_h" ) )
                    seg_data.hold_time_m = int( item_segment.getAttribute( "hold_time_m" ) )
                    seg_data.hold_time_s = int( item_segment.getAttribute( "hold_time_s" ) )
                    self.SegParamSet[seg_data.segid] = seg_data
                                                 
                    
                if segment_cnt != len(self.SegParamSet) :
                    bRet = False
                    raise Exception("segment cnt", "error")    
               
            elif  self.mainctrltype == 2:
                item_child = root.getElementsByTagName("resegment")[0]   
                self.ReHeatTimes = int( item_child.getAttribute('ReHeatTimes') )  
                segment_cnt = int( item_child.getAttribute('segment_cnt') )  
                item_childs = item_child.getElementsByTagName("segment_value")   
                self.SegParamSet.clear()
                for item_segment  in item_childs:  
                    seg_data = SegParam()
                    seg_data.segid = int( item_segment.getAttribute( "id" ) )
                    seg_data.start_temp = float( item_segment.getAttribute( "start_temp" ) )
                    seg_data.end_temp = float( item_segment.getAttribute( "end_temp" ) )
                    seg_data.raise_time = float( item_segment.getAttribute( "raise_time" ) )
                    seg_data.hold_time_h = int( item_segment.getAttribute( "hold_time_h" ) )
                    seg_data.hold_time_m = int( item_segment.getAttribute( "hold_time_m" ) )
                    seg_data.hold_time_s = int( item_segment.getAttribute( "hold_time_s" ) )
                    self.SegParamSet[seg_data.segid] = seg_data                                                 
                    
                if segment_cnt != len( len(self.SegParamSet) ):
                    bRet = False
                    raise Exception("segment cnt", "error") 
            
            item_child = root.getElementsByTagName("TCD")            
            if len(item_child) == 1:
                self.Temp_TCD = float( item_child[0].getAttribute('Temp_TCD') )  
                self.MaxTemp_TCD = float( item_child[0].getAttribute('MaxTemp_TCD') )  
                self.LoadGas_TCD =  item_child[0].getAttribute('LoadGas_TCD')   
                self.BridgeCur_TCD = float( item_child[0].getAttribute('BridgeCur_TCD') )  
                self.ZoomCoin_TCD = float( item_child[0].getAttribute('ZoomCoin_TCD') )  
                self.Polar_TCD = item_child[0].getAttribute('Polar_TCD') 
                self.hasTCD = True
            
            item_child = root.getElementsByTagName("FID")
            if len(item_child) == 1:
                self.Temp_FID = float( item_child[0].getAttribute('Temp_FID') )  
                self.MaxTemp_FID = float( item_child[0].getAttribute('MaxTemp_FID') )  
                self.Range_FID = float( item_child[0].getAttribute('Range_FID') ) 
                self.hasFID = True
            
            item_child = root.getElementsByTagName("AssistBox")
            if len(item_child) == 1:
                self.Temp1_AssistBox = float( item_child[0].getAttribute('Temp1_AssistBox') )  
                self.Temp2_AssistBox = float( item_child[0].getAttribute('Temp2_AssistBox') )  
                self.Temp3_AssistBox = float( item_child[0].getAttribute('Temp3_AssistBox') )  
                self.hasAssistantTemp = True
                
            item_child = root.getElementsByTagName("GasBox")
            if len(item_child) == 1:
                self.Temp_GasBox = float( item_child[0].getAttribute('Temp_GasBox') )  
                self.MaxTemp_GasBox = float( item_child[0].getAttribute('MaxTemp_GasBox') )                  
                self.hasGasBox = True
              
        except Exception,e:
            print Exception,":",e
            traceback.print_exc() 
            bRet = False
        
        return bRet
        
'''
    

if __name__ == "__main__":
    value_set = SolutionParamSet()
    
    value_set.hasTCD = True
    value_set.Temp_TCD = 20 
    value_set.SaveCfg("d:/demo.xnl") 
    value_set.ReadCfg("D:\\chad\project\\ControlSwPortal\\Beta1.1\\project_app\\control_app\\appdemo.jxc")
    value_set.SaveCfg("D:\\chad\project\\ControlSwPortal\\Beta1.1\\project_app\\control_app\\appdemo2.jxc")
    
    '''
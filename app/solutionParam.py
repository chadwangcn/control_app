#coding=utf-8

import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic
import traceback 

UI_PATH = "../res/ui/"
UI_MAIN_WIN = "solutionParam.ui"  

class solutionParam(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self,param):
        '''
        Constructor
        '''
        super( solutionParam, self ).__init__()
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8")) 
        self.dlg = uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.SolutionParamSet = param
        self.SolutionParamSet.currentState = "solutionparam"
        self.bindUI()
        self.load_data()
        pass
    
        
    def bindUI(self):
        self.connect( self.dlg.pbPrevious,QtCore.SIGNAL('clicked()'), self.OnPrevious )
        self.connect( self.dlg.pbNext,QtCore.SIGNAL('clicked()'), self.OnNext )
     
        pass
    
    def load_data(self):
        self.DisablePage()
        if self.SolutionParamSet.hasTCD:
                self.dlg.Temp_TCD.setValue( self.SolutionParamSet.Temp_TCD )
                self.dlg.MaxTemp_TCD.setValue( self.SolutionParamSet.MaxTemp_TCD )
                self.dlg.BridgeCur_TCD.setValue( self.SolutionParamSet.BridgeCur_TCD )
              
            
        if self.SolutionParamSet.hasFID:
            self.dlg.Temp_FID.setValue( self.SolutionParamSet.Temp_FID )
            self.dlg.MaxTemp_FID.setValue( self.SolutionParamSet.MaxTemp_FID )       
            #self.SolutionParamSet.Range_FID = self.dlg.Range_FID.value()
                
         
        if self.SolutionParamSet.hasGasBox:
            self.dlg.Temp_GasBox.setValue( self.SolutionParamSet.Temp_GasBox )
            self.dlg.MaxTemp_GasBox.setValue( self.SolutionParamSet.MaxTemp_GasBox )
       
        
        if self.SolutionParamSet.hasAssistantTemp:
            self.dlg.Temp1_assistBox.setValue( self.SolutionParamSet.Temp1_AssistBox )
            self.dlg.Temp2_assistBox.setValue( self.SolutionParamSet.Temp2_AssistBox )
            self.dlg.Temp3_assistBox.setValue( self.SolutionParamSet.Temp3_AssistBox )
           
    
    def OnPrevious(self):
        print "OnPrevious"
        [ret,status] = self.OnCheckValue()
        self.SolutionParamSet.action = "previous"
        self.accept()
        pass
    
    def OnNext(self):
        print "OnNext"
        [ret,status] = self.OnCheckValue()
        self.SolutionParamSet.action = "next"
        self.accept()
    
    def OnOk(self):
        pass
    
    def OnCancel(self):
        pass
    
    def DisablePage(self):
        index = self.dlg.toolBox.indexOf(self.dlg.page_fid)
        if self.SolutionParamSet.hasFID == False:            
            self.dlg.toolBox.setItemEnabled (index,False)
            self.dlg.toolBox.setItemText(index,self.dlg.toolBox.itemText(index)+ " unCheck" )
        else:
            self.dlg.toolBox.setCurrentIndex(index)
            
        index = self.dlg.toolBox.indexOf(self.dlg.page_tcd)
        if self.SolutionParamSet.hasTCD == False:            
            self.dlg.toolBox.setItemEnabled (index,False)
            self.dlg.toolBox.setItemText(index,self.dlg.toolBox.itemText(index)+ " unCheck" )
        else:
            self.dlg.toolBox.setCurrentIndex(index)
            
        index = self.dlg.toolBox.indexOf(self.dlg.page_gasbox)
        if self.SolutionParamSet.hasGasBox == False:            
            self.dlg.toolBox.setItemEnabled (index,False)
            self.dlg.toolBox.setItemText(index,self.dlg.toolBox.itemText(index)+ " unCheck" )
        else:
            self.dlg.toolBox.setCurrentIndex(index)
        
        index = self.dlg.toolBox.indexOf(self.dlg.page_extenion)
        if self.SolutionParamSet.hasAssistantTemp == False:            
            self.dlg.toolBox.setItemEnabled (index,False)
            self.dlg.toolBox.setItemText(index,self.dlg.toolBox.itemText(index)+ " unCheck" )
        else:
            self.dlg.toolBox.setCurrentIndex(index)
        
        index = self.dlg.toolBox.indexOf(self.dlg.page_const)
        if self.SolutionParamSet.mainctrltype != 0:
            self.dlg.toolBox.setItemEnabled (index,False)
            self.dlg.toolBox.setItemText(index," " )
            
        
            
    def OnCheckValue(self):
        ret = True
        status = ""
        try:
            '''
             self.Temp_TCD = 0.0
            self.MaxTemp_TCD = 0.0 
            self.LoadGas_TCD = ""
            self.BridgeCur_TCD = 0.0 
            self.ZoomCoin_TCD  = 0
            self.Polar_TCD = ""
        
            '''
            if self.SolutionParamSet.hasTCD:
                self.SolutionParamSet.Temp_TCD = self.dlg.Temp_TCD.value()
                self.SolutionParamSet.MaxTemp_TCD = self.dlg.MaxTemp_TCD.value()
                self.SolutionParamSet.BridgeCur_TCD = self.dlg.BridgeCur_TCD.value()
               
            '''
            self.Temp_FID = 0.0 
            self.MaxTemp_FID = 0.0 
            self.Range_FID = 0.0
            '''
            if self.SolutionParamSet.hasFID:
                self.SolutionParamSet.Temp_FID = self.dlg.Temp_FID.value()
                self.SolutionParamSet.MaxTemp_FID = self.dlg.MaxTemp_FID.value()
                #self.SolutionParamSet.Range_FID = self.dlg.Range_FID.value()
                
            '''
            self.Temp_GasBox = 0.0 
            self.MaxTemp_GasBox = 0.0
            '''
            if self.SolutionParamSet.hasGasBox:
                self.SolutionParamSet.Temp_GasBox = self.dlg.Temp_GasBox.value()
                self.SolutionParamSet.MaxTemp_GasBox = self.dlg.MaxTemp_GasBox.value()
            
            '''
            self.Temp1_AssistBox = 0.0 
            self.Temp2_AssistBox = 0.0 
            self.Temp3_assistBox = 0.0
            
            '''
            if self.SolutionParamSet.hasAssistantTemp:
                
                self.SolutionParamSet.Temp1_AssistBox = self.dlg.Temp1_assistBox.value()
                self.SolutionParamSet.Temp2_AssistBox = self.dlg.Temp2_assistBox.value()
                self.SolutionParamSet.Temp3_AssistBox = self.dlg.Temp3_assistBox.value()
                
                print "Temp1_AssistBox "  + str(self.SolutionParamSet.Temp1_AssistBox)
                print "Temp2_AssistBox "  + str(self.SolutionParamSet.Temp2_AssistBox)
                print "Temp3_AssistBox "  + str(self.SolutionParamSet.Temp3_AssistBox)
                
            print "H:" + str(self.dlg.Temp_Const_h.value()) + \
                  "M:"+ str(self.dlg.Temp_Const_m.value())  + \
                  "S:"+ str(self.dlg.Temp_Const_s.value())
            
            self.SolutionParamSet.Temp_Const = self.dlg.Temp_Const.value()
            self.SolutionParamSet.Time_Const = int(self.dlg.Temp_Const_h.value() ) *60*60 + \
                                               int(self.dlg.Temp_Const_m.value() ) *60 +\
                                               int(self.dlg.Temp_Const_s.value() ) 
                                               
            
                        
        except Exception,e:
            traceback.print_exc()   
            ret = False
            status = "Get UI Data Error"
        return [ret,status]
    
    def GetSolutionParamSet(self):
        return self.SolutionParamSet
            
            
            
           
    
    
    
        
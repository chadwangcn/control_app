#coding=utf-8

import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic
from app  import SolutionParamSet

UI_PATH = "../res/ui/"
UI_MAIN_WIN = "segment_setting.ui"   

class segment_object:
    def __init__( self ):
        self.index_tableview = 0
        self.start_temp = 0.00
        self.end_temp = 0.00
        self.raise_time = 0.00
        self.hold_time_h = 0
        self.hold_time_m = 0 
        self.hold_time_s = 0
        self.id = 0
        pass
 
class SegmentSetting( QtGui.QDialog ):
    def __init__( self,param ):
        super( SegmentSetting, self ).__init__()
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("GB2312"))
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8")) 
        self.dlg = uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.SolutionParamSet = param
        self.SolutionParamSet.currentState = "segmentsetting"
        
        self.setWindowTitle(self.tr("segment"))  
        self.tableViewModel = None
        
        self.tableViewModel = QStandardItemModel();
        self.tableViewModel.setColumnCount(4);
        self.tableViewModel.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant("start"))
        self.tableViewModel.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant("end"))
        self.tableViewModel.setHeaderData(2, QtCore.Qt.Horizontal, QtCore.QVariant("raise"))
        self.tableViewModel.setHeaderData(3, QtCore.Qt.Horizontal, QtCore.QVariant("hold"))        
        
        # read only
        self.tViewSegment.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.tViewSegment.setSelectionBehavior(QTableWidget.SelectRows) 
        self.tViewSegment.setSelectionMode(QTableWidget.SingleSelection)   
        
        self.dlg.tViewSegment.setModel(self.tableViewModel);
        ' self.dlg.tViewSegment.horizontalHeader().setDefaultAlignment(Qt::AlignLeft);'
        
        self.seg_cnt = 0
        self.segmentdata = {}
        
        self.bindUI()
        self.load_data()
        self.emit(SIGNAL("RefreshUIData") )
        
    def bindUI(self):
        self.connect(self.dlg.pbtAdd,QtCore.SIGNAL("clicked()"),self.OnAdd)
        self.connect(self.dlg.pbtAdd,QtCore.SIGNAL("clicked()"),self.OnCheck)        
        self.connect(self.dlg.pbtDel,QtCore.SIGNAL("clicked()"),self.OnDel)        
        self.connect(self.dlg.pbtModify,QtCore.SIGNAL("clicked()"),self.OnModify)
        self.connect(self.dlg.pbtModify,QtCore.SIGNAL("clicked()"),self.OnCheck)        
        self.connect(self.dlg.pbtExit,QtCore.SIGNAL("clicked()"),self.OnExit)        
        self.connect(self, QtCore.SIGNAL("RefreshUIData"),self.OnRefreshUIData )
        
        if self.SolutionParamSet.mainctrltype != 2:
            self.dlg.label_repeat.setVisible(False)
            self.dlg.repeat_cnt.setVisible(False)
        pass
        
    def load_data(self):
        #load data from system       
   
        for k,data in self.segmentdata.iteritems():
            print k
            print data
            try:                
                self.tableViewModel.setItem( data.id, 0, QStandardItem( QtCore.QString.number(data.start_temp) ) )
                self.tableViewModel.setItem( data.id, 1, QStandardItem( QtCore.QString.number(data.end_temp) ) )
                self.tableViewModel.setItem( data.id, 2, QStandardItem( QtCore.QString.number(data.raise_time) ) )
                self.tableViewModel.setItem( data.id, 3, QStandardItem( QtCore.QString.number(data.hold_time) ) )  
            except:
                pass
        
        pass
    
    def CheckAllInputData(self):
        return True
       
        f_value = self.dlg.start_temp.value()           
        if f_value <= 10.0 or f_value > 410.0:
            return False
            
               
        f_value = self.dlg.end_temp.value()
        if f_value <= 10.0 or f_value > 410.0:
            return False
        
        f_value = self.dlg.raise_time.value()
        if f_value <= 0.0 or f_value > 500:
            return False
        
        f_value = self.dlg.hold_time.value()
        if f_value <= 10.0 or f_value > 500:
            return False
        
        return True
    
    def OnCheck(self):
        pass
        
    
    def OnAdd(self):
        if self.CheckAllInputData():            
            new_data = segment_object()
            new_data.id = self.seg_cnt
            new_data.start_temp = self.dlg.start_temp.value()     
            new_data.end_temp = self.dlg.end_temp.value()
            new_data.raise_time = self.dlg.raise_time.value()
            
            hold_date = self.dlg.hold_time.dateTime ()  
            new_data.hold_time_h = hold_date.time().hour()
            new_data.hold_time_m = hold_date.time().minute()
            new_data.hold_time_s = hold_date.time().second()
            
            self.segmentdata[  self.seg_cnt ] = new_data   
            self.seg_cnt = self.seg_cnt + 1
            self.emit(SIGNAL("RefreshUIData") )
        else:
            pass
          
    def OnDel(self):        
        current_row =self.dlg.tViewSegment.selectedIndexes()
        bFound = False
        FoundKey = 0
        for index in current_row:                               
            for k,data in self.segmentdata.iteritems():  
                if data.index_show == index.row() :
                    bFound = True
                    data.start_temp = 0.00
                    data.end_temp = 0.00
                    data.raise_time = 0.00
                    data.hold_time = 0.00
                    FoundKey = data.id
                    self.segmentdata[FoundKey] = data
                    if bFound == True:                        
                        self.segmentdata.pop(data.id) 
                        self.emit(SIGNAL("RefreshUIData") )
                        return
   
    def OnModify(self):       
        if self.CheckAllInputData():
            current_row =self.dlg.tViewSegment.selectedIndexes()            
            for index in current_row:                               
                for k,data in self.segmentdata.iteritems():  
                    if data.index_show == index.row() :                       
                        data.start_temp = self.dlg.start_temp.value()     
                        data.end_temp = self.dlg.end_temp.value()
                        data.raise_time = self.dlg.raise_time.value()
                        
                        hold_date = self.dlg.hold_time.dateTime ()  
                        data.hold_time_h = hold_date.time().hour()
                        data.hold_time_m = hold_date.time().minute()
                        data.hold_time_s = hold_date.time().second()
                        self.segmentdata[data.id] = data
                        self.emit(SIGNAL("RefreshUIData") )
                        return        
    
    def OnExit(self): 
        self.CopyData() 
        self.accept()
        
    
    def CopyData(self):        
        for k,data in self.segmentdata.iteritems():  
            segment = SolutionParamSet.SegParam()
            segment.segid = data.id
            segment.start_temp = data.start_temp
            segment.end_temp = data.end_temp
            segment.raise_time = data.raise_time
            segment.hold_time_h = data.hold_time_h
            segment.hold_time_m = data.hold_time_m
            segment.hold_time_s = data.hold_time_s
            print "segid:" + str(segment.segid) + " start_temp" +  str(data.start_temp)
            self.SolutionParamSet.SegParamSet[segment.segid] = segment

    def OnRefreshUIData(self):
        print "OnRefreshUIData"
        self.tableViewModel.clear()
        self.tableViewModel.setColumnCount(4);
        self.tableViewModel.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant("start"))
        self.tableViewModel.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant("end"))
        self.tableViewModel.setHeaderData(2, QtCore.Qt.Horizontal, QtCore.QVariant("raise"))
        self.tableViewModel.setHeaderData(3, QtCore.Qt.Horizontal, QtCore.QVariant("hold"))
        index = 0
        for k,data in self.segmentdata.iteritems():            
            try:                
                data.index_show = index
                hold_time = str(data.hold_time_h) +":"+str(data.hold_time_m)+":"+str(data.hold_time_s) 
                
                self.tableViewModel.setItem( index, 0, QStandardItem( QtCore.QString.number(data.start_temp) ) )
                self.tableViewModel.setItem( index, 1, QStandardItem( QtCore.QString.number(data.end_temp) ) )
                self.tableViewModel.setItem( index, 2, QStandardItem( QtCore.QString.number(data.raise_time) ) )
                self.tableViewModel.setItem( index, 3, QStandardItem( hold_time ) )  
                
                self.segmentdata[  data.id ] = data  
                index = index+1
            except Exception,e:
                print e                
                
    def GetSolutionParamSet(self):
        return self.SolutionParamSet
            
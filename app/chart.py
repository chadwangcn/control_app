#coding=utf-8

import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic


UI_PATH = "../res/ui/"
UI_MAIN_WIN = "graphic.ui"   

class chart(QtGui.QWidget):
    '''
    classdocs
    '''

    def __init__(self, width,height,param):
        '''
        Constructor
        '''
        super( chart, self ).__init__()
        self.dlg= uic.loadUi( UI_PATH+UI_MAIN_WIN, self )
        self.canvas = self.dlg.frame
        
        self.bindUI()
        self.loadData()
       
        self.setAutoFillBackground(True);
        self.palette = QtGui.QPalette()
        self.palette.setColor(QtGui.QPalette.Background, QColor(192,253,123));    
        self.setPalette(self.palette);
        
    
    
    def bindUI(self):
        self.connect(self,QtCore.SIGNAL("sizeChange()"),self.updatewinsize)
     
        pass
    
    def updatewinsize(self):
        print "SizeChange"
        self.canvas.setGeometry(0,0,self.width(),self.height())
        
    def loadData(self):
        pass
    
    def changeBgColor(self, event, qp):          
        self.palette.setColor(QtGui.QPalette.Background, QColor(255, 0, 0, 127));         
        self.setPalette(self.palette);
        pass
      
    
    def drawCoordinates(self, event, qp):
       # width =self.width()
      #  height = self.height()
        
        step_w = self.width()/self.dlg.spinBoxW.value()
        step_h = self.height()/self.dlg.spinBoxH.value()
        print "w="+str(self.width() ) + " h="+ str(self.height() )+" step=" + str(step_w)
        
        pen = qp.pen()
        
        pen.setStyle(Qt.SolidLine);
        pen.setWidthF(1)
        qp.setPen(pen)
        
        " 绘制竖直方向  "
        for n in range(1,step_w):
            if n == 1 or n == step_w-1:
                pen.setStyle(Qt.SolidLine)
                qp.setPen(pen)
            else:
                pen.setStyle(Qt.DashLine)
                qp.setPen(pen)                
            qp.drawLine( 10, 20*n,self.height()*0.8,20*n)
            
        " 绘制水平方向  "
        for n in range(1,step_h):
            if n == 1 or n == step_h-1:
                pen.setStyle(Qt.SolidLine)
                qp.setPen(pen)
            else:
                pen.setStyle(Qt.DashLine)
                qp.setPen(pen)                
            qp.drawLine( 20*n,10,20*n,self.width()*0.8)
        
       
        
        
    
    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        self.text = "www"
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)
    
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)               
        self.drawCoordinates(event, qp)  
        self.drawText(event, qp)        
        qp.end()
        print "Paint"
        
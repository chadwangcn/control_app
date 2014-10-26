#coding=utf-8

from chart import *
from mainui import *
from main_beta import *
import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import * 
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *

if __name__ == '__main__':    
    app=QApplication(sys.argv)  
    #dialog = chart(800,600,0)
    dialog=main_beta()  
    dialog.show()  
    app.exec_()  
    
    
    
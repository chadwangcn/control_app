'''
Created on Apr 22, 2014

@author: ljwang
'''
import traceback
import os  
import stat  
import time

class RecorderCenter(object):
    '''
    RecorderCenter will save all the data to disk
    '''
    def __init__(self,_curFolderPath, _objectName,_defualtFileSize):
        '''
        Constructor
        '''
        self.objectName = _objectName
        self.curFolderPath = _curFolderPath
        self.defualtFileSize = _defualtFileSize   
        self.fileHandle = ""
        self.curFileName = ""
    
    def Exit(self):
        if self.fileHandle != "" :
            try:                
                self.fileHandle.flush()
                self.fileHandle.close()
            except  IOError, e:
                print Exception,":",e
                traceback.print_exc()      
    
    def getRecorderFileName(self):
        try:
            nowTime = time.localtime()    
            year = str(nowTime.tm_year)    
            month = str(nowTime.tm_mon)
            day = str(nowTime.tm_mday)
            hour = str(nowTime.tm_hour)
            miniter = str(nowTime.tm_min)
            sec = str(nowTime.tm_sec)           
                            
            curPath = self.curFolderPath+"/"+self.objectName+"/"+ year+"-"+month+"-"+day
            if not os.path.exists(curPath):
                os.makedirs(curPath)                
            
            return curPath+"/"+year+"-"+month+"-"+day+"-"+hour+"-"+miniter+"-"+sec+".bin"
        except  IOError, e:
             print Exception,":",e
             traceback.print_exc() 
        return ""         
      
    
    def checkFileSize(self,_fileName):
        ret = True;        
        try:            
            fileStats = os.stat ( _fileName )  
            size = fileStats [ stat.ST_SIZE ]
            if  size > self.defualtFileSize :
                ret = True;
            else:
                ret = False
        except IOError, e:
            print Exception,":",e
            traceback.print_exc() 
            ret =  False;
        return ret;
    
    def fillData(self,_objectString):
        '''
        will add a buffer before save data to physical file
        '''
        return self.saveDataToFile(_objectString)
    
    def saveDataToFile(self,_objectString):
        ret = True;
        if self.fileHandle == "" :
            try:
                self.curFileName = self.getRecorderFileName()
                self.fileHandle = open(self.curFileName,'a+')
            except  IOError, e:
                print Exception,":",e
                traceback.print_exc()       
                ret = False
        else:
            if self.checkFileSize( self.curFileName )  :
                try:
                    self.fileHandle.flush()
                    self.fileHandle.close()
                    self.curFileName = self.getRecorderFileName()
                    self.fileHandle = open(self.curFileName,'a+')                    
                except  IOError, e:
                    print Exception,":",e
                    traceback.print_exc()       
                    ret = False
        
        try:
            self.fileHandle.write(_objectString)
            self.fileHandle.flush()
        except IOError, e:
            print Exception,":",e
            traceback.print_exc() 
            ret = False
        return ret
           
        
        
         
         
            
             
                
                 
                
            
            
            
        
        
    
    
    
    
    
    
        
    
    
        
        
        
        
        
        
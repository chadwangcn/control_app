#coding=utf-8

class cfg_data(object):
    '''
    
    '''
    def __init__(self):
        self.init_data()
        
    def init_data(self):
        self.method_name = ""
        self.filepath = ""        
        self.mode = ""
        
        self.inital_Tmp = 0 
        self.inital_holdtime = 0
        
        self.hasTCD = False
        self.TCD_Tmp = 0 
        self.TCD_MaxTmp = 0 
        self.TCD_LoadGas = ""
        self.TCD_BridgeCur = 0
        
        self.hasFID = False
        self.FID_Tmp = 0
        self.FID_MaxTmp = 0
        self.FIDRange= 0
        
        self.hasAssitBox = False
        self.AssitBox1 = 0
        self.AssitBox2 = 0 
        self.AssitBox3 = 0
        
        
        
        self.hasGasbox = False
        self.Gasbox_Tmp = 0 
        self.Gasbox_MaxTmp = 0
        
        
        self.hasSwitchCtrl = False
        self.SwitchCtrlData = []
        
        self.HasLoopCtrl = False
        self.LoopCtrlCnt = 0
        
        ' construction '
        self.const_tmp = 0.0
        
        ' segment'
        self.segment_data = []  
        
    def validcheck(self):
        pass   
    
    def save(self, _filePath):
        pass
    
    def read(self, _filePath):
        pass
    
    
        
'''
Created on Apr 22, 2014

@author: ljwang
'''
import unittest
from engine.RecorderCenter import *

class Test(unittest.TestCase):


    def setUp(self):
        self.testObject = RecorderCenter.RecorderCenter("d:/video","uart",10*1024*1024)
        pass


    def tearDown(self):
        self.testObject.Exit()
        pass
        
    def testDirName(self):
        i= 200000;
        while i>0:
            self.testObject.saveDataToFile("tshiissddddddddddddddddddddddddddddddddddd")
            i= i -1
                    
        pass
    
    def testFileName(self):
        pass

    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
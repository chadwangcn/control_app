'''
Created on Jul 4, 2014

@author: lijun
'''
import unittest
from data_consume.cvs_parse import *

class Test(unittest.TestCase):


    def setUp(self):
        self.cvs = cvs_comsumer()

    def tearDown(self):
        pass


    def testReadLocalCvsFile(self):        
        self.cvs.load_file("/home/lijun/demo_cvs.csv")
   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
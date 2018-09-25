import unittest
import os
import pandas as pd
from generateMatrix import *


#Checks if two objects are dataframes with the same information
def equalDF(df1, df2):
    if (isinstance(df1, pd.DataFrame) and
        isinstance(df2, pd.DataFrame)):
        return df1.equals(df2)
    else:
        raise TypeError('Must compare two dataframes')

class TestAdjMatrixTranslator(unittest.TestCase):

    scriptDir = os.path.dirname(__file__)
    relPath = "testGenerateMatrixFiles/"
    
    #values for testing
    dictionaryTests = [{"":[]},
                       {"user1":["user2","user3","user4"], 
                        "user2":["user1","user3"],
                        "user3":["user4"]},
                       {"user1":["user2"], 
                        "user2":["user1"]},
                       {"user1":["user3","user2"], 
                        "user2":["user1","user3"],
                        "user3":["user1","user2"]},
                       {"user1":["user2","user3","user4","user5"], 
                        "user2":["user1","user3","user4","user5"],
                        "user3":["user1","user2","user4","user5"],
                        "user4":["user1","user2","user3","user5"],
                        "user5":["user1","user2","user3","user4"]}
                       ]
    
    testFiles = ["test0.txt", "test1.txt", "test2.txt", "test3.txt", "test4.txt"]
    checkFiles = ["check0.csv", "check1.csv", "check2.csv", "check3.csv", "check4.csv"]
    
    initialFiles = ["testGroup1.txt"]
    initialMatrices = ["emptyMatrixGroup1.csv"]
    
    def testParse(self):
        for i in range(len(self.testFiles)):
            test = os.path.join(self.scriptDir, self.relPath + self.testFiles[i])
            self.assertTrue(parse(test) == self.dictionaryTests[i])
    
    def testInitialize(self):        
        for i in range(len(self.initialMatrices)):
            test = os.path.join(self.scriptDir, self.relPath + self.initialFiles[i])
            check = os.path.join(self.scriptDir, self.relPath + self.initialMatrices[i])
            self.assertTrue(equalDF(initializeMatrix(test), pd.read_csv(check, header=0, index_col=0))) 
    
    def testFillDF(self):       
        for i in range(len(self.checkFiles)):
            testMatrix = initializeMatrix(os.path.join(self.scriptDir, self.relPath + self.initialFiles[0]))
            testDict = self.dictionaryTests[i]
            check = os.path.join(self.scriptDir, self.relPath + self.checkFiles[i])
            self.assertTrue(equalDF(fillDF(testMatrix, testDict), pd.read_csv(check, header=0, index_col=0)))
            

unittest.main()








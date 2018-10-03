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
    checkSymmetricFiles = ["check0.csv", "check1.csv", "check2.csv", "check3.csv", "check4.csv"]
    checkDirectionalFiles = ["d_check0.csv", "d_check1.csv", "d_check2.csv", "d_check3.csv", "d_check4.csv"]
    
    initialFiles = ["testGroup1.txt"]
    initialMatrices = ["emptyMatrixGroup1.csv"]
    
    def test_parse(self):
        for i in range(len(self.testFiles)):
            test = os.path.join(self.scriptDir, self.relPath + self.testFiles[i])
            self.assertTrue(parse(test) == self.dictionaryTests[i])
    
    def test_initialize(self):        
        for i in range(len(self.initialMatrices)):
            test = os.path.join(self.scriptDir, self.relPath + self.initialFiles[i])
            check = os.path.join(self.scriptDir, self.relPath + self.initialMatrices[i])
            self.assertTrue(equalDF(initializeMatrix(test), pd.read_csv(check, header=0, index_col=0))) 
    
    def test_fill_symmetric_df(self):       
        files = self.checkSymmetricFiles
        for i in range(len(files)):
            testMatrix = initializeMatrix(os.path.join(self.scriptDir, self.relPath + self.initialFiles[0]))
            testDict = self.dictionaryTests[i]
            check = os.path.join(self.scriptDir, self.relPath + files[i])
            self.assertTrue(equalDF(fillDF(testMatrix, testDict), pd.read_csv(check, header=0, index_col=0)))
            
    def test_fill_directional_df(self): 
        files = self.checkDirectionalFiles
        for i in range(len(files)):
            testMatrix = initializeMatrix(os.path.join(self.scriptDir, self.relPath + self.initialFiles[0]))
            testDict = self.dictionaryTests[i]
            check = os.path.join(self.scriptDir, self.relPath + files[i])
            self.assertTrue(equalDF(fillDF(testMatrix, testDict, directional=True), pd.read_csv(check, header=0, index_col=0)))
    
    def test_initialize_from_names_list(self):
        check = os.path.join(self.scriptDir, self.relPath + self.initialMatrices[0])
        names = ["user1", "user2", "user3", "user4", "user5"]
        self.assertTrue(equalDF(initializeMatrix(names), pd.read_csv(check, header=0, index_col=0)))

unittest.main()








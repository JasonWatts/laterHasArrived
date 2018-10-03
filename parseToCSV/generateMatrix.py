#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 13:10:43 2018

@author: Kyle Hansen and Jared Wilkens
"""

import pandas as pd
import re

def parse(file):
    #opens file that has the saved responses from the survey
    #file must be in same directory as this python file
    intermediateFile = open(file)
    
    #creates an empty dictionary that will save the responses in the intermeidate file 
    #responses will be saved in the format {a : list b} where a is the name of the responder or survey taker,
    #and the list b is the list of names that make up the response of person a
    intermediateNames = {}
    
    #loops through, input file cleans each line that constitues an atmoic response of a single survey taker,
    #and saves the result in the dictionary intermediateNames
    for line in intermediateFile:
        #passes line of text into the string responseRaw
        responseRaw = line
        #removes all spaces in responseRaw
        responseRaw = responseRaw.replace(" ", "")
        #removes line break token in responseRAw
        responseRaw = responseRaw.strip("\n")
        #breaks string on ',' and ':' into different elements saving each of these broken elements in responseList
        responseList = re.split(',|:', responseRaw)
    
    
        #populates dictionary according to proper format 
        #places responder as the key of the dictionary
        responder = responseList.pop(0)
        #places the list of names, or response of the survey, as the value in the dictionary
        intermediateNames.update({responder : responseList})
    
    #closes previously opend input file 
    intermediateFile.close()
    return intermediateNames

def initializeMatrix(names):
    """
    Turn a list of names separated by '\n' into an empty adjacency matrix
    
    Parameters
    ----------
    names : .txt or list
        a text file of names separated by '\n' 
        OR
        a list of names

    Returns
    -------
    pandas.DataFrame
        an adjacency matrix populated by 0's
    
    """
    
    #open txt file and separate names into list
    if not isinstance(names, list):
        with open(names) as f:
            content = f.readlines()
    else:
        content = names
    #Sanitize data of \n and spaces (currently spaces removal is commented out)
    content = [x.strip('\n') for x in content]
    #content = [x.replace(" ","") for x in content]
    
    #crete empty pandas dataframe
    df = pd.DataFrame(0, index=content, columns=content)
    return df
    
def fillDF(df, intermediateNames, directional=False):
    """
    Fill dataframe df with information from intermediateNames.
    
    fillDF creates an adjacency matrix corresponding to intermediateNames
    where a 1 in a cell indicates that two people are related in some manner.
    The matrix is symmetric, and does not represent direction
    
    
    Parameters
    ----------
    df : pandas.DataFrame
        a dataframe with the initial values as column and row names
        which will be filled as the adjacency matrix
        
    intermediateNames : dict
        a dictionary relating one name to a list of names
        
    Returns
    -------
    pandas.DataFrame
        an adjacency matrix showing the relationships in intermediateNames
        
    """
    
    #iterate through dictionary names
    for keyName, value in intermediateNames.items():
        for valueName in value:
            #set both cells to 1 which show the relation between each name 
            df.at[keyName, valueName] = 1
            if not directional:
                df.at[valueName, keyName] = 1

    return df
    
    
def makeCSV(df, file_path):
    """
    Saves a csv file with the given adjacency matrix
    
    Parameters
    ----------
    df : pandas.DataFrame
        an adjacency matrix
        
    filePath : string
        a .csv file name
        
    Returns
    -------
    null
    
    """
    if (file_path[-4:] == '.csv'):
        df.to_csv(file_path)
    else:
        raise Exception("File name must be of type '.csv'")
    

def run_all(names, intermediate_file, csv_path):
    parsed_file = parse(intermediate_file)
    empty_df1 = initializeMatrix(names)
    empty_df2 = empty_df1.copy()

    full_df = fillDF(empty_df1, parsed_file)
    makeCSV(full_df, csv_path)
    directional_df = fillDF(empty_df2, parsed_file, directional=True)
    makeCSV(directional_df, csv_path[:-4] + "_directional.csv")



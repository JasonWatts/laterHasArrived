#coding: utf8
#
# Defines and helper functions for dealing with the file structure of this project.
#

import os
from person_class import Person

NAME_FILE = "names.csv"
HOMEPAGE_TEMPLATE = "homepage.html"
SURVEY_TEMPLATE = "survey.html"
RESULTS_TEMPLATE = "results.html"
QUESTION_FILE = "questionname.txt"
OUT_FILE = "response.txt"
CSV_NAME = "adjacency.csv"
ADMIN_TEMPLATE = "adminpage.html"
CSV_DIRECTIONAL = "adjacency_directional.csv"

dir_path = os.path.dirname(os.path.realpath(__file__))
SURVEY_DIR = os.path.join(dir_path, "surveys") #I don't know why something that isn't a constant is being defined like it is a constant, but I'm not going to touch this while I'm splitting up files.

#Ensure the survey directory exists
if not os.path.exists(SURVEY_DIR):
    os.makedirs(SURVEY_DIR)

def read_names(filepath):
    csv = open(filepath)
    csv.readline()
    names = []
    participants = {}
    for line in csv:
        names.append(line.strip("\n"))
    csv.close()
    for i in range(len(names)):
        name_info = names[i].split(",")
        if len(name_info) == 4:
            person = Person(i, name_info[0], name_info[1], name_info[2], name_info[3])
        elif len(name_info) == 3:
            person = Person(i, name_info[0], name_info[1], name_info[2])
        else:
            person = Person(i, name_info[0], name_info[1])
        print(person)
        participants[person.id_num] = person

    all_names = set()
    duplicate_names = set()
    for key in participants:
        if participants[key].get_name() in all_names:
            duplicate_names.add(participants[key].get_name())
        all_names.add(participants[key].get_name())
    for key in participants:
        if participants[key].get_name() in duplicate_names:
            participants[key].set_duplicate()

    return participants


def GetQuestionNameFromTextFile(filepath):
    file = open(filepath, 'r')
    question = file.read()
    return question

def GetFormFromName(name, survey_folders, question_number):
    #print(name)
    folder_path = os.path.join(survey_folders, name)
    #print(folder_path)
    questionnamepath = os.path.join(folder_path, str(question_number) + QUESTION_FILE)
    #print(questionnamepath)
    inputfilepath = os.path.join(folder_path, NAME_FILE)
    #print(inputfilepath)
    intermediatefilepath = os.path.join(folder_path, str(question_number) + OUT_FILE)
    #print(intermediatefilepath)
    participants = read_names(inputfilepath)
    #print(nameslist)
    print(questionnamepath)
    questiontext = GetQuestionNameFromTextFile(questionnamepath)
    #print(questiontext)
    return questiontext, inputfilepath, participants, intermediatefilepath

def createSurveyDirectory(path_to_new_folder, questions):
    os.mkdir(path_to_new_folder)

    #Make intermediatefile
    for question in questions:
        question_index = question[0]
        new_intermediatefile_path = os.path.join(path_to_new_folder, str(question_index) + OUT_FILE)
        open(new_intermediatefile_path, 'a').close()

        #Make file that just has the question
        new_question_name_path = os.path.join(path_to_new_folder, str(question_index) + QUESTION_FILE)
        question_name_file = open(new_question_name_path,"w")
        question_name_file.write(question[1])
        question_name_file.close()
    print('directory and text files created')


















    ##

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
SURVEY_DIR = os.path.join(dir_path, "./surveys") #I don't know why something that isn't a constant is being defined like it is a constant, but I'm not going to touch this while I'm splitting up files.

#Ensure the survey directory exists
if not os.path.exists(SURVEY_DIR):
    os.makedirs(SURVEY_DIR)

def tannersReadFileGetNamesFunction(filepath):
    csv = open(filepath)
    names = []
    people = []
    names_to_return = []
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
        people.append(person)

    for individual in people:
        names_to_return.append("%s%d" %(individual.get_name(), individual.id_num))

    return names_to_return


def GetQuestionNameFromTextFile(filepath):
    file = open(filepath, 'r')
    question = file.read()
    return question

def GetFormFromName(name, survey_folders):
    #print(name)
    folder_path = os.path.join(survey_folders, name)
    #print(folder_path)
    questionnamepath = os.path.join(folder_path, QUESTION_FILE)
    #print(questionnamepath)
    inputfilepath = os.path.join(folder_path, NAME_FILE)
    #print(inputfilepath)
    intermediatefilepath = os.path.join(folder_path, OUT_FILE)
    #print(intermediatefilepath)
    nameslist = tannersReadFileGetNamesFunction(inputfilepath)
    #print(nameslist)
    questiontext = GetQuestionNameFromTextFile(questionnamepath)
    #print(questiontext)
    return questiontext, inputfilepath, nameslist, intermediatefilepath

def createSurveyDirectory(path_to_new_folder, question_name):
    os.mkdir(path_to_new_folder)

    #Make intermediatefile
    new_intermediatefile_path = os.path.join(path_to_new_folder, OUT_FILE)
    open(new_intermediatefile_path, 'a').close()

    #Make file that just has the question
    new_question_name_path = os.path.join(path_to_new_folder, QUESTION_FILE)
    question_name_file = open(new_question_name_path,"w")
    question_name_file.write(question_name)
    question_name_file.close()
    print('directory and text files created')

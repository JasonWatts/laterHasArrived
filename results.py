#coding: utf8
#
# Serves a page that lets the client view a survey's results in a table, and download them as a CSV file.
# Re-generates the adjacency matrix CSV files every time this page gets loaded.
#

from flask import Blueprint, render_template, request
import pandas as pd
from person_class import Person
from survey_folders import *
from parseToCSV import *
from survey_folders import *
from take_survey import getNumberOfQuestions

results = Blueprint('results', __name__, template_folder='templates')




@results.route('/survey/<name>/results')
def results_page(name):
    SurveyFilePath = os.path.join(SURVEY_DIR, name)
    fileList = os.listdir(SurveyFilePath)
    number_of_questions = getNumberOfQuestions(name, SURVEY_DIR)

    question_numbers = [e for e in range(0, number_of_questions+1)]
    if request.url[-1] != "/":
        url = request.url + "/"
    else:
        url = request.url

    question_links = [url + str(e) for e in question_numbers]

    return render_template("results_main.html", elems=question_links)




@results.route('/survey/<name>/results/<question_number>')
def render_results(name, question_number):
    questiontext, inputfilepath, participants, intermediatefilepath = GetFormFromName(name, SURVEY_DIR, question_number)

    survey = os.path.join(SURVEY_DIR, name)
    csv_path = os.path.join(survey, str(question_number) + CSV_NAME)
    input_path = os.path.join(survey, str(question_number) + NAME_FILE)
    out_path = os.path.join(survey, str(question_number) + OUT_FILE)
    generateMatrix.run_all(participants, out_path, csv_path) #Create a bunch of file paths and then pass them to a function to generate the adjacency matrix CSV files.
    title=name

    question=questiontext

    df = pd.read_csv(csv_path)
    df = df.rename(columns={"Unnamed: 0": " "})
    table = df.to_html() #Render a table of the survey results in html.
    #table = table1[0:105] + "<th></th>" + table1[130:] #fix upper left cell called Unnamed: 0


    downloadlinknormal = request.url.split('/survey')[0]
    downloadlinkdirectional = downloadlinknormal + "/downloadCSV-directional/{}/{}".format(name, question_number)

    downloadlinknormal = downloadlinknormal + '/downloadCSV/{}/{}'.format(name, question_number)
    resultsURL = request.url[:-1]


    return render_template(RESULTS_TEMPLATE, table=table, title=title, url=resultsURL,
            question=question, downloadlinknormal=downloadlinknormal, downloadlinkdirectional=downloadlinkdirectional)



















#####

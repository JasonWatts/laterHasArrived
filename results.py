#coding: utf8
#
# Serves a page that lets the client view a survey's results in a table, and download them as a CSV file.
# Re-generates the adjacency matrix CSV files every time this page gets loaded.
#

from flask import Blueprint, render_template
import pandas as pd
from person_class import Person
from survey_folders import *
from parseToCSV import *
from survey_folders import *

results = Blueprint('results', __name__, template_folder='templates')

@results.route('/survey/<name>/results')
def results_page(name):
    SurveyFilePath = os.path.join(SURVEY_DIR, name)
    fileList = os.listdir(SurveyFilePath)
    print(fileList)
    return render_template("results_main.html", list=fileList)



@results.route('/survey/<name>/<question_number>/results')
def render_results(name, question_number):
    questiontext, inputfilepath, participants, intermediatefilepath = GetFormFromName(name, SURVEY_DIR, question_number)

    survey = os.path.join(SURVEY_DIR, name)
    csv_path = os.path.join(survey, CSV_NAME)
    input_path = os.path.join(survey, NAME_FILE)
    out_path = os.path.join(survey, OUT_FILE)
    generateMatrix.run_all(participants, out_path, csv_path) #Create a bunch of file paths and then pass them to a function to generate the adjacency matrix CSV files.
    title=name

    question=questiontext

    df = pd.read_csv(csv_path)
    table = df.to_html() #Render a table of the survey results in html.

    return render_template(RESULTS_TEMPLATE, table=table, title=title, question=question)

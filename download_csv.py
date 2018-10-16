#coding: utf8
#
# URLs that let the user download the adjacency matrix CSV file for a given survey.
# Adjacency matrix can be either directional or nondirectional.
#

from flask import Blueprint, render_template, make_response
from survey_folders import *

download_csv = Blueprint('download_csv', __name__, template_folder='templates')

@download_csv.route('/downloadCSV/<survey_name>')
def download_csv_standard(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_NAME) #Get the path to the survey's nondirectional adjacency matrix CSV file.
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    cd = 'attachment; filename=AdjacencyMatrix' + survey_name + '.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

@download_csv.route('/downloadCSV-directional/<survey_name>')
def download_csv_directional(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_DIRECTIONAL) #Get the path to the survey's directional adjacency matrix CSV file.
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    cd = 'attachment; filename=DirectionalAdjacencyMatrix' + survey_name + '.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

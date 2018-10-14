from flask import Blueprint, render_template, make_response
from survey_folders import *

download_csv = Blueprint('download_csv', __name__, template_folder='templates')

@download_csv.route('/downloadCSV/<survey_name>')
def download_csv_standard(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_NAME)
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    download_name = 'AdjacencyMatrix' + survey_name + '.csv'
    cd = 'attachment; filename=' + download_name
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

@download_csv.route('/downloadCSV-directional/<survey_name>')
def download_csv_directional(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_DIRECTIONAL)
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    download_name = 'DirectionalAdjacencyMatrix' + survey_name + '.csv'
    cd = 'attachment; filename=' + download_name
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

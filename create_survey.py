#coding: utf8
#
# Serves a page that lets the client enter information to create a new survey.
# Creates a new survey folder in "surveys" using that information.
#

from flask import Blueprint, render_template, request
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, SubmitField
from survey_folders import *

class CreateSurvey(Form):
    survey_create_name = TextField('Please enter the title of this survey:')
    question_name = TextField('Please enter your question prompt:')
    csv_upload = FileField('Upload CSV File')
    submit = SubmitField('Create Survey')

create_survey = Blueprint('create_survey', __name__, template_folder='templates')
@create_survey.route('/createSurvey', methods=['get', 'post'])
def createSurveyPage():
    if request.method == 'POST': #If the form is being submitted, then process the data.
        print("recieved post for createSurvey")

        folder_name = request.form['survey_create_name'].replace(' ', '_') #Retrieve the name of the survey and replace spaces with underscores.
        path_to_new_folder = os.path.join(SURVEY_DIR, folder_name)

        question_name = request.form['question_name'] #Retrive the question prompt.
        createSurveyDirectory(path_to_new_folder, question_name)

        names_file = request.files['csv_upload'] #Attempt to download the given CSV file.
        if names_file:
            names_file.save(os.path.join(path_to_new_folder, NAME_FILE))
            print('survey created in '+path_to_new_folder)
            newstring = request.url.replace('/createSurvey', '/survey/{}'.format(folder_name))
            return "Thanks! you can now send your survey out at <a href='{0}'>{0}</a>  and  you can see and download your results at <a href='{0}/results'>{0}/results</a>".format(newstring)
        return "Unable to upload names file."

    form = CreateSurvey() #If the form is not being submitted, then create a new form and serve it to the user.
    return render_template(ADMIN_TEMPLATE, form=form)

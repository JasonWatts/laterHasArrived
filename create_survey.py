#coding: utf8
#
# Serves a page that lets the client enter information to create a new survey.
# Creates a new survey folder in "surveys" using that information.
#

from flask import Blueprint, render_template, request
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, SubmitField, IntegerField, TextAreaField
from survey_folders import *

class CreateSurvey(Form):
    survey_create_name = TextField('Please enter the title of this survey:')
    questions = TextAreaField('Please enter the questions you would like to answer, press enter to split the questions:')
    csv_upload = FileField('Upload CSV File')
    submit = SubmitField('Create Survey')

def processQuestions(questions):
    list_of_questions = questions.split('\n')
    list_of_questions = [e for e in list_of_questions if e != '']
    return list_of_questions, len(list_of_questions)

create_home = Blueprint('home', __name__, template_folder='templates')
@create_home.route('/')
def homepage():
    surveyNamesList = os.listdir(SURVEY_DIR)
    return render_template(HOMEPAGE_TEMPLATE, list=surveyNamesList)



create_survey = Blueprint('create_survey', __name__, template_folder='templates')
@create_survey.route('/createSurvey', methods=['get', 'post'])
def createSurveyPage():
    if request.method == 'POST': #If the form is being submitted, then process the data.

        folder_name = request.form['survey_create_name'].replace(' ', '_') #Retrieve the name of the survey and replace spaces with underscores.
        path_to_new_folder = os.path.join(SURVEY_DIR, folder_name)

        questions = request.form['questions']

        questions, number_of_questions = processQuestions(questions)

        if questions == 'Not the right number of questions':
            return render_template(ADMIN_TEMPLATE, form=form)

        questions = [(questions.index(e), e) for e in questions]

        createSurveyDirectory(path_to_new_folder, questions)

        names_file = request.files['csv_upload'] #Attempt to download the given CSV file.
        if names_file:
            names_file.save(os.path.join(path_to_new_folder, NAME_FILE))

            send_out_survey_link = request.url.strip("createSurvey") + 'survey/{}/'.format(folder_name)
            see_results_link = request.url.strip("createSurvey") + 'survey/{}/results'.format(folder_name)

            send_out_link = "Thanks! you can now send your survey out at <a href='(0)'>(0)</a>  and  you can see and download your results at <a href='(1)'>(1)</a>".replace('(0)', send_out_survey_link)


            send_out_link = send_out_link.replace('(1)', see_results_link)

            return render_template(ADMIN2_TEMPLATE, link_to_go_to=send_out_survey_link,
            see_results_link=see_results_link )
        return "Unable to upload names file."

    form = CreateSurvey() #If the form is not being submitted, then create a new form and serve it to the user.
    return render_template(ADMIN_TEMPLATE, form=form)






















    ##

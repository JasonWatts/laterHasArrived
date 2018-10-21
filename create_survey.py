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
    number_of_questions = IntegerField('Enter the number of questions:')
    questions = TextAreaField('Please enter the questions you would like to answer, press enter to split the questions:')
    csv_upload = FileField('Upload CSV File')
    submit = SubmitField('Create Survey')

def processQuestions(questions, number_of_questions):
    list_of_questions = questions.split('~')
    print(list_of_questions)
    print(int(number_of_questions))
    if len(list_of_questions) != int(number_of_questions):
        return 'Not the right number of questions'
    else:
        return list_of_questions


create_survey = Blueprint('create_survey', __name__, template_folder='templates')
@create_survey.route('/', methods=['get', 'post'])
def createSurveyPage():
    if request.method == 'POST': #If the form is being submitted, then process the data.
        print("recieved post for createSurvey")

        folder_name = request.form['survey_create_name'].replace(' ', '_') #Retrieve the name of the survey and replace spaces with underscores.
        path_to_new_folder = os.path.join(SURVEY_DIR, folder_name)

        number_of_questions = request.form['number_of_questions'] #Retrive the question prompt.
        questions = request.form['questions']

        questions = processQuestions(questions, number_of_questions)

        if questions == 'Not the right number of questions':
            print('It Didnt work, not right number of questions')
            return render_template(ADMIN_TEMPLATE, form=form)

        questions = [(questions.index(e), e) for e in questions]
        print(questions)
        print(number_of_questions)

        createSurveyDirectory(path_to_new_folder, questions)

        names_file = request.files['csv_upload'] #Attempt to download the given CSV file.
        if names_file:
            names_file.save(os.path.join(path_to_new_folder, NAME_FILE))
            print('survey created in '+ path_to_new_folder)
            newstring = request.url + '/survey/{}'.format(folder_name)
            return "Thanks! you can now send your survey out at <a href='{0}'/survey/0>{0}'/survey/0</a>  and  you can see and download your results at <a href='{0}/results'>{0}/results</a>".format(newstring)
        return "Unable to upload names file."

    form = CreateSurvey() #If the form is not being submitted, then create a new form and serve it to the user.
    return render_template(ADMIN_TEMPLATE, form=form)

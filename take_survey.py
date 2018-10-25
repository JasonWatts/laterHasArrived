#coding: utf8
#
# Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
# Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Blueprint, render_template, request, redirect
from flask_wtf import Form
from wtforms import widgets, SelectField, SelectMultipleField, SubmitField, TextField
from wtforms.validators import InputRequired
from survey_folders import *

# Checkbox input object, credit to https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Class for the survey.
class SurveyForm(Form):
    name = SelectField('Please select who you are. Type your name after clicking the drop down box!', validators = [InputRequired()], id='name_select') #Dropdown menu for participant's name.
    search = TextField('Enter Name', id='searchbar') #Searchbar to filter the checkbox field.
    choices = MultiCheckboxField("", validators = [InputRequired()], id='selector') #Checkbox field of names.
    submit = SubmitField('submit') #Submit button on the form.

take_survey = Blueprint('take_survey', __name__, template_folder='templates')

# This is where the participant will enter in the survey
@take_survey.route('/survey/<name>/<person_id>/<question_number>') #Should not just be "/<name>" because browsers make requests to "/favicon.ico"
def my_view_func(name, question_number, person_id):
    print(name)
    print(question_number)
    print(SURVEY_DIR)
    questiontext, inputfilepath, participants, intermediatefilepath = GetFormFromName(name, SURVEY_DIR, question_number)
    form = SurveyForm()
    redirectlink = request.url + '/handle_data'
    display_list = []
    for key in participants:
        if int(key) != int(person_id):
            display_list.append((key, participants[key].get_name()))  # Populate the name dropdown and checkbox options with the available names.
    form.choices.choices = display_list
    form.name.choices = display_list
    print("served form for /survey/"+name)
    return render_template(SURVEY_TEMPLATE, questiontext=questiontext, form=form, redirectlink = redirectlink, name = name)


def getNumberOfQuestions(survey_name, SURVEY_DIR):
    files = os.listdir(os.path.join(SURVEY_DIR, survey_name))
    print("survey-dir:  " + SURVEY_DIR)
    print("files:  " + str(files))
    nums = [int(e.split('response')[0]) for e in files if 'response' in e]
    print("nums : " + str(nums))
    number_of_questions = max(nums)
    return number_of_questions




# This page handles our data and writes it to the intermediate file path
@take_survey.route('/survey/<name>/<person_id>/<question_number>/handle_data', methods=['POST'])
def handle_data(name, person_id, question_number):
    print(name)
    print(question_number)
    person = person_id
    choices = request.form.getlist('choices') #Get the list of people the participant knows.
    print("recieved a response for /survey/"+name+" from "+person)
    questiontext, inputfilepath, participants, intermediatefilepath = GetFormFromName(name, SURVEY_DIR, question_number)
    with open(intermediatefilepath, "a") as out:
        out.write("{}: {}\n".format(person, ', '.join(choices))) #Write the response as a new line into an intermediate file, in the format "participant: name1, name2, name3"
    print("response recorded")

    ## read number of questions
    print(request.url)
    number_of_questions = getNumberOfQuestions(name, SURVEY_DIR)
    print(number_of_questions)

    ## Go to next question when done
    next_q = int(question_number) + 1
    redirectlink = request.url.replace('{}/handle_data'.format(question_number), str(next_q))

    if int(question_number) < number_of_questions:
        return redirect(redirectlink)
    return "Thank you for your response! Please return to the SurveyMonkey tab"



@take_survey.route('/survey/<name>/', methods=['POST', 'GET'])
def pick_name(name):
    form = SurveyForm()
    questiontext, inputfilepath, participants, intermediatefilepath = GetFormFromName(name, SURVEY_DIR, 0)
    display_list = [(key, participants[key].get_name()) for key in participants]  # Populate the name dropdown and checkbox options with the available names.
    form.choices.choices = display_list
    form.name.choices = display_list
    if request.method == 'POST':
        person = request.form['name']
        choices = request.form.getlist('choices')
        print("recieved a response for /survey/"+name+" from "+person)
        print(person)
        if request.url[-1] != "/":
            url = request.url + "/"
        else:
            url = request.url
        redirectlink = url + str(person) + '/0'
        return redirect(redirectlink)
    else:
        return render_template(PICK_NAME_TEMPLATE, form=form, name = name)
















    ##########

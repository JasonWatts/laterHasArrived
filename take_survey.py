#coding: utf8
#
# Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
# Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Blueprint, render_template, request
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
@take_survey.route('/survey/<name>') #Should not just be "/<name>" because browsers make requests to "/favicon.ico"
def my_view_func(name):
    questiontext, inputfilepath, nameslist, intermediatefilepath = GetFormFromName(name, SURVEY_DIR)
    form = SurveyForm()
    redirectlink = request.url + '/handle_data'
    form.choices.choices = [(e, e) for e in nameslist] #Populate the checkbox options with the available names.
    form.name.choices =  [(e, e) for e in nameslist]   #Populate the name dropdown options with the available names.
    print("served form for /survey/"+name)
    return render_template(SURVEY_TEMPLATE, questiontext=questiontext, form=form, redirectlink = redirectlink, name = name)

# This page handles our data and writes it to the intermediate file path
@take_survey.route('/survey/<name>/handle_data', methods=['POST'])
def handle_data(name):
    person = request.form['name'] #Get the participant's name.
    choices = request.form.getlist('choices') #Get the list of people the participant knows.
    print("recieved a response for /survey/"+name+" from "+person)
    questiontext, inputfilepath, nameslist, intermediatefilepath = GetFormFromName(name, SURVEY_DIR)
    with open(intermediatefilepath, "a") as out:
        out.write("{}: {}\n".format(person, ', '.join(choices))) #Write the response as a new line into an intermediate file, in the format "participant: name1, name2, name3"
    print("response recorded")
    return "Thank you for your response!"

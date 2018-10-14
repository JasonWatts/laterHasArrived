from flask import Blueprint, render_template, request
from flask_wtf import Form
from wtforms import widgets, SelectField, SelectMultipleField, SubmitField, TextField
from wtforms.validators import InputRequired
from survey_folders import *

#Checkbox input object, credit to https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Class for the survey.
class SurveyForm(Form):
    name = SelectField('Please select who you are. Type your name after clicking the drop down box!', validators = [InputRequired()])
    search = TextField('Enter Name', id='searchbar')
    Choices = MultiCheckboxField("", validators = [InputRequired()], id='selector')
    submit = SubmitField('submit')

take_survey = Blueprint('take_survey', __name__, template_folder='templates')

# This is where the participant will enter in the survey
@take_survey.route('/<name>')
def my_view_func(name):
    questiontext, inputfilepath, nameslist, intermediatefilepath = GetFormFromName(name, SURVEY_DIR)
    print('GetFormFromName Worked')
    form = SurveyForm()
    name + '/handle_data'
    print(request.url)
    redirectlink = request.url + '/handle_data'
    print('form created')
    form.Choices.choices = [(e, e) for e in nameslist]
    print('choices assigned')
    form.name.choices =  [(e, e) for e in nameslist]
    #form.choice.choices =  [(e, e) for e in nameslist]
    print('name assigned')
    return render_template(SURVEY_TEMPLATE, questiontext=questiontext, form=form, redirectlink = redirectlink, name = name)

### This page handles our data and writes it to the intermediate file path
@take_survey.route('/<name>/handle_data', methods=['POST'])
def handle_data(name):
    print(request.form)
    #print(name)
    print('we made it to handle_data')
    Person = request.form['name']
    #Choices = [request.form['choice']]
    Choices = request.form.getlist('Choices')
    print('person is :')
    print(Person)
    print('Choices for ourput are:')
    print(Choices)
    questiontext, inputfilepath, nameslist, intermediatefilepath = GetFormFromName(name, SURVEY_DIR)
    with open(intermediatefilepath, "a") as out:
        print(intermediatefilepath)
        print('OUTPUT TEXT:')
        print("{}: {}\n".format(Person, ', '.join(Choices)))
        output = "{}: {}\n".format(Person, ', '.join(Choices))
        out.write(output)
    return "Thank you for your response!"

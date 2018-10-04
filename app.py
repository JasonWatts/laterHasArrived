#coding: utf8
#
#Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
#Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Flask, render_template, request, make_response
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from flask.views import View
from wtforms import widgets, SelectField, SelectMultipleField, SubmitField, TextField
from wtforms.validators import InputRequired
from parseToCSV import *
import os
import pandas as pd
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from person_class import Person


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'

dir_path = os.path.dirname(os.path.realpath(__file__))

HOMEPAGE_TEMPLATE = "homepage.html"
SURVEY_TEMPLATE = "survey.html"
RESULTS_TEMPLATE = "results.html"
NAME_FILE = "names.csv"
QUESTION_FILE = "questionname.txt"
OUT_FILE = "response.txt"
CSV_NAME = "adjacency.csv"
ADMIN_TEMPLATE = "adminpage.html"
CSV_DIRECTIONAL = "adjacency_directional.csv"
SURVEY_DIR = os.path.join(dir_path, "./surveys")

#Ensure the survey directory exists
if not os.path.exists(SURVEY_DIR):
    os.makedirs(SURVEY_DIR)


def tannersReadFileGetNamesFunction(filepath):
    csv = open(filepath)
    names = []
    people = []
    names_to_return = []
    for line in csv:
        names.append(line.strip("\n"))
    csv.close()
    for i in range(len(names)):
        name_info = names[i].split(",")
        if len(name_info) == 4:
            person = Person(i, name_info[0], name_info[1], name_info[2], name_info[3])
        elif len(name_info) == 3:
            person = Person(i, name_info[0], name_info[1], name_info[2])
        else:
            person = Person(i, name_info[0], name_info[1])
        people.append(person)

    for individual in people:
        names_to_return.append(individual.get_name())

    return names_to_return


def GetQuestionNameFromTextFile(filepath):
    file = open(filepath, 'r')
    question = file.read()
    return question

def GetFormFromName(name, survey_folders): 
    #print(name)
    folder_path = os.path.join(survey_folders, name)
    #print(folder_path)
    questionnamepath = os.path.join(folder_path, QUESTION_FILE)
    #print(questionnamepath)
    inputfilepath = os.path.join(folder_path, NAME_FILE)
    #print(inputfilepath)
    intermediatefilepath = os.path.join(folder_path, OUT_FILE)
    #print(intermediatefilepath)
    nameslist = tannersReadFileGetNamesFunction(inputfilepath)
    #print(nameslist)
    questiontext = GetQuestionNameFromTextFile(questionnamepath)
    #print(questiontext)
    return questiontext, inputfilepath, nameslist, intermediatefilepath


#Checkbox input object, credit to https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Class for the survey.
class SurveyForm(Form):
    name = SelectField('Please select who you are. Type your name after clicking the drop down box!', validators = [InputRequired()])
    Choices = MultiCheckboxField("", validators = [InputRequired()])
    submit = SubmitField('submit')


class CreateSurvey(Form):
    survey_create_name = TextField('What is the Name of the Survey? :')
    question_name = TextField('What should the name of the question be? :')
    csv_upload = FileField('Enter File plz')
    submit = SubmitField('submit')



def createSurveyDirectory(path_to_new_folder, question_name):
    os.mkdir(path_to_new_folder)

    #Make intermediatefile
    new_intermediatefile_path = os.path.join(path_to_new_folder, OUT_FILE)
    open(new_intermediatefile_path, 'a').close()

    #Make file that just has the question
    new_question_name_path = os.path.join(path_to_new_folder, QUESTION_FILE)
    question_name_file = open(new_question_name_path,"w")
    question_name_file.write(question_name)
    question_name_file.close()
    print('directory and text files created')


@app.route('/')
def homepage():
    return render_template(HOMEPAGE_TEMPLATE)




@app.route('/admin', methods=['get', 'post'])
def adminpage():
    form = CreateSurvey()
    print('Survey Created')
    if request.method == 'POST':
        folder_name = request.form['survey_create_name']
        folder_name = folder_name.replace(' ', '_')
        path_to_new_folder = os.path.join(SURVEY_DIR, folder_name)

        question_name = request.form['question_name']
        createSurveyDirectory(path_to_new_folder, question_name)

        print('Post worked')
        file = request.files['csv_upload']
        print(file)
        if file:
            print('if file')
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(path_to_new_folder, NAME_FILE))
            print(os.path.join(path_to_new_folder, NAME_FILE))
            print('file saved')
            return 'thanks! you can now send your survey out at "_______/{}"'.format(folder_name)

    return render_template(ADMIN_TEMPLATE, form=form)


# This is where the participant will enter in the survey
@app.route('/<name>')
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
    print('name assigned')
    return render_template(SURVEY_TEMPLATE, questiontext=questiontext, form=form, redirectlink = redirectlink)


### This page handles our data and writes it to the intermediate file path
@app.route('/<name>/handle_data', methods=['POST'])
def handle_data(name):
    print(request.form)
    #print(name)
    print('we made it to handle_data')
    Person = request.form['name']
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



@app.route('/<name>/manager')
def render_manager(name):
    questiontext, inputfilepath, nameslist, intermediatefilepath = GetFormFromName(name, SURVEY_DIR)
    
    survey = os.path.join(SURVEY_DIR, name)
    csv_path = os.path.join(survey, CSV_NAME)
    input_path = os.path.join(survey, NAME_FILE)
    out_path = os.path.join(survey, OUT_FILE)
    
    generateMatrix.run_all(input_path, out_path, csv_path)
    
    title=name
       
    question=questiontext

    df = pd.read_csv(csv_path)
    table = df.to_html()

    return render_template(RESULTS_TEMPLATE, table=table, title=title, question=question)



@app.route('/downloadCSV/<survey_name>')
def download_csv(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_NAME)
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    cd = 'attachment; filename=AdjacencyMatrix.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

@app.route('/downloadCSV-directional/<survey_name>')
def download_csv_directional(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_DIRECTIONAL)
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    cd = 'attachment; filename=AdjacencyMatrix.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response


if __name__ == "__main__":
    app.run()

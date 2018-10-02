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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'

SURVEY_TEMPLATE = "survey.html"
NAME_FILE = "names.txt"
OUT_FILE = "response.txt"
CSV_NAME = "adjacency.csv"
ADMIN_TEMPLATE = "adminpage.html"
where_on_my_computer_do_I_want_to_save_survey_folders = "C:/Users/walke/Desktop/"


def tannersReadFileGetNamesFunction(filepath):
    df = pd.read_csv(filepath)
    names = list(df['names'])
    return names


def GetQuestionNameFromTextFile(filepath):
    file = open(filepath, 'r')
    question = file.read()
    return question

def GetFormFromName(name, where_on_my_computer_do_I_want_to_save_survey_folders):
    print(name)
    folder_path = os.path.join(where_on_my_computer_do_I_want_to_save_survey_folders, name)
    print(folder_path)
    questionnamepath = os.path.join(folder_path, 'questionname.txt')
    print(questionnamepath)
    inputfilepath = os.path.join(folder_path, 'input.csv')
    print(inputfilepath)
    intermediatefilepath = os.path.join(folder_path, 'intermediatefile.txt')
    print(intermediatefilepath)
    nameslist = tannersReadFileGetNamesFunction(inputfilepath)
    print(nameslist)
    questiontext = GetQuestionNameFromTextFile(questionnamepath)
    print(questiontext)
    return questiontext, inputfilepath, nameslist



#names = open(NAME_FILE,'r').read().split('\n')[:-1] #Strip the last element, which will just be an empty string created by the last newline in the file.
#names_nospace = [name.strip() for name in names]

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
    new_intermediatefile_path = os.path.join(path_to_new_folder, 'intermediatefile.txt')
    open(new_intermediatefile_path, 'a').close()

    #Make file that just has the question
    new_question_name_path = os.path.join(path_to_new_folder, 'questionname.txt')
    question_name_file = open(new_question_name_path,"w")
    question_name_file.write(question_name)
    question_name_file.close()
    print('directory and text files created')




@app.route('/admin', methods=['get', 'post'])
def adminpage():
    form = CreateSurvey()
    print('Survey Created')
    if request.method == 'POST':
        folder_name = request.form['survey_create_name']
        folder_name = folder_name.replace(' ', '_')
        path_to_new_folder = os.path.join(where_on_my_computer_do_I_want_to_save_survey_folders, folder_name)

        question_name = request.form['question_name']
        createSurveyDirectory(path_to_new_folder, question_name)

        print('Post worked')
        file = request.files['csv_upload']
        print(file)
        if file:
            print('if file')
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(path_to_new_folder, 'input.csv'))
            print('file saved')
            return 'thanks! you can now send your survey out at "_______/{}"'.format(folder_name)

    return render_template(ADMIN_TEMPLATE, form=form)

@app.route('/<name>')
def my_view_func(name):
    questiontext, inputfilepath, nameslist = GetFormFromName(name, where_on_my_computer_do_I_want_to_save_survey_folders)
    print('GetFormFromName Worked')
    form = SurveyForm()
    print('form created')
    form.Choices.choices = [(e, e) for e in nameslist]
    print('choices assigned')
    form.name.choices =  [(nameslist.index(e), e) for e in nameslist]
    print('name assigned')
    if request.method == 'POST':
        print('posting')
        form = SurveyForm(request.form)
        if form.validate_on_submit():
            print('is valid on submit')
            print(form.Choices.data)
            print(form.name.data)
            with open(inputfilepath, "a") as out:
                out.write("{}: {}\n".format(form.name.data, ', '.join(form.choices.data)))
            return "Thank you for your response!"
        else:
            print(form.errors)
    else:
        print(request.method)

    #print(questiontext)
    #print(nameslist)
    return render_template(SURVEY_TEMPLATE, questiontext=questiontext, form=form)






@app.route('/manager')
def render_manager():
    generateMatrix.run_all(NAME_FILE, OUT_FILE, CSV_NAME)

    df = pd.read_csv(CSV_NAME)
    html = df.to_html() +  '''<button type="download" onclick="window.open('/downloadCSV')">Download CSV</button>'''

    return html


@app.route('/downloadCSV/')
def download_csv():
    with open(CSV_NAME) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    cd = 'attachment; filename=AdjacencyMatrix.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

if __name__ == "__main__":
    app.run()

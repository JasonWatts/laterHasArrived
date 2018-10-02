#coding: utf8
#
#Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
#Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Flask, render_template, request, make_response
from flask_wtf import Form
from flask.views import View
from wtforms import widgets, SelectField, SelectMultipleField, SubmitField, TextField
from wtforms.validators import InputRequired
from parseToCSV import *
import os
from werkzeug import secure_filename
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'

SURVEY_TEMPLATE = "survey.html"
NAME_FILE = "names.txt"
OUT_FILE = "response.txt"
CSV_NAME = "adjacency.csv"
ADMIN_TEMPLATE = "adminpage.html"
where_on_my_computer_do_I_want_to_save_survey_folders = "C:/Users/walke/Desktop/"



names = open(NAME_FILE,'r').read().split('\n')[:-1] #Strip the last element, which will just be an empty string created by the last newline in the file.
names_nospace = [name.strip() for name in names]

#Checkbox input object, credit to https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Class for the survey.
class SurveyForm(Form):
    name = SelectField('Please select who you are. Type your name after clicking the drop down box!', choices = list(zip(names,names_nospace)), validators = [InputRequired()])
    choices = MultiCheckboxField("Please select who you know", choices = list(zip(names,names_nospace)), validators = [InputRequired()])
    submit = SubmitField('submit')


class CreateSurvey(Form):
    survey_create_name = TextField('What is the Name of the Survey? :')
    question_name = TextField('What should the name of the question be? :')
    csv_upload = FileField('Enter File plz')
    submit = SubmitField('submit')


def createSurveyDirectory(path_to_new_folder):
    os.mkdir(path_to_new_folder) # makes a new folder
    new_text_files_path = os.path.join(path_to_new_folder, 'intermediatefile.txt')
    open(new_text_files_path, 'a').close() #Creates a blank intermediatefile.txt in that folder
    print('directory and text files created')




@app.route('/admin', methods=['get', 'post'])
def adminpage():
    form = CreateSurvey()
    print('Survey Created')
    if request.method == 'POST':
        folder_name = request.form['survey_create_name'] 
        folder_name = folder_name.replace(' ', '_') # Important note: folder_name's will replace ' ' with '_', to make it easier for URL team
        path_to_new_folder = os.path.join(where_on_my_computer_do_I_want_to_save_survey_folders, folder_name)
        createSurveyDirectory(path_to_new_folder)

        print('Post worked')
        file = request.files['csv_upload']
        print(file)
        if file:
            print('if file worked')
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(path_to_new_folder, filename))  # Saves Filename to our new folder
            print('file saved')
            return 'thanks!' # if it worked it should go to a new screen that just says thanks!

    return render_template(ADMIN_TEMPLATE, form=form)




@app.route('/', methods=['get','post'])
def survey():
    form = SurveyForm(request.form)
    if form.validate_on_submit():
        with open(OUT_FILE, "a") as out:
            out.write("{}: {}\n".format(form.name.data, ', '.join(form.choices.data)))
        return "Thank you for your response!"
    else:
        print(form.errors)
    return render_template(SURVEY_TEMPLATE, form=form)

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

#coding: utf8
#
#Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
#Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Flask, render_template, request, make_response
from flask_wtf import Form
from wtforms import widgets, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired
from parseToCSV import *
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'

SURVEY_TEMPLATE = "survey.html"
NAME_FILE = "names.txt"
OUT_FILE = "response.txt"
CSV_NAME = "adjacency.csv"

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

@app.route('/', methods=['get','post'])
def survey():
    form = SurveyForm(request.form)
    if form.validate_on_submit():
        with open(OUT_FILE, "a") as out:
            out.write(f"{form.name.data}: {', '.join(form.choices.data)}\n")
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

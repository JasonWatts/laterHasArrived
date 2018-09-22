#coding: utf8
#
#Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
#Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import widgets, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'

NAMES = ["name1", "name2", "name3"] #TODO: Load from file.

#Checkbox input object, credit to https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Class for the survey.
class SurveyForm(Form):
    name = SelectField('Name', choices = list(zip(NAMES,NAMES)), validators = [InputRequired()])
    choices = MultiCheckboxField("Connections", choices = list(zip(NAMES,NAMES)), validators = [InputRequired()])
    submit = SubmitField('submit')
    n_choices = len(NAMES)

@app.route('/', methods=['get','post'])
def survey():
    form = SurveyForm(request.form)
    if form.validate_on_submit():
        print(form.choices.data)
    else:
        print(form.errors)
    return render_template('survey.html', form=form)

#coding: utf8
#
#Serves the user a web form created from (1) an html template, and (2) a file listing the available names.
#Writes a respondents results to a single line of a "response.txt" dump file.
#

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def survey():
    return render_template('survey.html', names=["name1","name2","name3"])

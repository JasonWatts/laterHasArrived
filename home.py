#coding: utf8
#
# A basic homepage, with a button that links to the createSurvey page.
#

from flask import Blueprint, render_template
from survey_folders import *

home = Blueprint('home', __name__, template_folder='templates')
@home.route('/')
def homepage():
    return render_template(HOMEPAGE_TEMPLATE)

from flask import Blueprint, render_template, request
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, SubmitField
from werkzeug import secure_filename
from survey_folders import *

class CreateSurvey(Form):
    survey_create_name = TextField('Please enter the title of this survey:')
    question_name = TextField('Please enter your question prompt:')
    csv_upload = FileField('Upload CSV File')
    submit = SubmitField('Create Survey')

create_survey = Blueprint('create_survey', __name__, template_folder='templates')
@create_survey.route('/createSurvey', methods=['get', 'post'])
def createSurveyPage():
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
            url = request.url
            newstring = url.replace('/createSurvey', '/survey/{}'.format(folder_name))
            string = """
            Thanks! you can now send your survey out at <a href='{}'>{}</a>  and  you can see and download your results at <a href='{}/results'>{}/results</a>
            """.format(newstring, newstring, newstring, newstring)
            return string

    return render_template(ADMIN_TEMPLATE, form=form)

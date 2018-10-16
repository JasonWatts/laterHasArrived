#coding: utf8
#
# Assemles the blueprints for each web page and hosts the application.
#

from flask import Flask
import socket

from home import home
from create_survey import create_survey
from take_survey import take_survey
from results import results
from download_csv import download_csv

my_ip=([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]) #Get an IP that others can connect to.

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'
app.url_map.strict_slashes = False


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

participants = {}

#Ensure the survey directory exists
if not os.path.exists(SURVEY_DIR):
    os.makedirs(SURVEY_DIR)


def read_names(filepath):
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
        participants[person.id_num] = person

    for individual in people:
        names_to_return.append("%s%d" %(individual.get_name(), individual.id_num))

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
    nameslist = read_names(inputfilepath)
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
    search = TextField('Enter Name', id='searchbar')
    Choices = MultiCheckboxField("", validators = [InputRequired()], id='selector')
    #choice = SelectField('Select a Name', validators = [InputRequired()], id='selector')
    submit = SubmitField('submit')


class CreateSurvey(Form):
    survey_create_name = TextField('Please enter the title of this survey:')
    question_name = TextField('Please enter your question prompt:')
    csv_upload = FileField('Upload CSV File')
    submit = SubmitField('Create Survey')



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




@app.route('/createSurvey', methods=['get', 'post'])
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
            newstring = url.replace('/createSurvey', '/{}'.format(folder_name))
            string = """
            Thanks! you can now send your survey out at <a href='{}'>{}</a>  and  you can see and download your results at <a href='{}/results'>{}/results</a>
            """.format(newstring, newstring, newstring, newstring)
            return string

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
    display_list = []
    for key in participants:
        temp = str(participants[key].get_name())
        display_list.append((key,temp))
    form.Choices.choices = display_list
    #form.Choices.choices = [(e, e) for e in nameslist]
    print('choices assigned')
    #form.name.choices =  [(e, e) for e in nameslist]
    form.name.choices = display_list
    #form.choice.choices =  [(e, e) for e in nameslist]
    print('name assigned')
    return render_template(SURVEY_TEMPLATE, questiontext=questiontext, form=form, redirectlink = redirectlink, name = name)

### This page handles our data and writes it to the intermediate file path
@app.route('/<name>/handle_data', methods=['POST'])
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



@app.route('/<name>/results')
def render_results(name):
    questiontext, inputfilepath, nameslist, intermediatefilepath = GetFormFromName(name, SURVEY_DIR)

    survey = os.path.join(SURVEY_DIR, name)
    csv_path = os.path.join(survey, CSV_NAME)
    input_path = os.path.join(survey, NAME_FILE)
    out_path = os.path.join(survey, OUT_FILE)
    generateMatrix.run_all(participants, out_path, csv_path)
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
    download_name = 'AdjacencyMatrix' + survey_name + '.csv'
    cd = 'attachment; filename=' + download_name
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

@app.route('/downloadCSV-directional/<survey_name>')
def download_csv_directional(survey_name):
    file_path = os.path.join(SURVEY_DIR, survey_name, CSV_DIRECTIONAL)
    with open(file_path) as csvFile:
        makeCSV = csvFile.read()
    response = make_response(makeCSV)
    download_name = 'DirectionalAdjacencyMatrix' + survey_name + '.csv'
    cd = 'attachment; filename=' + download_name
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'
    return response

app.register_blueprint(home)
app.register_blueprint(create_survey)
app.register_blueprint(take_survey)
app.register_blueprint(results)
app.register_blueprint(download_csv)

if __name__ == "__main__":
    app.run(debug=True, host=my_ip, port=3134)

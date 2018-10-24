#coding: utf8
#
# Assemles the blueprints for each web page and hosts the application.
#

from flask import Flask
import socket

from create_survey import create_survey
from take_survey import take_survey, pick_name
from results import results
from download_csv import download_csv

my_ip=([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]) #Get an IP that others can connect to.

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing_key'
app.url_map.strict_slashes = False

app.register_blueprint(create_survey)
app.register_blueprint(take_survey)
app.register_blueprint(results)
app.register_blueprint(download_csv)

if __name__ == "__main__":
    app.run(debug=True, host=my_ip, port=3134)

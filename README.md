# laterHasArrived
Software Development Project for Westmont's CS120 2018
Web app that lets you take a simple survey then creates an adjacency matrix from the data collected.

# TODO:
1. [Create] The input names.csv file of participant names should have a header row,
which should not be treated as an actual participant
1. (DONE) [Create] The prompt of the names.csv file should mention "file containing names of participants" 
1. [Results] Verify resolution of NaN problem associated with duplicate rows/columns in AM table
1. [Respond] Remove (not just disable) responder's name from selection options
1. [Respond] Remove the assigned ID suffix in names lists
1. 
1. [Respond] On survey-submit, resulting page should also prompt responder
to return to survey monkey tab from which this started
1. [Respond] Display extra identifying name info only when duplicate names exist
1. [Respond] Display extra identifying info for all names
(possibly minus names that already incorporate such info) on hover
1. [Create/Respond/Results] Improve appearance fonts/margins/styling/...
1. [Create] Allow second and subsequent questions within single survey;
currently second/subsequent questions in an existing survey generate errors
1. [General] Maintain README.md, keeping it aligned with project progress
1. [README] Consolidate "Server" and "Getting started" into a "Running" section
1. [README] Expand "Requirements" with Python 3.5, Internet connection accessible to responders, etc.
1. [README] "CSV" should probably be moved earlier and may not merit its own section;
should mention a header row; should not say "unique-id1" because these are not unique
but collectively uniquely identify an individual
1. [README] Update "Admin view" section, maybe eliminate in favor of documentation
for each of the available URLs
1. ~~Update REAMDE: go to "...../admin"~~
1. What should the  question prompt be?
1. Add home page
   * remove the "..../admin" from README
1. In README move csv req to top
1. Add extra info for CSV upload button
1. Clarify successful test addition response
1. Add spaces between first and last names, or commas between last and first
1. Add flag for ignoring trailing slash in URL
1. Document all URLs to type in the URL bar
1. Clarify between both csv download buttons(include survey name in the downloaded file)

# Requirements

In order to run this application you first need to pip3 install some libraries:

```
pip3 install pandas --user
pip3 install flask
pip3 install flask-wtf
```

# Contributors
Christian,
Drew,
Heather,
Jared,
Jason,
Kalie,
Kyle,
Tanner,
Trevor,
Walker,
M'Kya,
Maya

# Getting started
Clone the repository to a location of your choosing, then cd into the folder.
```
$ git clone https://github.com/JasonWatts/laterHasArrived.git
$ cd laterHasArrived/
```
To start the program:
```
$ python3 app.py
```
The output should display a line similar to the following:
```
* Running on http://127.0.0.1:5000/admin (Press CTRL+C to quit)
```
Finally copy and paste the URL displayed in your terminal into a browser.

# CSV

In order for the program to run the csv must be named "names.csv" and be formatted in the following manner (last name,first name,unique-id1,unique-id2) where unique-id1 and unique-id2 are not required 


# Admin view
If you are an administrator and would like to view the adjacency matrix, type in "/manager" at the end of the current URL. This will pull up the manager view of the matrix that has been updated based on surveys received. You also will have the option to download a CSV file of the results.

# Server
To use your computer as a server, go to the file containing app.py and then run the following commands, replacing "0.0.0.0" with your device's current IP address. 
```
$ export PATH="/python/bin:$PATH"
$ export FLASK_APP=app.py
$ flask run --host=0.0.0.0 
```

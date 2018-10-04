# laterHasArrived
Software Development Project for Westmont's CS120 2018
Web app that lets you take a simple survey then creates an adjacency matrix from the data collected.

# TODO:
1. Update REAMDE: go to "...../admin"
2. What should the  question promt be?
3. Add home page
   * remove the "..../admin" from README
4. In README move csv req to top
5. Add extra info for CSV upload button
6. Clarify successfull test addition responce
7. Add spaces for names
8. Remove 'your' name after you choose it
9. Add flag for ignoring trailing slash in URL
10. Document all URLs to type in the url bar
11. Clarify between both csv download buttons(include survey name in the downloaded file)

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

In order for the program to run the csv must be named "names.csv" and be formated in the following manner (last name,first name,unique-id1,unique-id2) where unique-id1 and unique-id2 are not required 


# Admin view
If you are an administrator and would like to view the adjacency matrix, type in "/manager" at the end of the current URL. This will pull up the manager view of the matrix that has been updated based on surveys recieved. You also will have the option to download a CSV file of the results.

# Server
To use your computer as a server, go to the file containing app.py and then run the following commands, replacing "0.0.0.0" with your device's current IP address. 
```
$ export PATH="/python/bin:$PATH"
$ export FLASK_APP=app.py
$ flask run --host=0.0.0.0 
```

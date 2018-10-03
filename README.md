# laterHasArrived
Software Development Project for Westmont's CS120 2018
Web app that lets you take a simple survey then creates an adjacency matrix from the data collected.

# Requirements

In order to run this application you first need to pip3 install some libraries:

```
pip3 install pandas --user

```

# Contributors
Christian
Drew
Heather
Jared
Jason
Kalie
Kyle
Tanner
Trevor
Walker
M'Kya

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
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Finally copy and paste the URL displayed in your terminal into a browser.

#csv 

In order for the program to run the csv must be named "names.csv" and be formated in the following manner (last name, first name, unique-id1, unique-id2) where unique-id1 and unique-id2 are not required 


# Admin view
If you are an administrator and would like to view the adjacency matrix, type in "/manager" at the end of the current URL. This will pull up the manager view of the matrix that has been updated based on surveys recieved. You also will have the option to download a CSV file of the results.

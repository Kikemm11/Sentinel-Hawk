Sentinel Hawk is a flask web application to automate, optimize and manage all processes involved within a parking lot stablishment.
Part of it uses AI to recognize the vehicles and automatically generate a ticket with relevant information such as the type of vehicle, the charge and the status of the ticket
(Paid, Unpaid and Canceled). In other manners the web application allows the users with the employee role to manage the tickert system to pay and cancel transactions, 
while the admin rol is able to control all the system settings and review its revenues and daily operations on demand.

Inside this repository you will be provided with:

-The sentinel hawk source code.
- One .txt file named libs.txt with all the needed dependencies to get the project up and running.
- One .sql file containing the database structure and initial data to connect to the web application ready to be restored.

Installation:

  We highly recommend to set a python virtual environment before install all the dependencies!

  - Download or clone the repository and extract all the files
  - Create a python virtual environment $ python3 -m venv venv
  - Activate the venv $ cd venv && source bin/activate
  - Install all the required dependencies $ cd .. && pip install -r libs.txt
  - Restore the given postgres database
  - Finally run the app server $ python3 app.py
  - Open the web app in localhost:5000
  - Log in with the user: admin password: 'admin'

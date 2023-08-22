# Capstone Competency Tracker

## Installing the app
1. run pipenv install
2. run pipenv shell
3. run python main.py


## Logging into the app
As soon as you run the app, you will be prompted to either login or quit. Should you choose to login, the initial login credentials are provided below.
### Username and password

 #### Manager login info:
 Username: tylermckell@devpipeline.com
 Password: new_password
 #### User login info:
 (there are technically multiple users you can log in with right from the start, but let's use jace as an example)
 Username: jace@google
 Password: jace


## User_menu vs. Manager_menu
The app will automatically check the user_type in the database to check if the logged in user is a manager or just a regular user. If the logged in user is just a regular user, you will be directed to the user_menu where you can choose from the various option allotted to regular users. If the logged in user is a manager, they will be directed to the manager_menu where they can choose from the larger amount of options allotted to managers.

## How to navigate the User and Manager menus

The various menus through out the entire app look similar to this...

***** Welcome to the secret MANAGER menu *****
Please select one of the options below...
[V]iew from different options
[A]dd user, new competency, new assessment, assessment result
[E]dit user info, competency, assessment, assessment result
[D]elete assessment result
[X] Export all reports to a CSV file
[I]mport assessment results from a CSV file
[L]og-out

To choose one of the options above^^, the user should simply type the number or letter in the brackets[ ] that is associated with the option they would like to choose. For example, typing the letter 'v' would result in the user being able to '[V]iew from different options.

## Logging out and Quitting
In almost every single menu/sub-menu, the user has the option to log out or quit. Logging out will essentially take the user back to the intitial menu where the user can choose to log into the app or quit the app entirely. When the user selects the option to 'Quit program', the app will shut off.

## Various file submissions
 - **Main.py:** actual program that contains all the code to run the app
 - **updated_capstone_database.db:** the database
 - **CSV files** (from the manager's export & import functions):
	 - **competency_report_for_single_user.csv:** this is the output when the manager wants export a CSV file for a single user's competency report
	 - **competency_report_by_competency_and_users.csv:** this is the output when the manager wants export a CSV file for all user's competency reports
	 - **importing.csv:** this file is used for when the manager wants to import assessment result data from a CSV file into the database
  - **ERD.jpg**: ERD picture on paper


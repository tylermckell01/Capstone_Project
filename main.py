# Import necessary modules... sqlite3, csv, bcrypt
import sqlite3
import csv
import bcrypt


## Create first three users & login info (tyler mckell is manager so you can actually log in, jimmy is a user, jace is a user)

## username: tylermckell@devpipeline.com
## password: new_password

## username: jimmy@gmail
## password: chicago

## username: jace@google
## password: jace

# def create_user(cursor):
#     query = '''
#         INSERT INTO Users (first_name, last_name, phone_number, email, password, active, date_created, hire_date, user_type)
#         VALUES ('Tyler', 'McKell', '555555555', 'tylermckell@devpipeline.com', 'password', 1, '08-18-2023', '05-12-2023', 'manager');

#     '''

#     cursor.executescript(query)
    
# connection = sqlite3.connect('updated_capstone_database.db')
# cursor = connection.cursor()
# connection.commit()
# create_user(cursor)




# Update initial user's password so it is hashed correctly
def update_initial_user_password():
    connection = sqlite3.connect('updated_capstone_database.db')
    cursor = connection.cursor()

    new_password = "new_password"  
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    update_query = "UPDATE Users SET password = ? WHERE email = ?"
    cursor.execute(update_query, (hashed_password, "tylermckell@devpipeline.com"))

    connection.commit()
    connection.close()
update_initial_user_password()


# # Create initial capstone_database.db Database
def create_schema(cursor):
    query = '''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT,
            phone_number TEXT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            date_created TEXT NOT NULL,
            hire_date TEXT NOT NULL,
            user_type
        );

        CREATE TABLE IF NOT EXISTS Competencies (
            competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competency_name TEXT, 
            date_created TEXT,
            FOREIGN KEY (competency_id)
                REFERENCES Assessments (competency_id)
            FOREIGN KEY (competency_name)
                REFERENCES Assessments (competency_name)
        );

        CREATE TABLE IF NOT EXISTS Assessments (
            competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competency_name TEXT NOT NULL,
            assessment_name TEXT NOT NULL,
            date_created TEXT
        );

        CREATE TABLE IF NOT EXISTS Assessment_Results (
            user_id INTEGER,
            assessment TEXT,
            score INTEGER,
            date_taken TEXT,
            manager_administered TEXT,
            FOREIGN KEY (user_id) 
                REFERENCES Users (user_id),
            FOREIGN KEY (assessment) 
                REFERENCES Assessments (assessment_name)
        );

    '''

    cursor.executescript(query)
    
connection = sqlite3.connect('updated_capstone_database.db')
cursor = connection.cursor()
connection.commit()
create_schema(cursor)
    






# LOG-IN FUNCTIONS

## PASSWORD functions

### password hashing function
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


### check password function
def check_pw(password_input, db_hashed_password):
    return bcrypt.checkpw(password_input, db_hashed_password)


## Login into the system function
def user_login():
    print("\nUser Login")
    print("------------")
    email_input = input("\nUsername (email): ")
    password_input = input("Password: ").encode('utf-8')

    cursor.execute("SELECT user_id, password, user_type FROM Users WHERE email = ?", (email_input,))
    user_record = cursor.fetchone()

    if user_record is None:
        print('Invalid login, please try again')
        return
    

    user_id = user_record[0]
    hashed_password = user_record[1].encode('utf-8')
    user_type = user_record[2]


    if check_pw(password_input, hashed_password):
        if user_type == 'manager':
            print("\nManager login successful")
            manager_menu()
        elif user_type == 'user':
            print('\nUser login successful')
            user_menu(user_id)
    else:
        print('invalid password')






# USER menu Functions

## view competency data for only the logged in user (DONT ACTUALLY NEED THIS FUNCTION)
# def view_user_competency_data(user_id):
#     connection = sqlite3.connect("updated_capstone_database.db")
#     cursor = connection.cursor()

#     query = """
#         SELECT Users.first_name, Users.last_name, Competencies.competency_name, Assessment_Results.score
#         FROM Users
#         JOIN Assessment_Results ON Users.user_id = Assessment_Results.user_id
#         JOIN Assessments ON Assessment_Results.assessment = Assessments.assessment_name
#         JOIN Competencies ON Assessments.competency_name = Competencies.competency_name
#         WHERE Users.user_id = ?
# ;
#     """
    
#     cursor.execute(query, (user_id,))
#     rows = cursor.fetchall()

#     connection.close()

#     for row in rows:
#         first_name, last_name, competency_name, score = row
#         print(f"Name: {first_name} {last_name}, Competency: {competency_name}, Score: {score}")

    
## view assessment data for only the logged in user
def view_user_assessment_data(user_id):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = """
        SELECT Assessment_results.assessment, Assessment_results.score, Assessment_results.date_taken
        FROM Assessment_Results
        WHERE user_id = ?;
    """
    
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    connection.close()

    for row in rows:
        assessment, score, date_taken = row
        print(f"Assessment: {assessment}\nScore: {score}\nDate Taken: {date_taken}\n")








# MANAGER menu Functions

## VIEWING FUNCTIONS
### Views all Users Function
def view_all_users(table_name):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name}"

    cursor.execute(query)
    rows = cursor.fetchall()

    connection.close()

    formatted_rows = []
    for row in rows:
        user_id, first_name, last_name, phone_number, email, password, active, date_created, hire_date, user_type = row
        formatted_rows.append(f"User ID: {user_id} First name: {first_name} Last name: {last_name} Phone number: {phone_number} Email: {email} Password: {password} Active: {active} Date created: {date_created} Hire date: {hire_date} User type: {user_type}")

    return formatted_rows

### Searches user by first name Function
def first_name_search_user(table_name, search_param=None):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name} WHERE first_name LIKE ?"
    if search_param:
        params = ('%' + search_param + '%',)  


    cursor.execute(query, params)
    rows = cursor.fetchall()

    connection.close()

    return rows

### Searches user by last name Function
def last_name_search_user(table_name, search_param=None):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name} WHERE last_name LIKE ?"
    if search_param:
        params = ('%' + search_param + '%',)  


    cursor.execute(query, params)
    rows = cursor.fetchall()

    connection.close()

    return rows

### Views a report of all users and their competency levels for a given competency
def view_all_users_and_competency_level():
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = f"""SELECT Users.user_id, Users.first_name, Users.last_name, Assessment_Results.assessment, Assessment_Results.score
                FROM Users 
                INNER JOIN Assessment_Results ON Users.user_id = Assessment_Results.user_id;"""

    cursor.execute(query)
    rows = cursor.fetchall()

    connection.close()

    formatted_rows = []
    for row in rows:
        user_id, first_name, last_name, assessment, score = row
        formatted_row = f"User ID: {user_id}, Name: {first_name} {last_name}, Competency: {assessment}, Score (0-4): {score}"
        formatted_rows.append(formatted_row)

    return formatted_rows

### View a competency level report for an individual user
def view_individual_user_and_competency_level(first_name, last_name):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = """
        SELECT Users.user_id, Users.first_name, Users.last_name, Assessment_Results.assessment, Assessment_Results.score
        FROM Users
        INNER JOIN Assessment_Results ON Users.user_id = Assessment_Results.user_id
        WHERE first_name = ? AND last_name = ?;
    """
    name_values = (first_name, last_name)

    cursor.execute(query, name_values)
    rows = cursor.fetchall()

    connection.close()

    formatted_rows = []
    for row in rows:
        user_id, first_name, last_name, assessment, score = row
        formatted_row = f"User ID: {user_id}, Name: {first_name} {last_name}, Assessment: {assessment}, Score: {score}"
        formatted_rows.append(formatted_row)
    return formatted_rows

### View a list of assessments for a given user
def view_assessments_individual_user(first_name, last_name):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = """
        SELECT Users.user_id, Users.first_name, Users.last_name, Assessment_Results.assessment, Assessment_Results.score, Assessment_Results.date_taken
        FROM Users
        INNER JOIN Assessment_Results ON Users.user_id = Assessment_Results.user_id
        WHERE first_name = ? AND last_name = ?;
    """
    name_values = (first_name, last_name)

    cursor.execute(query, name_values)
    rows = cursor.fetchall()

    connection.close()

    formatted_rows = []
    for row in rows:
        user_id, first_name, last_name, assessment, score, date_taken = row
        formatted_row = f"User ID: {user_id}, Name: {first_name} {last_name}, Assessment: {assessment}, Score: {score}, Date taken: {date_taken}"
        formatted_rows.append(formatted_row)
    return formatted_rows







## Adding Functions
### Add user function
def add_user(first_name, last_name, phone_number, email, password, active, date_created, hire_date, user_type):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = 'INSERT OR REPLACE INTO Users (first_name, last_name, phone_number, email, password, active, date_created, hire_date, user_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    values = (first_name, last_name, phone_number, email, password, active, date_created, hire_date, user_type)

    cursor.execute(query, values)
    connection.commit()

    connection.close()

    return f"User '{first_name} {last_name}' has been added Successfully, wahoo!"

### Add competency function
def add_competency(competency_name, date_created):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = 'INSERT OR REPLACE INTO Competencies (competency_name, date_created) VALUES (?, ?)'
    values = (competency_name, date_created)

    cursor.execute(query, values)
    connection.commit()

    connection.close()

    return f"Competency '{competency_name}' has been added Successfully, wahoo!"

### Add a new assessment to a competency function
def add_assessment_to_competency(competency_name, assessment_name, date_created):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = '''
        INSERT OR REPLACE INTO Assessments (competency_name, assessment_name, date_created)
        SELECT ?, ?, ?
        WHERE EXISTS (SELECT 1 FROM Competencies WHERE competency_name = ?)
    '''
    values = (competency_name, assessment_name, date_created, competency_name)

    cursor.execute(query, values)
    connection.commit()
    connection.close()

    return f"Assessment '{assessment_name}' was successfully added to the Competency '{competency_name}'. Wahoo! "

    
### Add an assessment result for a user for an assessment(this is like rocording test results for a user)
def add_assessment_result(assessment, score, date_taken, manager_administered, user_id):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = '''
        INSERT INTO Assessment_Results (user_id, assessment, score, date_taken, manager_administered)
        VALUES (?, ?, ?, ?, ?)
    '''
    values = (user_id, assessment, score, date_taken, manager_administered)

    cursor.execute(query, values)
    connection.commit()
    connection.close()

    return f"Assessment result added for User ID {user_id} in '{assessment}' assessment. Score: {score}. Date taken: {date_taken}. Administered by Manager: {manager_administered}."






## Editing Functions
### Edit a user's information function (also used for regular users)
def edit_user(user_id, column_to_update, new_value):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = f"""
    UPDATE Users
    SET {column_to_update} = ?
    WHERE user_id = ?
    """
    values = (new_value, user_id)
    cursor.execute(query, values)

    connection.commit()
    connection.close()

    return f"User '{user_id}' has been updated. {column_to_update} has been set to '{new_value}'."

### Edit a competency
def edit_competency(competency_id, column_to_update, new_value):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()


    query = f"""
    UPDATE Competencies
    SET {column_to_update} = ?
    WHERE competency_id = ?
    """
    values = (new_value, competency_id)
    cursor.execute(query, values)

    connection.commit()
    connection.close()

    return f"Competency '{competency_id}' has been updated. {column_to_update} has been set to '{new_value}'."

### Edit an assessment
def edit_assessment(assessment_name, column_to_update, new_value):

    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()


    query = f"""
    UPDATE Assessments
    SET {column_to_update} = ?
    WHERE assessment_name = ?
    """
    values = (new_value, assessment_name)
    cursor.execute(query, values)

    connection.commit()
    connection.close()

    return f"Assessment '{assessment_name}' has been updated. {column_to_update} has been set to '{new_value}'."

### Edit an assessment result
def edit_assessment_result(user_id, column_to_update, new_value):

    if new_value.upper() == 'SCORE':
        new_value = int(input("what is the updated score? "))

    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()


    query = f"""
    UPDATE Assessment_Results
    SET {column_to_update} = ?
    WHERE user_id = ?
    """
    values = (new_value, user_id)
    cursor.execute(query, (values))

    connection.commit()
    connection.close()

    return f"Assessment result'{column_to_update}' has been updated. {column_to_update} has been set to '{new_value}'."





## Delete Function
### delete an assessment result (hard time getting print statements to work, but the function does delete correctly)
def delete_assessment_result(user_id, assessment, date_taken):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    read_cust_query = "SELECT * FROM Assessment_Results WHERE user_id = ? AND assessment = ? AND date_taken = ?"
    cursor.execute(read_cust_query, (user_id, assessment, date_taken))
    existing_user = cursor.fetchone()

    if existing_user is None:
        connection.close()
        return f"user with ID {user_id} not found in the database."

    confirm = input(f"are you sure you want to delete '{assessment}' {date_taken} associated with user {user_id} from the database? (Y/N): ")
    if confirm.upper() == "Y":

        delete_query = "DELETE FROM Assessment_Results WHERE user_id = ? AND assessment = ? AND date_taken = ?"
        cursor.execute(delete_query, (user_id, assessment, date_taken))
        connection.commit()
        connection.close()
        print(f"Assessment {assessment} taken {date_taken} associated with user {user_id} has been deleted from the database.")

    elif confirm.upper() == 'N':
        connection.close()
        print(f"Phew that was a close call! Operation canceled.")
    
    else:
        connection.close()
        print(f"Invalid input, operation canceled.")






## Export functions
### Export competency report by competency and users
def export_competency_report_by_competency_and_users():
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = """
        SELECT Users.first_name, Users.last_name, Assessment_Results.*
        FROM Users
        JOIN Assessment_Results ON Users.user_id = Assessment_Results.user_id
        ORDER BY Users.user_id;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()

    connection.close()

    with open('competency_report_by_competency_and_users.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['First Name', 'Last Name', 'User ID', 'Assessment', 'Score', 'Date Taken', 'Manager Administered'])
        csv_writer.writerows(rows)

    print("Competency report by competency and users exported successfully.")


### Export competency report for a single user
def export_competency_report_for_single_user(user_id):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    query = """
        SELECT Users.first_name, Users.last_name, Assessment_Results.*
        FROM Users
        JOIN Assessment_Results ON Users.user_id = Assessment_Results.user_id
        WHERE Users.user_id = ?;
    """
    
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    connection.close()

    with open('competency_report_for_single_user.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['First Name', 'Last Name', 'User ID', 'Assessment', 'Score', 'Date Taken', 'Manager Administered'])
        csv_writer.writerows(rows)

    print(f"Competency reports for 'User {user_id}' exported successfully.")















## Import function
### import assessment results from a CSV file
def import_assessment_results_from_csv(csv_filename):
    connection = sqlite3.connect("updated_capstone_database.db")
    cursor = connection.cursor()

    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) 

        for row in csv_reader:
            user_id, assessment_name, score, date_taken, manager_administered = row
            query = """
                INSERT INTO Assessment_Results (user_id, assessment, score, date_taken, manager_administered)
                VALUES (?, ?, ?, ?, ?);
            """
            values = (user_id, assessment_name, score, date_taken, manager_administered)
            cursor.execute(query, values)

    connection.commit()
    connection.close()
    print("Assessment results imported successfully.")








# MENU functions.... Manager & User

# Manager menu function
def manager_menu():
    while True:
        manager_input = input('''
        *** Welcome to the secret MANAGER menu ***
        Please select one of the options below...
        [V]iew from different options
        [A]dd user, new competency, new assessment, assessment result
        [E]dit user info, competency, assessment, assessment result
        [D]elete assessment result
        [X] Export all reports to a CSV file
        [I]mport assessment results from a CSV file
        [L]og-out
                              
        ''')

    # various view functions
        if manager_input.upper() == 'V':
            while True:
                view_input = input('''
            *** Welcome to the viewing menu ***
            Please select one of the options below...
            [1] View all users
            [2] Search for users by first name or last name
            [3] View a report of all users and their competency levels for a given competency
            [4] view a competency level report for an individual user
            [5] view a list of assessments for a given user
            [B] go back to the previous page
            [Q]uit
                                
            ''')

                if view_input == '1':
                    result = view_all_users('Users')
                    print(result)

                elif view_input == '2':
                    search_by = input('search by [F]irst name or [L]ast name? ').upper()
                    if search_by == 'F':
                        first_name = input("What is the user's first name? ")
                        result = first_name_search_user('Users', first_name )
                        print(result)
                    elif search_by == 'L':
                        last_name = input("What is the user's last name? ")
                        result = last_name_search_user('Users', last_name)
                        print(result)

                elif view_input == '3':
                    result = view_all_users_and_competency_level()
                    print(result)

                elif view_input == '4':
                    first_name = input("What is the user's first name? ")
                    last_name = input("What is the user's last name? ")
                    result = view_individual_user_and_competency_level(first_name, last_name)
                    print(result)

                elif view_input == '5':
                    first_name = input("What is the user's first name? ")
                    last_name = input("What is the user's last name? ")
                    result = view_assessments_individual_user(first_name, last_name)
                    print(result)

                elif view_input.upper() == 'B':
                    break

                elif view_input.upper() == 'Q':
                    quit()
            
                else:
                    print('Invalid input, please try again.')


        # various adding functions
        elif manager_input.upper() == 'A':
            while True:
                add_input = input('''
            *** Welcome to the adding menu ***
            Please select one of the options below...
            [1] Add a user
            [2] Add a new competency
            [3] Add a new assessment to a competency
            [4] Add an assessment result to a user for an assessment
            [B] go back to the previous page     
            [Q]uit
                                
            ''')
                if add_input == '1':
                    first_name = input("What is the user's first name? ")
                    last_name = input("What is the user's last name? ")
                    phone_number = input("What is the user's phone number? ")
                    email = input("What is the user's email? ")
                    password = input("What will be the user's password? ").lower()
                    hashed_password = hash_password(password)
                    active = 1
                    date_created = input("What is today's date? (mm-dd-yyyy) ")
                    hire_date = input("What day was the user hired? (mm-dd-yyyy) ")
                    user_type = input("Will this person be a user or a manager? ")
                    add_user(first_name, last_name, phone_number, email, hashed_password, active, date_created, hire_date, user_type)
                
                elif add_input == '2':
                    competency_name = input('What will be the name of the new competency? ')
                    date_created = input('What is the date the competency was created? (mm-dd-yyyy) ')
                    add_competency(competency_name, date_created)

                elif add_input == '3':
                    competency_name = input('What is the name of the existing competency? ')
                    assessment_name = input('What would you like to name the assessment? ')
                    date_created = input('What is the date this assessment was created? (mm-dd-yyyy) ')
                    add_assessment_to_competency(competency_name, assessment_name, date_created)
                    
                elif add_input == '4':
                    user_id = input("What is the user_id of the user who took the assessment? ")
                    assessment_name = input('what is the name of the assessment? ')
                    score = input('what is the score the user received? (0-4) ')
                    date_taken = input('What was the date this assessment was taken? (mm-dd-yyyy) ')
                    manager_administered = input('What is the name of the manager whom administered this assessment? ')

                    add_assessment_result(assessment_name, score, date_taken, manager_administered, user_id)

                elif add_input.upper() == 'B':
                    break

                elif add_input.upper() == 'Q':
                    quit()

                else:
                    print('invalid input, please try again')


        # various editing functions
        elif manager_input.upper() == 'E':
            while True:
                edit_input = input('''
            *** Welcome to the adding menu ***
            Please select one of the options below...
            [1] Edit a user's info
            [2] Edit a competency
            [3] Edit an assessment
            [4] Edit an assessment result
            [B] go back to the previous page
            [Q]uit program

            ''')
                if edit_input == '1':
                    user_id = input("what is the person's user id? ")
                    column_to_update = input("what is the name of the column you would like to update? ")
                    if column_to_update == 'password':
                        new_password = input("Enter your new password: ")
                        hashed_password = hash_password(new_password)
                        edit_user(user_id, 'password', hashed_password)
                    else:
                        new_value = input("what is the new value you would like to input? ")
                        edit_user(user_id, column_to_update, new_value)

                elif edit_input == '2':
                    competency_id = input("what is the id of the competency you would like to update? ")
                    column_to_update = input("what is the name of the column you would like to update? ")
                    new_value = input("what is the new value you would like to input? ")
                    edit_competency(competency_id, column_to_update, new_value)

                elif edit_input == '3':
                    assessment_name = input("what is the assessment_name you would like to update? ")
                    column_to_update = input("what is the name of the column you would like to update? ")
                    new_value = input("what is the new value you would like to input? ")
                    edit_assessment(assessment_name, column_to_update, new_value)

                elif edit_input == '4':
                    user_id = input("what is the person's user id? ")
                    column_to_update = input("what is the name of the column you would like to update? ")
                    new_value = input("what is the new value you would like to input? ")
                    edit_assessment_result(user_id, column_to_update, new_value)

                elif edit_input.upper() == 'B':
                    break

                elif edit_input.upper() == 'Q':
                    quit()

                else:
                    print('Invalid input, please try again.')

        # delete assessment result function
        elif manager_input.upper() == 'D':
            while True:
                delete_input = input('''
            *** Welcome to the deleting menu ***
            Please select one of the options below...
            [Y]es, I want to delete an assessment result
            [B] go back to the previous page
            [Q]uit program
                                   
            ''')
                
                if delete_input.upper() == 'Y':
                    user_id = input('What is the user_id of the person associated with the assessment result? ')
                    assessment = input('What is the assessment you would like to delete? ')
                    date_taken = input('What was the date this assessment was taken? (mm-dd-yyyy) ')
                    delete_assessment_result(user_id, assessment, date_taken)

                elif delete_input.upper() == 'B':
                    break
                
                elif delete_input.upper() == 'Q':
                    quit()

                else:
                    print('Invalid input, please try again.')


        # Export reports to a CSV file
        elif manager_input.upper() == 'X':
            while True:
                export_input = input('''
            *** Welcome to the Exporting menu ***
            Please select one of the options below...
            [1] Export all competency reports by competency and users
            [2] Export a competency report for a single user
            [B] go back to the previous page
            [Q]uit program
                                    
            ''')
                if export_input == '1':
                    export_competency_report_by_competency_and_users()
                
                elif export_input == '2':
                    user_id = input("What is the user_id of the person who's competency reports you'd like to export? ")
                    export_competency_report_for_single_user(user_id)

                elif export_input.upper() == 'B':
                    break

                elif export_input.upper() == 'Q':
                    quit()

                else:
                    print('Invalid input, please try again.')

        # Import assessment results from a CSV file
        elif manager_input.upper() == 'I':
            while True:
                import_input = input('''
            *** Welcome to the deleting menu ***
            Please select one of the options below...
            [Y]es, I want to import assessment results
            [B] go back to the previous page
            [Q]uit program

            ''')
                if import_input.upper() == 'Y':
                    csv_filename = input('Please enter CSV file name that you would like to import: ')
                    import_assessment_results_from_csv(csv_filename)

                elif import_input.upper() =='B':
                    break

                elif import_input.upper() == 'Q':
                    quit()

                else:
                    print("Invalid input, please try again.")

        elif manager_input.upper() == 'L':
            print('You have successfully logged out, good bye!')
            break


# User menu function
def user_menu(user_id):
    while True:
        input_option = input('''
        *** Welcome to the User Menu ***
        Please select one of the options below...
        [V]iew your competency and assessment data
        [E]dit your first name, last name, or password
        [L]og-out
        [Q]uit program
                             
        ''')

        if input_option.upper() == 'V':
            view_user_assessment_data(user_id)


        elif input_option.upper() == 'E':
            while True:
                edit_input = input('''What would you like to edit?
                                [F] First name
                                [L] Last name
                                [P] Password 
                                [B] go back to the previous page
                                [Q] Quit program

                                ''')
                if edit_input.upper() == 'F':
                    new_first_name = input("Enter your new first name: ")
                    edit_user(user_id, "first_name", new_first_name)
                    print("First name updated!")

                elif edit_input.upper() == 'L':
                    new_last_name = input("Enter your new last name: ")
                    edit_user(user_id, "last_name", new_last_name)
                    print(f"Last name updated to {new_last_name}!")

                elif edit_input.upper() == 'P':
                    new_password = input("Enter your new password: ")
                    hashed_password = hash_password(new_password)
                    edit_user(user_id, "password", hashed_password)
                    print(f"Password updated to {new_password}!")

                elif edit_input.upper() == 'B':
                    break

                elif edit_input.upper() == 'Q':
                    quit()

                else:
                    print('Invalid input, please try again.')


        elif input_option.upper() == 'L':
            print('You have successfully logged out, have a nice day! ')
            break
        
        elif input_option.upper() == 'Q':
            quit()













# Initial statement

while True:
    statement = '''
    ** Capstone Database**
    [L] Login
    [Q] Quit

    '''
    print(statement)
    initial_input = input('Enter your choice: ')


    # Conditionals
    
    if initial_input.upper() == 'L':
        user_login()
    
    elif initial_input.upper() == 'Q':
        quit()

    else:
        print('invalid input, try again')

    
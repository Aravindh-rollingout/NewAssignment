# NewAssignment
The dependencies for this assignment have been listed in the requirements.txt. Run the following command to install all dependencies at once.

pip install -r requirements.txt

Following which it is recommended to create a virtual environment with the python version 3.8.

virtualenv NewAssignment/venv

Assignment Execution Steps:
1. Clone the repository from git@github.com:Aravindh-rollingout/NewAssignment.git

2. You will have to run the python file mail_executor_main with the following command
   python mail_executor_main

3. Make sure you have a MySQL DB with username and password as 'root' available for connection.

4. The terminal will directly open a window in your default browser requesting your authentication and permissions to view your mail messages.

5. Your auth details will be saved in a 'token.pickle' file under the NewAssignment directory which will be used for re-runs of the program or to refresh if the credentials become invalid.

5. Based on the rules and actions in the 'rules.json' file actions will be performed one after the other and will be stored in a MySQL Database in a Table 'HappyMails'. The connection is established through mysql.connector.

6. The ReadByUser (Mark As Read), Label (Add Label) and Archive (Archive Message) columns will be displayed in the console with values retrieved from the DB tables.

7. util.py contains the following constants allowed for all fields in rules.json:

    CONTAINS = 'Contains'
    NOT_CONTAINS = 'Does Not Contain'
    EQUALS = 'Equals'
    NOT_EQUALS = 'Does Not Equal'

    LESS_THAN = 'Less Than'
    GREATER_THAN = 'Greater Than'

    INTERVAL_DAYS = 'Days'
    INTERVAL_MONTHS = 'Months'

    PREDICATE_ANY = 'Any'
    PREDICATE_ALL = 'All'

    ACTION_MARK_AS_READ = 'Mark As Read'
    ACTION_ARCHIVE = 'Archive Message'
    ADD_LABEL = 'Add Label'

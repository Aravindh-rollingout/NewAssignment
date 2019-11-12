import mysql.connector

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

FROM_COL = 'FromAddress'
TO_COL = 'ToAddress'
SUB_COL = 'MailSub'
DATE_COL = 'DateReceived'


class DbConn:
    cur = None
    conn = None

    @staticmethod
    def connection():
        conn = mysql.connector.connect(host="127.0.0.1",
                                       user='root',
                                       password='root',
                                       auth_plugin='mysql_native_password',
                                       port='3306')
        DbConn.cur = conn.cursor()
        #print("Db connection eshabilshed sucessfuly", conn, cur)
        DbConn.conn = conn
        return DbConn.conn

from __future__ import print_function
from util import Util

import calendar
import base64
import email
from apiclient import errors


from db_conn import DbConn
from query_executor import QueryExecutor


db_obj = DbConn()


def main():

    service = Util.get_gmail_service()

    # Call the Gmail API for retrieving messages.
    #  Messages fetched are limited to 100 by Gmail by default
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages')

    # B.connect to DB
    db_obj.connection()

    # create new database and table
    create_db_and_table()

    # Get complete list of mail info for a single update query
    val = Util.get_value_list_from_messages(messages, service)

    # Insert the mail content to MySQL DB
    QueryExecutor.execute_insert_query(db_obj, val)

    # fetch ids based on rules.json
    rule_list = Util.get_rule_list_from_json()
    if not rule_list:
        print("Error parsing json file")
    # rule_list will be None if json file parsing fails

    # Update DB rule-wise
    rule_no = 1
    for rule in rule_list:
        print("Applying Rule filter: ", rule_no)
        rule_no += 1

        # Construct select for current rule to fetch IDs
        query, value_list, desc = Util.construct_select_query(rule)
        db_obj.cur.execute(query, value_list)
        records = db_obj.cur.fetchall()

        # perform action for selected Ids
        id_list = Util.get_id_list(records)
        query, value_list = Util.construct_update_query(rule, id_list)

        if len(id_list) > 0:
            value_list.extend(id_list)
            db_obj.cur.execute(query, value_list)
            db_obj.conn.commit()
            print("Name of executed Rule: ", desc)
        else:
            print("The rule'", desc, "'did not fetch any mails")

    # Printing all DB data after all rules have been applied
    QueryExecutor.execute_select_all_query(db_obj)


def create_db_and_table():
    QueryExecutor.create_database(db_obj, "happydata")
    QueryExecutor.use_database(db_obj, "happydata")
    QueryExecutor.drop_table(db_obj, "HappyMails")
    QueryExecutor.create_table(db_obj, "HappyMails")


if __name__ == '__main__':
    main()

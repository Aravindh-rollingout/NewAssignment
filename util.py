import os.path
import json
import pickle
import dateparser
from traceback import format_exc

from dateutil.relativedelta import *
from datetime import datetime
from apiclient import errors

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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


class Util:
    @staticmethod
    def get_rule_list_from_json():
        try:
            with open('NewAssignment/rules.json') as json_content:
                rule_content = json.load(json_content)
                rule_list = rule_content.get("rule_set")
            return rule_list
        except Exception:
            print("Error parsing json file. Please check location of .json file")
            return None

    @staticmethod
    def get_gmail_service():
        creds = None
        # to store authorization tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # When credentials are not present/valid refresh token or initiate user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'NewAssignment/credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                except FileNotFoundError as ex:
                    print(
                        "Error while parsing credentials json file. Please check name and location of credntials.json file. Find error details here")
                    print(format_exc())
                    return None

            # save credentials in .pickle file
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        return service

    @staticmethod
    def get_value_list_from_messages(messages, service):
        val = []
        for message in messages:
            full_mail = None
            mail_details = None
            full_mail, mail_details = Util.GetMessage(
                service=service, user_id='me', msg_id=message['id'])
            _id = mail_details['Id']
            _subject = mail_details['Subject']
            _from = mail_details['From']
            _to = mail_details['To']
            _date = mail_details['Date']
            dt_obj = dateparser.parse(_date[:-6])
            # date format error handling
            millisec = dt_obj.timestamp() * 1000
            val.append((_id, _from, _to, _subject, millisec))
        return val

    @staticmethod
    def construct_select_query(rule):
        value_list = []
        sub_query = ""
        try:
            desc = rule['description']
            pred = rule.get('predicate')
            sub_rules = rule.get('rules')
            clause = ' AND ' if (pred == PREDICATE_ALL) else ' OR '
            for sub_rule in sub_rules:
                field = sub_rule.get('field')
                condition = sub_rule.get('condition')
                if field == 'Date':
                    comparator = ' > ' if condition == LESS_THAN else ' < '

                    interval_value = sub_rule.get('value')
                    interval = sub_rule.get('interval')
                    month = 0
                    day = 0
                    if interval == INTERVAL_DAYS:
                        month = int(interval_value)
                    elif interval == INTERVAL_MONTHS:
                        day = int(interval_value)
                    else:
                        raise Exception("Input format for field is invalid.")
                    stamp = datetime.now() + relativedelta(months=-month, days=-day)
                    stamp_millis = int(stamp.timestamp() * 1000)
                    value_list.append(str(stamp_millis))
                elif field in ['To', 'From', 'Subject']:
                    value = '%' + sub_rule.get('value')+'%'
                    comparator = ' LIKE ' if condition == CONTAINS else ' NOT LIKE '
                    value_list.append(value)
                else:
                    raise Exception("Input format for field is invalid.")
                sub_query += Util.field_to_columns(field) + \
                    comparator + '%s' + clause

            query = "Select Id from HappyMails where " + \
                sub_query[:-len(clause)]
            return query, value_list, desc
        except Exception as ex:
            print("Input format invalid for rules.json")
            print(format_exc())
            return None, None, None

    @staticmethod
    def get_id_list(records):
        id_list = []
        for row in records:
            id_list.append(row[0])
        return id_list

    @staticmethod
    def construct_update_query(rule, id_list):
        value_list = []
        query = "UPDATE HappyMails SET "
        actions = rule.get('actions')
        for sub_action in actions:
            action = sub_action.get('action')
            if action == ADD_LABEL:
                query += ' Label = %s,'
                value_list.append(sub_action.get('label'))
            elif action == ACTION_MARK_AS_READ:
                query += ' ReadByUser = true,'
            elif action == ACTION_ARCHIVE:
                query += ' Archive = true,'

        format_strings = ','.join(['%s'] * len(id_list))
        query = query[:-1] + ' Where Id in (%s)' % format_strings
        return query, value_list

    @staticmethod
    def field_to_columns(field):
        switcher = {
            "Subject": SUB_COL,
            "From": FROM_COL,
            "To": TO_COL,
            "Date": DATE_COL
        }
        return switcher.get(field, "nothing")

    @staticmethod
    def GetMessage(service, user_id, msg_id):
        try:
            full_mail = service.users().messages().get(
                userId=user_id, id=msg_id).execute()

            payload = full_mail.get('payload')
            headers = payload.get('headers')

            email_details = {}
            email_details['Id'] = full_mail.get('id')

            for header in headers:
                if header.get('name') in ['Subject', 'From', 'To', 'Date']:
                    email_details[header.get('name')] = header.get('value')

            return full_mail, email_details
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

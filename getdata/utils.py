from __future__ import print_function
import os
import re
from bs4 import BeautifulSoup
import psycopg2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date,datetime
from marketing.models import Whatsapp_Groups
# To encode the data
from base64 import urlsafe_b64decode
import logging
logger = logging.getLogger(__name__)
#libraries for Options_play data extraction
import psycopg2
from django.http import JsonResponse
import json
import os

from coda_project.settings import dba_values ,source_target #dblocal,herokudev,herokuprod
# from testing.utils import dblocal,herokudev,herokuprod
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

#DB VARIABLES
# host,dbname,user,password=herokudev() #herokudev() #dblocal() #,herokuprod()
host,dbname,user,password=dba_values() #herokudev() #dblocal() #,herokuprod()

#DB VARIABLES
(source_host, source_dbname, source_user, source_password,target_db_path) = source_target()

def fetch_and_insert_data():
    (source_host, source_dbname, source_user, source_password, target_db_path) = source_target()

    # Connect to the source database
    source_conn = psycopg2.connect(
        host=source_host,
        dbname=source_dbname,
        user=source_user,
        password=source_password
    )
    source_cursor = source_conn.cursor()

    # Connect to the target database
    target_conn = psycopg2.connect(target_db_path)
    target_cursor = target_conn.cursor()

    source_tables = ['investing_shortput', 'investing_credit_spread', 'investing_covered_calls','investing_oversold']
    target_tables = ['investing_shortput', 'investing_credit_spread', 'investing_covered_calls','investing_oversold']

    try:
        # Iterate over source and target tables
        for source_table, target_table in zip(source_tables, target_tables):
            # Drop the target table if it exists
            target_cursor.execute(f"DROP TABLE IF EXISTS {target_table}")
            print("Target table dropped.")

            # Fetch the structure of the source table
            source_cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{source_table}'")
            columns = source_cursor.fetchall()

            # Get unique column names and their corresponding data types
            unique_columns = {}
            for column in columns:
                column_name = column[0]
                column_data_type = column[1]
                if column_name not in unique_columns:
                    unique_columns[column_name] = column_data_type

            create_table_query = f"CREATE TABLE {target_table} ("
            column_names = set()  # Track column names to avoid duplicates
            for column_name, column_data_type in unique_columns.items():
                if column_name not in column_names:
                    create_table_query += f"{column_name} {column_data_type}, "
                    column_names.add(column_name)
            create_table_query = create_table_query.rstrip(", ") + ")"

            # Create the target table
            target_cursor.execute(create_table_query)
            print("Target table created.")

            # Fetch data from the source table
            source_cursor.execute(f"SELECT * FROM {source_table}")
            rows = source_cursor.fetchall()

            # Insert data into the target table
            for row in rows:
                placeholders = "%s, " * len(row)
                placeholders = placeholders.rstrip(", ")
                target_cursor.execute(f"INSERT INTO {target_table} VALUES ({placeholders})", row)

        # Commit the changes in the target database
        target_conn.commit()

        print("Data transfer successful!")
    except Exception as e:
        print(f"Data transfer failed: {str(e)}")

    # Close the database connections
    source_conn.close()
    target_conn.close()


def compute_stock_values(stockdata):
    date_today = date.today()
    row = None  # Initialize row to None
    iv = rr = ar = sp = num_days = date_expiry = days_to_exp = None  # Initialize variables
    for current_row in stockdata:
        try:
            iv = current_row.Implied_Volatility_Rank
            rr = current_row.Raw_Return
            ar = current_row.Annualized_Return
            sp = current_row.Stock_Price
            num_days = current_row.Days_To_Expiry
            date_expiry = current_row.Expiry.date()  # Assign the datetime object directly
            days_to_exp = (date_expiry - date_today).days

            if isinstance(iv, str):
                iv = iv.replace('%', '')
            if isinstance(rr, str):
                rr = rr.replace('%', '')
            if isinstance(ar, str):
                ar = ar.replace('%', '')
            if isinstance(sp, str):
                sp = sp[1:]

            row = current_row  # Update row with the current valid row
        except (ValueError, AttributeError):
            continue

    return row, iv, rr, ar, sp, num_days, date_expiry, days_to_exp




def row_value():
    putsrow_value=3
    callsrow_value=3
    id_value=3
#     rows = Editable.objects.all()
#     if rows:
#         first_row = rows[0]  # get the first object in the QuerySet
#         putsrow_value = first_row.putsrow  # get the value of the `putsrow` field
#         callsrow_value = first_row.callsrow  # get the value of the `callsrow` field
#         id_value=first_row.id
#         # print(putsrow_value,callsrow_value,id_value)
#     else:
#         print("No objects found with id=1")
#         putsrow_value=1
#         callsrow_value=1
#         id_value=1
    return putsrow_value,callsrow_value,id_value

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credential_file='gapi/creds/robincredentials.json'
            # CURR_DIR = os.path.dirname(os.path.realpath(__file__))
            # credential_file=str(CURR_DIR)+'/credentials.json'  #may need backslash in windows
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
    return service

def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages']) 
    return messages

def get_message(service, msg_id):
    # mark that mail as read.
    msg = service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            'addLabelIds': [],
            'removeLabelIds': ['UNREAD'],
        },
        x__xgafv='1').execute()

    # get all the data about msg.
    msg = service.users().messages().get(userId='me', id=msg_id).execute()
    if not msg:
        logger.error('message not found!')
        return

    msg_payload = msg.get('payload')

    headers = msg_payload.get('headers')

    for header in headers:
        if header.get('name') == 'Date':
            received_date = header.get('value')
        if header.get('name') == 'From':
            from_mail = header.get('value')
        if header.get('name') == 'To':
            to_mail = header.get('value')
        if header.get('name') == 'Subject':
            subject = header.get('value')
    try:
        html_part = msg_payload.get('parts')[1]
        encoded_data = html_part.get('body').get('data')

        decoded_str = str(urlsafe_b64decode(encoded_data),'UTF-8')
        file_name = 'mail-'+msg_id+'.html'
        # html_path = os.path.join('stored_mails', file_name)

        # if not os.path.exists(html_path):

        with open(file_name, 'w+') as out:
            file = out.write(decoded_str)
    except:
        return 
    
    # return {
    #     'id': msg_id,
    #     'from_mail': from_mail,
    #     'to_mail': to_mail,
    #     'subject': subject,
    #     'text_mail': decoded_str,
    #     'received_date': received_date,
    #     'file_name' : file_name
    # }
    return file_name

#inserting data into database
def stock_data(symbol,action,qty, unit_price, total_price,date):
    #Database connection 
    try:
        with psycopg2.connect(
                                host = host,
                                dbname = dbname,
                                user = user,
                                password = password,
                                port = 5432
                            ) as conn:
            with conn.cursor() as cursor:
                #Creating database named RobinhoodEmailInfo
                creating_db = '''CREATE TABLE IF NOT EXISTS getdata_stockmarket (
                    symbol varchar(250),
                    action varchar(200),
                    qty int,
                    unit_price float,
                    total_price float,
                    date date
                )'''
                cursor.execute(creating_db)

                insert_query = '''INSERT INTO getdata_stockmarket(symbol,action,qty,unit_price,total_price,date) VALUES (%s,%s,%s,%s,%s,%s)'''
                values = (symbol,action, qty,unit_price,total_price,date)
                cursor.execute(insert_query,vars = values)
    except Exception as err:
        print(err)


#inserting data into cryptodatabase
def crypto_data(symbol,action,unit_price, total_price,date):
    try:
        with psycopg2.connect(
                                host = host,
                                dbname = dbname,
                                user = user,
                                password = password,
                                port = 5432
                            ) as conn:
            with conn.cursor() as cursor:
                #getdata_cryptomarket
                creating_db = '''CREATE TABLE IF NOT EXISTS getdata_cryptomarket(
                    symbol varchar(250),
                    action varchar(200),
                    unit_price float,
                    total_price float,
                    date date
                )'''
                cursor.execute(creating_db)

                insert_query = '''INSERT INTO getdata_cryptomarket(symbol,action,unit_price,total_price,date) VALUES (%s,%s,%s,%s,%s)'''
                values = (symbol,action,unit_price,total_price,date)
                cursor.execute(insert_query,vars = values)
    
        
    except Exception as err:
        print(err)

def getdata(file):
    '''Get the html content'''
    try:
        HTMLFile = open(file, "r")
    
        # Reading the file
        index = HTMLFile.read()
        #parsing into beautifulsoup
        soup = BeautifulSoup(index, 'html.parser')
    except:
        return 0
    return soup

#Fetch the header option
def GetSubject(soup):
    '''Profile Name'''
    try:
        name = soup.find_all('div', {'class' : 'mj-section-rh'})
        subject = name[1].find('div').text
        sub_pat = re.compile(r'Order Executed|Option Order Executed')
        sub_match = sub_pat.findall(subject)
        subject = sub_match[0].strip()
        print(subject)

        return subject
    except:
        return None

def populate_table_from_json_file(file_path):
    try:
        # Read the text file containing JSON data
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        #  Extract data into a list of dictionaries
        data_list = [{
        	# 'id': item.get('id', 'default_id'),
            # 'id': item.get('id', 'default_id')[:-15] + '-' + item.get('id', 'default_id')[-15:] if item.get('id', None) and len(item.get('id', '')) > 15 else item.get('id', 'default_id'), 
            'id': item['id'][:-15] + ('-' if '-' not in item['id'][-15:] else '') + item['id'][-15:],
        	'name': item.get('name', 'default_name'), 
        	'participants': len(item.get('participants', []))
        } for item in json_data['data']]

        # Delete all existing entries in the table
        # Whatsapp_Groups.objects.all().delete()
        # return

        # Insert or update data from data_list
        # for data in data_list:
        #     Whatsapp_Groups.objects.create(
        #         group_id=data['id'],
        #         group_name=data['name'],
        #         participants=data['participants']
        #     )
        for data in data_list:
            Whatsapp_Groups.objects.update_or_create(
                group_id=data['id'],
                defaults={
                    'group_name': data['name'],
                    'participants': data['participants']
                }
            )

    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

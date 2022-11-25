from __future__ import print_function
import os
import pandas as pd
import re
from dateutil import parser
from bs4 import BeautifulSoup
import psycopg2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# To encode the data
from base64 import urlsafe_b64decode
import logging
logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

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
            CURR_DIR = os.path.dirname(os.path.realpath(__file__))
            credential_file=str(CURR_DIR)+'/credentials.json'  #may need backslash in windows
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
                            host = 'localhost',
                            dbname = 'Stock Price Index',
                            user = 'postgres',
                            password = 'Honnappa001@500',
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

                insert_query = '''INSERT INTO stockmarket VALUES (%s,%s,%s,%s,%s,%s)'''
                values = (symbol,action, qty,unit_price,total_price,date)
                cursor.execute(insert_query,vars = values)
    except Exception as err:
        print(err)


#inserting data into cryptodatabase
def crypto_data(symbol,action,unit_price, total_price,date):
    #Database connection 
    try:
        with psycopg2.connect(
                            host = 'localhost',
                            dbname = 'Stock Price Index',
                            user = 'postgres',
                            password = 'Honnappa001@500',
                            port = 5432
                            ) as conn:
            with conn.cursor() as cursor:
                #Creating database named RobinhoodEmailInfo
                creating_db = '''CREATE TABLE IF NOT EXISTS getdata_cryptomarket(
                    symbol varchar(250),
                    action varchar(200),
                    unit_price float,
                    total_price float,
                    date date
                )'''
                cursor.execute(creating_db)

                insert_query = '''INSERT INTO cryptomarket VALUES (%s,%s,%s,%s,%s)'''
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
        print(subject)
        print("-----------------------------")
        return subject
    except:
        return None

#fetch order executed information
def get_executed_info(soup, header):
    try:
        name = soup.find_all('div', {'class' : 'mj-section-rh'})
        text_body = name[2].find_all('div')
        text = str(text_body[2])

        open_buy_pat = re.compile(r'(buy|open|close)')
        open_buy_match = open_buy_pat.findall(text)
        try:
            action = open_buy_match[0]
        except:
            action = 'open'

        print(f'---------  open/buy/close option -----')
        print(f'                {action}')
        print(f'--------------------------------------')

        #Quantity of stocks sold
        qty_pat = re.compile(r"\s\d+\s")
        qty_match = qty_pat.findall(text)
        qty = qty_match[0]

        if len(qty_match) > 1:
            #selling stocks
            print(f'Quantifty of stocks sold : {qty}')

            #Company name
            cmp_pat = re.compile(r"[A-Z]+\s")
            cmp_match = cmp_pat.findall(text)
            symbol = cmp_match[0].strip()
            print(f"Symbol : {symbol}")

            #average price and Total price
            price_pat = re.compile(r'[$]\d+[0-9.]+\d+')
            price_match = price_pat.findall(text)
            if len(price_match) <= 2:
                avg_price = price_match[0].replace('$','')
                total_price = price_match[1].replace('$','')
            else:
                avg_price = price_match[1].replace('$','')
                total_price = price_match[2].replace('$','')

            try:
                total_price = float(total_price.replace(',',''))
            except:
                total_price = float(total_price)

            #strike_price
            try:
                avg_price = float(avg_price.replace(',',''))
            except:
                avg_price = float(avg_price)

            print(f'avg price and total_price: {avg_price} {total_price}')

            #Date Primary Key
            date_pat = re.compile(r'(januarary|February|March|April|May|June|July|August|September|October|November|December)+')
            date_match = date_pat.finditer(text)
            for i in date_match:
                start = i.start()
            date = (parser.parse(text[start:],fuzzy_with_tokens = True,ignoretz = True))[0]
            print(f'date : {date}')
            print('--------------------------------------')
            stock_data(symbol=symbol,action=action,qty=qty,unit_price=avg_price, total_price=total_price,date=date)

        #CryptoTrade
        else:
            print(f'Action : {action}')
            #Company
            cmp_pat = re.compile(r'of\s\w+')
            cmp_match = cmp_pat.findall(text)
            symbol = cmp_match[0].split(' ')
            symbol = symbol[-1].strip()

            #Selling price and buying price
            price_pat = re.compile(r'[$]\d+[0-9.]+\d+')
            price_match = price_pat.findall(text)

            unit_price = price_match[1].replace('$','')
            total_price = price_match[0].replace('$','')

            try:
                unit_price = float(unit_price.replace(',',''))
            except:
                unit_price = float(unit_price)
            
            try:
                total_price = float(total_price.replace(',',''))
            except:
                toal_price = float(total_price)
            
            #Date Primary Key
            date_pat = re.compile(r'(januarary|February|March|April|May|June|July|August|September|October|November|December)+')
            date_match = date_pat.finditer(text)
            for i in date_match:
                start = i.start()
            date = (parser.parse(text[start:],fuzzy_with_tokens = True,ignoretz = True))[0]
            print(f'date : {date}')
            print('--------------------------------------')
            crypto_data(symbol=symbol,action = action,unit_price=unit_price,total_price=total_price, date= date)

    except Exception as err:
        print(err)

        
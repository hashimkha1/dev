from __future__ import print_function
import os
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


#libraries for Options_play data extraction
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import psycopg2
import time

from coda_project.settings import dblocal,herokudev,herokuprod
# from testing.utils import dblocal,herokudev,herokuprod
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

#DB VARIABLES
host,dbname,user,password=dblocal() #,herokudev(),herokuprod()

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

#Stock Price Index info
def get_stock_price(soup, header):
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

        #selling stocks
        print(f'Quantifty of stocks sold : {qty}')

        #Company name
        cmp_pat = re.compile(r"[A-Z]+\s")
        cmp_match = cmp_pat.findall(text)
        symbol = cmp_match[0].strip()
        print(f"Symbol : {type(symbol)}")

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
        print(f'date : {type(date)}')
        print('--------------------------------------')
        stock_data(symbol=symbol,action=action,qty=qty,unit_price=avg_price, total_price=total_price,date=date)
    except Exception as err:
        print(err)

def get_crypto_price(soup, header):
    try:
        print("Crypto ------------------")
        name = soup.find_all('div', {'class' : 'mj-section-rh'})
        text_body = name[2].find_all('div')
        text = str(text_body[2])

        sell_buy_pat = re.compile(r'(buy|sell)')
        sell_buy_match = sell_buy_pat.findall(text)
        action = sell_buy_match[0]
        print(f'Action : {action}')

        #Company
        cmp_pat = re.compile(r'of\s\w+')
        cmp_match = cmp_pat.findall(text)
        symbol = cmp_match[0].split(' ')
        symbol = symbol[-1].strip()
        print(f'Symbol : {symbol}')

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
            total_price = float(total_price)
        
        #Date Primary Key
        date_pat = re.compile(r'(januarary|February|March|April|May|June|July|August|September|October|November|December)+')
        date_match = date_pat.finditer(text)
        for i in date_match:
            start = i.start()
        date = (parser.parse(text[start:],fuzzy_with_tokens = True,ignoretz = True))[0]
        print(f'date : {type(date)}')
        
        crypto_data(symbol=symbol,action = action,unit_price=unit_price,total_price=total_price, date= date)
    except Exception as err:
        print(f"Alert Message : {err}")

#Optionsplay Data extraction funcationality
#credit_spread functionality
def dump_data_credit(values):
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
                creating_db = '''CREATE TABLE IF NOT EXISTS getdata_creadspread (
                    Symbol TEXT,
                    Strategy TEXT,
                    Type TEXT,
                    Price TEXT,
                    Sell_Strike TEXT,
                    Buy_Strike TEXT,
                    Expiry TEXT,
                    Premium TEXT,
                    Width TEXT,
                    Prem_Width TEXT,
                    Rank TEXT,
                    Earnings_Date TEXT
                )'''
                cursor.execute(creating_db)

                insert_query = '''INSERT INTO getdata_creadspread(Symbol,Strategy, Type,Price,Sell_Strike,Buy_Strike,Expiry,Premium,Width,Prem_Width,Rank,Earnings_Date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                # values = (Symbol,Action, Expiry, Days_To_Expiry,	Strike_Price,	Mid_Price,	Bid_Price,	Ask_Price,Implied_Volatility_Rank,	Earnings_Date,	Earnings_Flag,	Stock_Price,Raw_Return,	Annualized_Return,	Distance_To_Strike)
                cursor.execute(insert_query,vars= values)

    except Exception as err:
        print(err)

def main_cread_spread():
    path = r"Chrome_driver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.headless = True
    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Chrome(executable_path = path, options=options)
    driver.get('https://www.optionsplay.com/hub/credit-spread-file')

    driver.maximize_window()
    time.sleep(5)
    driver.implicitly_wait(4)
    form = driver.find_element(By.TAG_NAME, 'form')
    form.find_element(By.ID, 'Login').send_keys('info@codanalytics.net')
    form.find_element(By.ID, 'Password').send_keys('!ZK123sebe')

    btn = driver.find_element(By.XPATH, '//*[@id="applicationHost"]/div/div/div[3]/div/div/div/div[1]/div/div/form/div[4]/button')
    btn.send_keys(Keys.ENTER)
    time.sleep(4)
    table = driver.find_element(By.XPATH, '//*[@id="CreditSpreadFile"]')
    tbody = table.find_element(By.XPATH,'//*[@id="CreditSpreadFile"]/tbody')
    rows = tbody.find_elements(By.TAG_NAME,'tr')
    rows = len(rows)
    # //*[@id="CreditSpreadFile"]/tbody/tr[1]
    # //*[@id="CreditSpreadFile"]/tbody/tr[1]/td[15]
    time.sleep(5)
    for row in range(1,rows+1):
        values = []
        for col in range(1,13):
            path = '//*[@id="CreditSpreadFile"]/tbody/tr[{}]/td[{}]'.format(row,col)
            value = driver.find_element(By.XPATH,path).text
            values.append(value)
            print(value, end =' ')
        dump_data_credit(tuple(values))
        print('')

#covered_calls
def dump_data_covered_calls(values):
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
                creating_db = '''CREATE TABLE IF NOT EXISTS getdata_coveredcalls(
                    Symbol varchar(250),
                    Action varchar(200),
                    Expiry varchar(200),
                    Days_To_Expiry varchar(200),
                    Strike_Price varchar(200),
                    Mid_Price varchar(200),
                    Bid_Price varchar(200),
                    Ask_Price varchar(200),
                    Implied_Volatility_Rank varchar(200),
                    Earnings_Date varchar(200),
                    Earnings_Flag BOOL,
                    Stock_Price varchar(200),
                    Raw_Return varchar(200),
                    Annualized_Return varchar(200),
                    Distance_To_Strike varchar(200)
                )'''
                cursor.execute(creating_db)

                insert_query = '''INSERT INTO getdata_coveredcalls(Symbol,Action, Expiry, Days_To_Expiry,	Strike_Price,	Mid_Price,Bid_Price,Ask_Price,Implied_Volatility_Rank,	Earnings_Date,	Earnings_Flag,	Stock_Price,Raw_Return,	Annualized_Return,	Distance_To_Strike) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                # values = (Symbol,Action, Expiry, Days_To_Expiry,	Strike_Price,	Mid_Price,	Bid_Price,	Ask_Price,Implied_Volatility_Rank,	Earnings_Date,	Earnings_Flag,	Stock_Price,Raw_Return,	Annualized_Return,	Distance_To_Strike)
                cursor.execute(insert_query,vars = values)

    except Exception as err:
        print(err)

def main_covered_calls():
    path = r"Chrome_driver.exe"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("start-maximized")
    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Chrome(executable_path = path, options=options)
    driver.get('https://www.optionsplay.com/hub/covered-calls')

    driver.maximize_window()
    time.sleep(2)
    driver.implicitly_wait(2)
    form = driver.find_element(By.TAG_NAME, 'form')
    form.find_element(By.ID, 'Login').send_keys('info@codanalytics.net')
    form.find_element(By.ID, 'Password').send_keys('!ZK123sebe')

    btn = driver.find_element(By.XPATH, '//*[@id="applicationHost"]/div/div/div[3]/div/div/div/div[1]/div/div/form/div[4]/button')
    btn.send_keys(Keys.ENTER)
    time.sleep(3)
    table = driver.find_element(By.XPATH, '//*[@id="coveredCalls"]')
    tbody = table.find_element(By.XPATH,'//*[@id="coveredCalls"]/tbody')
    rows = tbody.find_elements(By.TAG_NAME,'tr')
    rows = len(rows)
    # //*[@id="coveredCalls"]/tbody/tr[1]
    # //*[@id="coveredCalls"]/tbody/tr[1]/td[15]
    time.sleep(4)
    for row in range(1,rows+1):
        values = []
        for col in range(1,16):
            path = '//*[@id="coveredCalls"]/tbody/tr['+str(row)+']/td['+str(col)+']'
            value = driver.find_element(By.XPATH,path).text.strip()
            values.append(value)

        value = float(values[14].replace('%',''))
        if values[11] == 'N' and value < 30:
            dump_data_covered_calls(tuple(values))

#short put
def dump_data_short_put(values):
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
                creating_db = '''CREATE TABLE IF NOT EXISTS getdata_shortput (
                    Symbol varchar(250),
                    Action varchar(200),
                    Expiry varchar(200),
                    Days_To_Expiry varchar(200),
                    Strike_Price varchar(200),
                    Mid_Price varchar(200),
                    Bid_Price varchar(200),
                    Ask_Price varchar(200),
                    Implied_Volatility_Rank varchar(200),
                    Earnings_Date varchar(200),
                    Earnings_Flag BOOL,
                    Stock_Price varchar(200),
                    Raw_Return varchar(200),
                    Annualized_Return varchar(200),
                    Distance_To_Strike varchar(200)
                )'''
                cursor.execute(creating_db)

                insert_query = '''INSERT INTO getdata_shortput(Symbol,Action, Expiry, Days_To_Expiry,	Strike_Price,	Mid_Price,Bid_Price,Ask_Price,Implied_Volatility_Rank,	Earnings_Date,	Earnings_Flag,	Stock_Price,Raw_Return,	Annualized_Return,	Distance_To_Strike) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                # values = (Symbol,Action, Expiry, Days_To_Expiry,	Strike_Price,	Mid_Price,	Bid_Price,	Ask_Price,Implied_Volatility_Rank,	Earnings_Date,	Earnings_Flag,	Stock_Price,Raw_Return,	Annualized_Return,	Distance_To_Strike)
                cursor.execute(insert_query,vars = values)

    except Exception as err:
        print(err)

def main_shortput():
    path = r"Chrome_driver.exe"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("start-maximized")
    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Chrome(executable_path = path, options=options)
    driver.get('https://www.optionsplay.com/hub/short-puts')

    driver.maximize_window()
    time.sleep(2)
    driver.implicitly_wait(2)
    form = driver.find_element(By.TAG_NAME, 'form')
    form.find_element(By.ID, 'Login').send_keys('info@codanalytics.net')
    form.find_element(By.ID, 'Password').send_keys('!ZK123sebe')

    btn = driver.find_element(By.XPATH, '//*[@id="applicationHost"]/div/div/div[3]/div/div/div/div[1]/div/div/form/div[4]/button')
    btn.send_keys(Keys.ENTER)
    time.sleep(3)
    table = driver.find_element(By.XPATH, '//*[@id="shortPuts"]')
    tbody = table.find_element(By.XPATH,'//*[@id="shortPuts"]/tbody')
    rows = tbody.find_elements(By.TAG_NAME,'tr')
    rows = len(rows)
    # //*[@id="shortPuts"]/tbody/tr[1]
    # //*[@id="shortPuts"]/tbody/tr[1]/td[15]
    time.sleep(4)
    for row in range(1,rows+1):
        values = []
        for col in range(1,16):
            path = '//*[@id="shortPuts"]/tbody/tr['+str(row)+']/td['+str(col)+']'
            value = driver.find_element(By.XPATH,path).text.strip()
            values.append(value)
        
        value = float(values[14].replace('%',''))
        if values[11] == 'N' and value < 30:
            dump_data_short_put(tuple(values))
    
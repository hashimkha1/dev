from __future__ import print_function
import os
import re
import glob
import psycopg2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date,datetime
# To encode the data
from base64 import urlsafe_b64decode
import logging
logger = logging.getLogger(__name__)
#libraries for Options_play data extraction
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import psycopg2

import yfinance as yf
import pandas as pd
import numpy as np

from coda_project.settings import dba_values ,source_target 
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

#DB VARIABLES
# host,dbname,user,password=herokudev() #herokudev() #dblocal() #,herokuprod()
host,dbname,user,password=dba_values() #herokudev() #dblocal() #,herokuprod()

#DB VARIABLES
(source_host, source_dbname, source_user, source_password,target_db_path) = source_target()

# accessing YAHOO Finance information

def fetch_or_compute_risk_statistics(ticker_symbol):
    ticker_data = yf.Ticker(ticker_symbol)
    
    try:
        # Fetching the historical data for the ticker symbol
        historical_data = ticker_data.history(period="10y")
        
        # Check if the fetched data is empty or not
        if historical_data.empty:
            raise ValueError(f"No historical data available for {ticker_symbol}")
        
        # Ensure the index is a DatetimeIndex and then localize the timezone
        if not isinstance(historical_data.index, pd.DatetimeIndex):
            historical_data.index = pd.to_datetime(historical_data.index)
        historical_data.index = historical_data.index.tz_convert("UTC")

        # Beta Calculation (Here, we're taking SPY as the benchmark):
        benchmark = yf.Ticker('SPY').history(period="10y")['Close'].pct_change().dropna()
        benchmark.index = pd.to_datetime(benchmark.index)  # Ensure the date index is in datetime format
        
        stock_returns = historical_data['Close'].pct_change().dropna()
        
        beta = stock_returns.cov(benchmark) / benchmark.var()
        
        # Mean Annual Return
        annual_return = (stock_returns.mean() + 1) ** 252 - 1

        # Annual Standard Deviation
        annual_std_dev = stock_returns.std() * np.sqrt(252)
        
        # Sharpe Ratio (using a 0.03 risk-free rate for illustration; adjust as needed)
        sharpe_ratio = (annual_return - 0.03) / annual_std_dev

        return beta, annual_return, annual_std_dev, sharpe_ratio
    except Exception as e:
        # Logging or printing the error can help with debugging
        print(f"Error fetching data for {ticker_symbol}: {str(e)}")
        return None, None, None, None  # Return a tuple of Nones

def fetch_data_util(category,ticker_symbol,number_years=None):
    ticker_data = yf.Ticker(ticker_symbol)
    # beta,annual_return,annual_std_dev,sharpe_ratio=fetch_or_compute_risk_statistics(ticker_symbol)
    if category == 'history':
        # If you want historical data:
        data = ticker_data.history(period=f"{number_years}y")
    elif category == 'financials':
        # If you want financial statements:
        data = ticker_data.financials
     
    elif category == 'risk':
        # Check if Yahoo provides the required risk information directly
        full_data = ticker_data.info
        if 'beta' in full_data:
            # Fetch risk details directly from Yahoo's info if available
            data = {
                'beta': full_data.get('beta', None),
                'annual_return': full_data.get('annualReturn', None),  # Update the key if different
                'annual_std_dev': full_data.get('annualStdDev', None), # Update the key if different
                'sharpe_ratio': full_data.get('sharpeRatio', None),    # Update the key if different
            }
        else:
            print(f"Failed to fetch or compute risk statistics for {ticker_symbol}")
            data = {}

    elif category == 'statistics':
        # Fetch key statistics and then extract only valuation measures
        full_data = ticker_data.info
        ''' ============== All finacial terms =============   '''
        ''' financial_terms = ["shareHolderRightsRisk", "overallRisk", "payoutRatio", "beta", "forwardPE", 
            "profitMargins", "sharesShort", "shortRatio", "bookValue", "trailingEps", "forwardEps", "pegRatio", 
            "enterpriseToRevenue", "enterpriseToEbitda", "totalCashPerShare", "ebitda", "totalDebt", 
            "quickRatio", "currentRatio", "revenuePerShare", "returnOnAssets", "operatingCashflow", 
            "revenueGrowth", "grossMargins", "ebitdaMargins", "operatingMargins"] '''
        ''' ====== old data show when click on symbol ========='''
        ''' valuation_keys = ['marketCap', 'enterpriseValue', 'trailingPE', 'forwardPE', 'priceToSalesTrailing12Months', 
                          'enterpriseToRevenue', 'enterpriseToEbitda', 'priceToBook'] ''' 
        valuation_keys = ["overallRisk", "sharesShort", "enterpriseToEbitda", "ebitda", "quickRatio", "currentRatio", "revenueGrowth"]
        data = {key: full_data.get(key, None) for key in valuation_keys}
        print(data)
    else:
        data = "Category not recognized"
    
    return data

def load_xel_data_to_postgres(xel_folder_path,table_name):
    # Create a PostgreSQL connection and cursor
    conn = psycopg2.connect(
        host=source_host,
        dbname=source_dbname,
        user=source_user,
        password=source_password
    )
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS {} (
        event_time TIMESTAMP,
        session_id INTEGER,
        event_name TEXT,
        column1 TEXT,
        column2 TEXT,
        column3 TEXT
    );
    '''.format(table_name)
    cursor.execute(create_table_query)

    # Get a list of XEL files in the folder
    xel_files = glob.glob(os.path.join(xel_folder_path, '*.xel'))
    for xel_file in xel_files:
        with open(xel_file, 'r') as file:
            # Read the contents of the XEL file
            xel_content = file.read()

            # Extract events using regular expressions
            events = re.findall(r'<Event event_time="(.*?)" session_id="(.*?)" event_name="(.*?)">(.*?)</Event>', xel_content, re.DOTALL)

            # Process each event
            for event in events:
                event_time, session_id, event_name, column_data = event

                # Extract column values
                column_values = {}
                columns = re.findall(r'<Column name="(.*?)" value="(.*?)"', column_data)
                for column_name, column_value in columns:
                    column_values[column_name] = column_value

                # Insert the event data into the database table
                insert_query = '''
                INSERT INTO {} (event_time, session_id, event_name, column1, column2, column3)
                VALUES (%s, %s, %s, %s, %s, %s)
                '''.format(table_name)
                cursor.execute(insert_query, (event_time, session_id, event_name, column_values.get('Column1'), column_values.get('Column2'), column_values.get('Column3')))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


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

    source_tables = ['investing_shortput', 'investing_credit_spread', 'investing_covered_calls']
    target_tables = ['investing_shortput', 'investing_credit_spread', 'investing_covered_calls']

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

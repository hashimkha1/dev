import logging
import logging.handlers
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import subprocess
import pandas as pd
import datetime
import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise

user_name= os.environ.get('USER')
password= os.environ.get('PASSWORD')
host= os.environ.get('HOST')
port='5432'
db_name=os.environ.get('DATABASE')

def dump_data(df, choice):
    connection_string = f'postgresql://{user_name}:{password}@{host}:{port}/{db_name}'

    # Create a database engine
    engine = create_engine(connection_string)

    # Create a sessionmaker
    Session = sessionmaker(bind=engine)

    if choice == 'CreditSpreadFile':
        df = pd.read_csv('data\credit_spread.csv')
        # Write DataFrame to PostgreSQL database using SQLAlchemy
        df.to_sql('Optionsplay_Credit_spread', engine, if_exists='replace', index=False)

    elif choice == 'coveredCalls':
        df = pd.read_csv('data\covered_calls.csv')
        df.to_sql('Optionsplay_Covered_calls', engine, if_exists='replace', index=False)

    else:
        df = pd.read_csv('data\shortput.csv')
        df.to_sql('OptionsPlay_short_put', engine, if_exists='replace', index=False)


def parse_data(html, choice):
    '''Extract the data table'''
    result = subprocess.run(["playwright", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    #Extracting table from table
    table = soup.select(f'table#{choice}')[0]
    # print(table)

    columns = table.find('thead').find_all('th')

    print(len(columns))
    df = pd.read_html(str(table))[0]

    #Removing last row
    df = df.iloc[:-1,:]
    
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str[:255]

    print(df.head())
    #saving into database
    return df
    
def extract_data(url, choice):
    '''Extract the HTML code'''
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=50, chromium_sandbox = False)
        page = browser.new_page()
        
        page.goto(url=url)
        page.fill(
           'input#Login', 'info@codanalytics.net' 
        )
        page.fill(
            'input#Password', '!ZK123sebe'
        )

        #click on submit button
        page.click("button[type=submit]")

        # Wait to load the HTML template
        try:
            page.wait_for_timeout(30000)
        except:
            page.wait_for_timeout(60000)

        if choice == 'CreditSpreadFile':
            html = page.inner_html('//*[@id="CreditSpreadFile_wrapper"]')

        elif choice == 'coveredCalls':
            html = page.inner_html('//*[@id="coveredCalls_wrapper"]')

        else:
            html = page.inner_html('//*[@id="shortPuts_wrapper"]')
        return html

#Executing the options play tables
def main_covered_calls():
    try:
        urls = {
            'coveredCalls' : 'https://www.optionsplay.com/hub/covered-calls'
        }

        html = extract_data(url=urls['coveredCalls'], choice='coveredCalls')
        data = parse_data(html, choice='coveredCalls')
        data.to_csv('data/covered_calls.csv')
        dump_data(df=data, choice='coveredCalls', index=False)
    except Exception as err:
        print(err)
    
    

def main_shortput():
    try:
        urls = {
            'shortPuts' : 'https://www.optionsplay.com/hub/short-puts'
        }

        html = extract_data(url=urls['shortPuts'], choice='shortPuts')
        data = parse_data(html, choice='shortPuts')
        data.to_csv('data/shortput.csv')
        dump_data(df=data, choice='shortPuts', index=False)
    except Exception as err:
        print(err)

def main_cread_spread():
    try:
        urls = {
            'CreditSpreadFile' : 'https://www.optionsplay.com/hub/credit-spread-file'
        }

        html = extract_data(url=urls['CreditSpreadFile'], choice='CreditSpreadFile')
        data = parse_data(html, choice='CreditSpreadFile')  
        data.to_csv('data/credit_spread.csv', index=False)
        dump_data(df=data, choice='CreditSpreadFile') 
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main_cread_spread()
    main_shortput()
    main_covered_calls()
    # send_email()
    time = datetime.datetime.now()
    logger.info(f'Code Executed : {time}')

        

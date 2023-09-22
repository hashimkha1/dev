import os
import pickle
from base64 import urlsafe_b64decode
from django.shortcuts import get_object_or_404, redirect, render

import os
import pandas as pd
from bs4 import BeautifulSoup
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import logging
logger = logging.getLogger(__name__)


# If you modified scopes, delete the file token.json and re-authenticate!
SCOPES = ('https://mail.google.com/',)
current_dir = os.path.dirname(os.path.abspath(__file__))

client_id = os.environ.get('GAPI_CLIENT_ID')
project_id = os.environ.get('GAPI_PROJECT_ID')
client_secret = os.environ.get('GAPI_CLIENT_SECRET')
DEFAULT_CREDENTIALS = {"installed":{"client_id": client_id,"project_id": project_id,"auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_secret": client_secret,"redirect_uris": ["http://localhost"]}}
# DEFAULT_CREDENTIALS = os.path.join(current_dir, 'creds/credentials.json')

DEFAULT_TOKEN = os.path.join(current_dir, 'creds/token.pickle')


def get_service(scopes=SCOPES, service_name='gmail', service_version='v1', token=DEFAULT_TOKEN, credentials=DEFAULT_CREDENTIALS):
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(token):
        with open(token, "rb") as token_file:
            creds = pickle.load(token_file)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes)
            flow = InstalledAppFlow.from_client_config(credentials, scopes)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(token, "wb") as token_file:
            pickle.dump(creds, token_file)
    return build(service_name, service_version, credentials=creds)


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
    # pprint(headers)

    # to_mail = msg_payload.get('headers')[0].get('value')
    # received_date = msg_payload.get('headers')[1].get('value')
    # from_mail = msg_payload.get('headers')[6].get('value')

    for header in headers:
        if header.get('name') == 'Date':
            received_date = header.get('value')
        if header.get('name') == 'From':
            from_mail = header.get('value')
        if header.get('name') == 'To':
            to_mail = header.get('value')
        if header.get('name') == 'Subject':
            subject = header.get('value')

    html_part = msg_payload.get('parts')[1]
    encoded_data = html_part.get('body').get('data')
    decoded_str = str(urlsafe_b64decode(encoded_data), 'UTF-8')

    file_name = 'mail-' + str(msg_id) + '.html'
    html_path = os.path.join(current_dir, 'stored_mails', file_name)

    if not os.path.exists(html_path):
        with open(html_path, 'w+') as out:
            out.write(decoded_str)

    text_part = msg.get('payload').get('parts')[0]
    encoded_data = text_part.get('body').get('data')
    decoded_str = str(urlsafe_b64decode(encoded_data), 'UTF-8')

    # return only what we want.
    return {
        'id': msg_id,
        'from_mail': from_mail,
        'to_mail': to_mail,
        'subject': subject,
        'file_name': file_name,
        'full_path': html_path,
        'text_mail': decoded_str,
        'received_date': received_date,
    }

    '''Importing the required libraries'''


def getdata(file):
    '''Get the html content'''
    HTMLFile = open(file, "r")
  
    # Reading the file
    index = HTMLFile.read()

    #parsing into beautifulsoup
    soup = BeautifulSoup(index, 'html.parser')
    return soup

def GetProfileName(soup):
    '''Profile Name'''
    try:
        profile = soup.find('div', {'class' : 'text profile-name'}).text
        return profile.strip()
    except:
        pass
    try:
        profile = soup.find('div', {'class' : 'text'}).text
        return profile.strip()
    except:
        pass

def gettable_data(soup):
    '''Table Data which contains the detailed information'''
    dict_ = {}
    dict_['Destination'] = 'cashapp'
    try:
        parent_tag = soup.find('td', {'class': 'divider-top detail-list-padding'})
        table_data = parent_tag.find_all('tr', {'class' : 'detail-row'})
        for i in table_data:
            label = i.find('div', {'class' : 'label'}).text.strip()
            value = i.find('div', {'class' : 'value'}).text.strip()
            try:
                if label == 'Amount':
                    dict_[label] = value
                if label == 'Identifier':
                    dict_[label] = value
                if label == 'To':
                    dict_[label] = value
                if label == 'From':
                    dict_[label] = value
                else:
                    pass
            except:
                dict_['Amount'] = '0'

    except TypeError as e:
        print(f"Error caused {e}")

    return dict_

def cashapp_main(path):
    if path.endswith('html'):
        dict_ = {
                'From' : "None",
                'Amount' : 0,
                'To' : "None"
                }
        try:
            soup = getdata(path)
            name = GetProfileName(soup)
            print(name)
            table_data = gettable_data(soup)
            # table_data['name'] = name
            # table_data['path'] = path
            # if table_data['name'] == 'Uber':
            #     table_data['To'] = 'Uber'
            #     table_data['From'] = 'CHRISTOPHER C MAGHAS'
            dict_['To'] = table_data['To']
            dict_['From'] = table_data['From']
            dict_['Amount'] = table_data['Amount']
            return dict_
        except:
            return dict_
    else:
        pass



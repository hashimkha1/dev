import os
import pickle

import logging
logger = logging.getLogger(__name__)

from base64 import urlsafe_b64decode

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If you modified scopes, delete the file token.json and re-authenticate!
SCOPES = ('https://mail.google.com/',)
current_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CREDENTIALS = os.path.join(current_dir, 'creds/credentials.json')
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
            flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes)
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
        userId = 'me',
        id = msg_id,
        body = {
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
    to_mail = msg_payload.get('headers')[0].get('value')
    received_date = msg_payload.get('headers')[1].get('value')
    from_mail = msg_payload.get('headers')[6].get('value')

    html_part = msg_payload.get('parts')[1]
    encoded_data = html_part.get('body').get('data')
    decoded_str = str(urlsafe_b64decode(encoded_data), 'UTF-8')

    file_name = 'mail-'+ str(msg_id) + '.html'
    html_path = os.path.join(current_dir, 'temp_mails', file_name)
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
        'file_name': file_name,
        'full_path': html_path,
        'text_mail': decoded_str,
        'received_date': received_date,
    }

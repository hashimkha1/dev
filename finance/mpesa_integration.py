import requests
from django.conf import settings

def generate_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    data = response.json()
    return data.get('access_token')

def initiate_payment(phone_number, amount, reference):
    token = generate_token()
    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password': settings.MPESA_PASSWORD,
        'Timestamp': settings.MPESA_TIMESTAMP,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': settings.MPESA_SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackURL': settings.MPESA_CALLBACK_URL,
        'AccountReference': reference,
        'TransactionDesc': 'Payment for something',
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

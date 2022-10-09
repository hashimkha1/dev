import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello there!", from_="whatsapp:+14155238886", to="whatsapp:+15005550006"
)

print(message.sid)

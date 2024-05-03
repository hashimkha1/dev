import tweepy
import logging

from celery import shared_task
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
# importing modules
from accounts.models import CustomerUser, TaskGroups
from application.models import UserProfile

# importing utils & Views
from main.utils import download_image
# from main.context_processors import image_view

logger = logging.getLogger(__name__)
User = get_user_model()

JOB_SUPPORTS = ["job support", "job_support", "jobsupport"]
ACTIVITY_LIST = ['BOG', 'BI Sessions', 'DAF Sessions', 'Project', 'web sessions']

# @shared_task(name="TrainingLoanDetectionHistory")
# def TrainingLoanDetectionHistory():
#     default_payment_fees = Default_Payment_Fees.objects.all().first()
#     employee = CustomerUser.objects.filter(Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True),is_active=True)
#     for emp in employee:
#         emp_id = emp.id
#         if Task.objects.filter(employee=emp).exists():
#             tasks = Task.objects.all().filter(employee=emp)
#             if TrainingLoan.objects.filter(user=emp).exists():
#                 trainingloan = TrainingLoan.objects.filter(user=emp)
#                 total_detection_amount = trainingloan.aggregate(Sum('detection_amount'))
#                 total_detection_amount = total_detection_amount['detection_amount__sum']
#                 loan_amount = float(default_payment_fees.loan_amount)
#                 if float(total_detection_amount) < loan_amount:
#                     total_pay = 0
#                     for task in tasks:
#                         total_pay = total_pay + task.get_pay
#                     total_loan = Decimal(total_pay) * Decimal("0.2")
#                     total_loan += Decimal(total_detection_amount)
#                     # loan = Decimal(total_pay) * Decimal("0.2")
#                     # loan = round(loan, 2)
#
#                     if total_loan > loan_amount:
#                         loan = Decimal(loan_amount) - Decimal(total_detection_amount)
#                         balance = 0
#                         if LoanUsers.objects.filter(user=emp).exists():
#                             LoanUsers.objects.filter(user=emp).update(is_loan=False)
#                         LBandLSDetection(emp_id)
#
#                         # else:
#                         #     LoanUsers.objects.create(is_loan=False,user=emp)
#                     else:
#                         loan = Decimal(total_pay) * Decimal("0.2")
#                         balancing_amount = TrainingLoan.objects.filter(user=emp).order_by('-id')[0]
#                         balancing_amount = balancing_amount.balance_amount
#                         balance = Decimal(balancing_amount) - loan
#                         LBandLSDetection(emp_id)
#
#                     loan = round(loan, 2)
#                     TrainingLoan.objects.create(
#                         user=emp,
#                         total_earnings_amount=total_pay,
#                         detection_amount=loan,
#                         category="Credit",
#                         balance_amount=balance,
#                         training_loan_amount=default_payment_fees
#                     )
#             else:
#                 total_pay = 0
#                 for task in tasks:
#                     total_pay = total_pay + task.get_pay
#
#                 loan = Decimal(total_pay) * Decimal("0.2")
#                 loan = round(loan, 2)
#                 loan_amount = Decimal(default_payment_fees.loan_amount)
#                 balance = loan_amount - loan
#                 TrainingLoan.objects.create(user=emp,total_earnings_amount=total_pay,detection_amount=loan, category="Credit", balance_amount=balance, training_loan_amount=default_payment_fees)
#                 LBandLSDetection(emp_id)


# @shared_task(name="advertisement_whatsapp")
# def advertisement_whatsapp(request):
#     runwhatsapp(request)

# def advertisement_whatsapp(request):
#     whatsapp_items = Whatsapp.objects.all()
#     image_url = None
#     # Get a list of all group IDs from the Whatsapp model
#     # group_ids = list(whatsapp_items.values_list('group_id', flat=True))
#     group_ids = list(whatsapp_items.values_list('group_id', flat=True))
#     # group_ids = ["120363047226624982@g.us"]

#     # Get the image URL and message from the first item in the Whatsapp model
#     if whatsapp_items:
#         image_url = whatsapp_items[0].image_url
#         message = whatsapp_items[0].message
#     else:
#         message = "local testing"
#     product_id = whatsapp_items[0].product_id
#     screen_id = whatsapp_items[0].screen_id
#     token = whatsapp_items[0].token
#     # product_id = os.environ.get('MYAPI_PRODUCT_ID')
#     # screen_id = os.environ.get('MYAPI_SCREEN_ID')
#     # token = os.environ.get('MYAPI_TOKEN_ID')
#     # Loop through all group IDs and send the message to each group
#     for group_id in group_ids:
#         print("Sending message to group", group_id)

#         # Set the message type to "text" or "media" depending on whether an image URL is provided
#         conn = http.client.HTTPSConnection("api.maytapi.com")
#         if image_url:
#             # Set the length of the random string
#             length = 10
#             # Generate a random string of lowercase letters and digits
#             random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
#             payload = json.dumps({
#                 "to_number": group_id,
#                 "type": "media",
#                 "message": image_url,
#                 "filename": random_string
#             })
#         else:
#             payload = json.dumps({
#                 "to_number": group_id,
#                 "type": "text",
#                 "message": message
#             })

#         headers = {
#             'accept': 'application/json',
#             'x-maytapi-key': token,
#             'Content-Type': 'application/json'
#         }
#         conn.request("POST", f"/api/{product_id}/{screen_id}/sendMessage", payload, headers)
#         res = conn.getresponse()
#         data = res.read()
#         print(data.decode("utf-8"))
#         # if response.status_code == 200:
#         if json.loads(data).get('success') is True:
#             print("Message sent successfully!")
#             message = f"Hi, {request.user}, your messages have been sent to your groups."
#         else:
#             # print("Error sending message:", response.text)
#             message = data
#     # Display a success message on the page
#     context = {"title": "WHATSAPP", "message": message}
#     return render(request, "main/errors/generalerrors.html", context)

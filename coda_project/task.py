from celery import shared_task
from django.http import HttpResponse
from django.shortcuts import render
from mail.custom_email import send_email
from management.models import Task, TaskHistory,LBandLS
from accounts.models import CustomerUser
from datetime import datetime, timedelta
from decimal import Decimal
from finance.models import LoanUsers, TrainingLoan, Default_Payment_Fees
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from application.models import UserProfile
# from accounts.utils import employees

from finance.models import PayslipConfig

from management.utils import paytime, payinitial, loan_computation, bonus, best_employee, additional_earnings, paymentconfigurations
from main.utils import image_view,download_image

from management.models import Advertisement
import tweepy
# importing modules
import urllib.request

import logging

from management.views import loan_update_save, normalize_period

from management.utils import deductions

from gapi.gservices import get_service, search_messages
from getdata.models import ReplyMail
from mail.custom_email import send_reply
# from django.core.management import call_command
import tweepy
# importing modules
import urllib.request
from PIL import Image

logger = logging.getLogger(__name__)

User = get_user_model()

@shared_task(name="task_history")
def dump_data():
    try:
        bulk_object = []
        get_data = Task.objects.all()
        for data in get_data:
            bulk_object.append(
                TaskHistory(
                    group=data.group,
                    category=data.category,
                    employee=data.employee,
                    activity_name=data.activity_name,
                    description=data.description,
                    slug=data.slug,
                    duration=data.duration,
                    point=data.point,
                    mxpoint=data.mxpoint,
                    mxearning=data.mxearning,
                    submission=data.submission,
                    is_active=data.is_active,
                    featured=data.featured,
                )
            )
        TaskHistory.objects.bulk_create(bulk_object)
        get_data.update(point=0)
        return True
    except Exception:
        return False

@shared_task(name="SendMsgApplicatUser")
def SendMsgApplicatUser():
  """Description: Aplicat user login after not upload section will send msg"""
  applicants = CustomerUser.objects.filter(is_applicant=True,is_active=True,profile__upload_a__exact='',profile__upload_b__exact='',profile__upload_c__exact='')
  for data in applicants:
    date_joined = data.date_joined
    after_10_date = timedelta(days = 10)
    pastdate = date_joined.date() + after_10_date
    presentdate = datetime.now().date()
    print('pastdate-->',pastdate)
    print("presentdate-->",presentdate)
    if pastdate == presentdate:
        subject = "No active mail"
        # to = data.email
        # content = f"""
        #         <span><h3>Hi {data.username},</h3>you applied for a position in CODA, kindly let us know of your progress, you can login at the following link to proceed with your interview </span>"""
        # email_template(subject,to,content)
        send_email(
            category=data.category,
            to_email=(data.email,),
            subject=subject,
            html_template='email/SendMsgApplicatUser.html',
            context={'username': data.first_name}
        )


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

def LBandLSDetection(emp):
    LBandLsAmount = 1000
    userprofile = UserProfile.objects.get(user_id=emp)
    if userprofile.laptop_status == True:
        if LBandLS.objects.filter(user_id=emp).exists():
            lbandls = LBandLS.objects.get(user_id=emp)
            lbandls = lbandls.laptop_bonus + float(LBandLsAmount)
            LBandLS.objects.filter(user_id=emp).update(laptop_bonus=lbandls)
        else:
            LBandLS.objects.create(user_id=emp,laptop_bonus=LBandLsAmount)
    elif userprofile.laptop_status == False:
        if LBandLS.objects.filter(user_id=emp).exists():
            # lbandlsfilter = LBandLS.objects.filter(user_id=emp)
            lbandls = LBandLS.objects.get(user_id=emp)
            laptop_service_amount = lbandls.laptop_service
            # laptop_service_amount = lbandlsfilter.aggregate(Sum('laptop_service'))
            # laptop_service_amount = laptop_service_amount['laptop_service__sum']
            if float(laptop_service_amount) < 20000:
                laptop_service_amt = lbandls.laptop_service + float(LBandLsAmount)
                LBandLS.objects.filter(user_id=emp).update(laptop_service=laptop_service_amt)
        else:
            LBandLS.objects.create(user_id=emp,laptop_service=LBandLsAmount)


@shared_task(name="TrainingLoanDeduction")
def TrainingLoanDeduction():
    from tqdm import tqdm
    # employee = CustomerUser.objects.filter(Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True),is_active=True)
    employee = CustomerUser.objects.filter(is_employee=True,is_staff=True,is_active=True)
    employee_number = CustomerUser.objects.filter(is_employee=True,is_staff=True,is_active=True).count()
    # (employee_subcategories,active_employees)=employees()
    # print(employee,employee_number)
    # print(active_employees)
    for emp in employee:
        # print(emp)
        # LBLS = LBandLS.objects.filter(user=emp)
        # lbandls = LBandLS.objects.get(user_id=employee)
        # today, year, month, day, deadline_date = paytime()
        # task_obj = Task.objects.filter(submission__contains=year)
        # userprofile = UserProfile.objects.get(user_id=emp)
        # print(userprofile)
        tasks = Task.objects.all().filter(employee=emp)
        user_data = TrainingLoan.objects.filter(user=emp, is_active=True)
        loantable = TrainingLoan
        payslip_config = paymentconfigurations(PayslipConfig, emp)
        # mxearning, points = payinitial(tasks)
        total_pay = Decimal(0)
        for task in tasks:
            total_pay = total_pay + task.get_pay
        # Deductions
        # print(loan_amount,loan_payment,balance_amount)
        # loan_payment = round(total_pay * payslip_config.loan_repayment_percentage, 2)
        loan_amount, loan_payment, balance_amount = loan_computation(total_pay, user_data, payslip_config)
        # print(loan_amount, loan_payment, balance_amount)
        logger.debug(f'balance_amount: {balance_amount}')
        # loan_update_save(loantable, user_data, emp, total_pay, payslip_config)
        

@shared_task(name="replies_job_mail")
def search_job_mail():
    search_results=[]
    search_query = ['jobs role', 'hiring', 'recruitment']
    # search_query = 'ranjeetgup19@gmail.com is:unread'
    service = get_service()  # default service with default scope, gmail-v1
    if not service:
        logger.error('No Service!')
    for search in search_query:
        se=search+" is:unread"
        search_results += search_messages(service, se)

    # search_results += search_messages(service, search_query)
    # search_results_len = len(search_results)

    if not search_results:
        logger.error('NO SEARCH RESULTS FOUND !')
        # return render(request,'main/snippets_templates/interview_snippets/result.html',{"message":message})
    else:
        for result in search_results:
            print(result.get('id'))
            try:
                msg_dict = send_reply(service=service, msg_id=result.get('id'))
                if msg_dict:
                    try:
                        ReplyMail.objects.create(
                            id=msg_dict.get('id'),
                            from_mail=msg_dict.get('from_mail'),
                            to_mail=msg_dict.get('to_mail'),
                            subject=msg_dict.get('subject'),
                            text_mail=msg_dict.get('text_mail'),
                            received_date=msg_dict.get('received_date')
                        )
                    except Exception as e:
                        logger.error('error on adding new record!')
                        logger.error('error msg is ' + str(e))
                        logger.error(f'msg id is: msg_dict.get("id")')
            except Exception as e:
                logger.error('error msg is ' + str(e))

                # from django.core.management import call_command
import tweepy
import requests
from management.models import Advertisement

"""

Twitter and Facebook AD management Scripts below

"""

@shared_task(name="advertisement")
def advertisement():
    #This function will post the latest tweet
    print("TWIITER TWESTING FUNCT")
    context = Advertisement.objects.all().first()
    apiKey = context.twitter_api_key 
    apiSecret = context.twitter_api_key_secret
    accessToken = context.twitter_access_token
    accessTokenSecret = context.twitter_access_token_secret
    # 3. Create Oauth client and set authentication and create API object
    oauth = tweepy.OAuthHandler(apiKey, apiSecret)
    oauth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(oauth)

    # 4. upload media
    value=None
    url = "https://www.codanalytics.net/static/main/img/service-3.jpg"
    image_path=download_image(url)
    print(image_path)

    # upload media
    media = api.media_upload(image_path)

    # post tweet with media_id
    description = context.post_description #'This is my tweet with an image'
    api.update_status(status=description, media_ids=[media.media_id])

# This function will post the latest Facebook Ad
@shared_task(name="advertisement_facebook")
def advertisement_facebook():
    pass
    # facebook_page_id = context.facebook_page_id
    # access_token = context.facebook_access_token
    # url = "https://graph.facebook.com/{}/photos".format(facebook_page_id)
    # msg = context.post_description
    # image_location = context.image
    # payload = {
    #     "url": image_location,
    #     "access_token": access_token,
    #     "message": msg,
    # }

    # # Send the POST request
    # requests.post(url, data=payload)

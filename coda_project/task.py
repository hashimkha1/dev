from celery import shared_task

from mail.custom_email import send_email
from management.models import Task, TaskHistory,LBandLS
from accounts.models import CustomerUser
from datetime import datetime, timedelta
#from management.utils import email_template
from decimal import Decimal
from finance.models import LoanUsers, TrainingLoan, Default_Payment_Fees
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from application.models import UserProfile

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
        send_email(category=data.category, to_email=(data.email,), subject=subject, html_template='email/SendMsgApplicatUser.html', context={'username': data.first_name})


@shared_task(name="TrainingLoanDetectionHistory")  
def TrainingLoanDetectionHistory():
    default_payment_fees = Default_Payment_Fees.objects.all().first()

    employee = CustomerUser.objects.filter(Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True),is_active=True)
    for emp in employee:
        emp_id = emp.id
        if Task.objects.filter(employee=emp).exists():
            tasks = Task.objects.all().filter(employee=emp)
            if TrainingLoan.objects.filter(user=emp).exists():
                trainingloan = TrainingLoan.objects.filter(user=emp)
                total_detection_amount = trainingloan.aggregate(Sum('detection_amount'))
                total_detection_amount = total_detection_amount['detection_amount__sum']
                loan_amount = float(default_payment_fees.loan_amount)
                if float(total_detection_amount) < loan_amount:
                    total_pay = 0
                    for task in tasks:
                        total_pay = total_pay + task.get_pay
                    total_loan = Decimal(total_pay) * Decimal("0.2")
                    total_loan += Decimal(total_detection_amount)
                    # loan = Decimal(total_pay) * Decimal("0.2")
                    # loan = round(loan, 2)

                    if total_loan > loan_amount:
                        loan = Decimal(loan_amount) - Decimal(total_detection_amount)
                        balance = 0
                        if LoanUsers.objects.filter(user=emp).exists():
                            LoanUsers.objects.filter(user=emp).update(is_loan=False)
                        LBandLSDetection(emp_id)

                        # else:
                        #     LoanUsers.objects.create(is_loan=False,user=emp)
                    else:
                        loan = Decimal(total_pay) * Decimal("0.2")
                        balancing_amount = TrainingLoan.objects.filter(user=emp).order_by('-id')[0]
                        balancing_amount = balancing_amount.balance_amount
                        balance = Decimal(balancing_amount) - loan
                        LBandLSDetection(emp_id)

                    loan = round(loan, 2)

                    TrainingLoan.objects.create(user=emp,total_earnings_amount=total_pay,detection_amount=loan, category="Credit",balance_amount=balance,training_loan_amount=default_payment_fees)
            else:

                total_pay = 0
                for task in tasks:
                    total_pay = total_pay + task.get_pay

                loan = Decimal(total_pay) * Decimal("0.2")
                loan = round(loan, 2)
                loan_amount = Decimal(default_payment_fees.loan_amount)
                balance = loan_amount - loan
                TrainingLoan.objects.create(user=emp,total_earnings_amount=total_pay,detection_amount=loan, category="Credit", balance_amount=balance, training_loan_amount=default_payment_fees)
                LBandLSDetection(emp_id)

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

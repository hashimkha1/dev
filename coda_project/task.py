from celery import shared_task
from mail.custom_email import send_email
from management.models import Task, TaskHistory,LBandLS
from accounts.models import CustomerUser
from datetime import datetime, timedelta
from decimal import Decimal
from finance.models import LoanUsers, TrainingLoan, Default_Payment_Fees
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from application.models import UserProfile

from finance.models import PayslipConfig

from management.utils import paytime, payinitial, loan_computation, bonus, best_employee, additional_earnings, paymentconfigurations


import logging

from management.views import loan_update_save, normalize_period

from management.utils import deductions

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

    employee = CustomerUser.objects.filter(Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True),is_active=True)
    print(employee)
    for emp in tqdm(employee):
        print(emp)
        userprofile = UserProfile.objects.get(user_id=emp)
        tasks = Task.objects.all().filter(employee=emp)
        LBLS = LBandLS.objects.filter(user=emp)
        user_data = TrainingLoan.objects.filter(user=emp, is_active=True)
        loantable = TrainingLoan
        # lbandls = LBandLS.objects.get(user_id=employee)
        payslip_config = paymentconfigurations(PayslipConfig, emp)
        today, year, month, day, deadline_date = paytime()
        task_obj = Task.objects.filter(submission__contains=year)
        mxearning, points = payinitial(tasks)
        total_pay = Decimal(0)
        for task in tasks:
            total_pay = total_pay + task.get_pay
        # Deductions
        # print(loan_amount,loan_payment,balance_amount)
        # loan_payment = round(total_pay * payslip_config.loan_repayment_percentage, 2)
        loan_amount, loan_payment, balance_amount = loan_computation(total_pay, user_data, payslip_config)
        print(loan_amount, loan_payment, balance_amount)
        logger.debug(f'balance_amount: {balance_amount}')
        loan_update_save(loantable, user_data, emp, total_pay, payslip_config)
        food_accomodation, computer_maintenance, health, kra = deductions(payslip_config, total_pay)
        # print("what is this----->",loan_update_save(loantable,user_data,employee,total_pay,payslip_config))
        userprofile = UserProfile.objects.get(user_id=emp)
        if userprofile.laptop_status == True:
            laptop_saving = Decimal(0)
            if LBandLS.objects.filter(user=emp).exists():
                lbandls = LBandLS.objects.get(user_id=emp)
                laptop_bonus = lbandls.laptop_bonus
            else:
                laptop_bonus = Decimal(0)
        else:
            laptop_bonus = Decimal(0)
            if LBandLS.objects.filter(user=emp).exists():
                lbandls = LBandLS.objects.get(user_id=emp)
                laptop_saving = lbandls.laptop_service
            else:
                laptop_saving = Decimal(0)
        laptop_bonus = round(Decimal(laptop_bonus), 2)
        laptop_saving = round(Decimal(laptop_saving), 2)
        # laptop_bonus,laptop_saving=lap_save_bonus(userprofile,LBLS,lbandls)
        # ====================Bonus Section=============================
        pointsearning, Night_Bonus, holidaypay, yearly = bonus(tasks, total_pay, payslip_config)
        # print(pointsearning,Night_Bonus,holidaypay,yearly)

        EOM = Decimal(0.00)  # employee of month
        EOQ = Decimal(0.00)  # employee of quarter
        EOY = Decimal(0.00)  # employee of year
        if month == 12:
            task_obj = Task.objects.filter(submission__contains=year)
            logger.debug(f'task_obj: {task_obj}')
            eoy_users = best_employee(task_obj)
            if (emp,) in eoy_users:
                logger.info('this employee is EOY!')
                EOY = payslip_config.eoy_bonus
        elif month % 3 == 0:
            task_obj = Task.objects.filter(Q(submission__contains=normalize_period(year, month - 2))
                                           | Q(submission__contains=normalize_period(year, month - 1))
                                           | Q(submission__contains=normalize_period(year, month)))
            logger.debug(f'task_obj: {task_obj}')
            eoq_users = best_employee(task_obj)
            user_tuple = (emp.username,)
            logger.debug(f'eoq_users: {eoq_users}')
            logger.debug(f'user_tuple: {user_tuple}')

            if user_tuple in eoq_users:
                logger.info('this employee is EOQ!')
                EOQ = payslip_config.eoq_bonus
                logger.debug(f'EOQ: {EOQ}')
        else:
            task_obj = Task.objects.filter(submission__contains=normalize_period(year, month))
            logger.debug(f'task_obj: {task_obj}')
            eom_users = best_employee(task_obj)
            if (employee,) in eom_users:
                logger.info('this employee is EOM!')
                EOM = payslip_config.eom_bonus
        # ====================Summary Section=============================
        total_deduction, total_bonus = additional_earnings(user_data, tasks, total_pay, payslip_config)
        total_bonus = total_bonus + EOM + EOQ + EOY
        # print("total is---->", total_deduction,total_bonus)
        # Net Pay
        total_value = total_pay + total_bonus
        net = total_value - total_deduction
        round_off = round(net) - net
        net_pay = net + round_off
        logger.debug(f'total deductions: {total_deduction}')
        logger.debug(f'total_bonus: {total_bonus}')
        logger.debug(f'net: {net}')
        logger.debug(f'net_pay: {net_pay}')
        # context = {
        #     # bonus
        #     "pointsearning": pointsearning,
        #     "EOM": EOM,
        #     "EOQ": EOQ,
        #     "EOY": EOY,
        #     "laptop_bonus": laptop_bonus,
        #     "holidaypay": holidaypay,
        #     "Night_Bonus": Night_Bonus,
        #     "yearly": yearly,
        #     # deductions
        #     "loan": loan_payment,
        #     "food_accomodation": food_accomodation,
        #     "computer_maintenance": computer_maintenance,
        #     "health": health,
        #     "laptop_saving": laptop_saving,
        #     "kra": kra,
        # 
        #     # General
        #     "total_pay": total_pay,
        #     'total_value': total_value,
        #     "total_deduction": total_deduction,
        #     'net': net,
        #     'net_pay': net_pay,
        #     "balance_amount": balance_amount,
        #     "tasks": tasks,
        #     "deadline_date": deadline_date,
        #     "today": today,
        # }
        # if request.user == employee or request.user.is_superuser:
        #     return render(request, "management/daf/payslip.html", context)
        # else:
        #     message = "Either you are not Login or You are forbidden from visiting this page-contact admin at info@codanalytics.net"
        #     return render(request, "main/errors/404.html", {"message": message})
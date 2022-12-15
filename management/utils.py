import random
from django.db.models import Sum,Max
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from decimal import Decimal
import calendar,string
from django.utils.text import slugify
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)

# from .models import Task

# ================================apis for payslip==========================
def best_employee(task_obj):
    sum_of_tasks = task_obj.annotate(sum=Sum('point'))
    # logger.debug(f'sum_of_tasks: {sum_of_tasks}')
    max_point = sum_of_tasks.aggregate(max=Max('sum')).get('max')
    # logger.debug(f'max_point: {max_point}')
    best_users = tuple(sum_of_tasks.filter(sum=max_point).values_list('employee__username'))
    # logger.debug(f'best_users: {best_users}')
    return best_users

def employee_reward(tasks):
    # sum_of_tasks = task_obj.annotate(sum=Sum('point'))
    # sum_of_tasks = task_obj.annotate(sum=Sum('mxpoint'))
    # max_point = sum_of_tasks.aggregate(max=Max('sum')).get('max')
    # point = sum_of_tasks.aggregate(max=Max('sum')).get('max')
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    mxpoints = tasks.aggregate(Your_Total_MaxPoints=Sum("mxpoint"))
    try:
        Points = points.get("Your_Total_Points")
    except (TypeError, AttributeError):
        Points = 0
    try:
        MaxPoints = mxpoints.get("Your_Total_MaxPoints")
    except (TypeError, AttributeError):
        MaxPoints = 0
    try:
        point_percentage=round((Points/MaxPoints),2)
    except (TypeError, AttributeError):
        point_percentage = 0
    return Points,MaxPoints,point_percentage

def payinitial(tasks):
    # tasks = Task.objects.all().filter(employee=employee)
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    # GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    return mxearning,points

def paymentconfigurations(PayslipConfig,employee):
    try:
        payslip_config = get_object_or_404(PayslipConfig, user=employee)
    except:
        payslip_config=PayslipConfig.objects.filter(
             Q(user__username="admin")| 
             Q(user__username="coda_info") 
             ).latest('id')
    return payslip_config

    # 1st month
    last_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month1.day)

    # 2nd month
    last_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=last_day_of_prev_month2.day)

    # 3rd month
    last_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=last_day_of_prev_month3.day)


def paytime():
    deadline_date = date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )
    # delta = deadline_date - date.today()
    payday = deadline_date + timedelta(days=15)
    delta = relativedelta(deadline_date, date.today())
    # year=delta.years
    # months=delta.months
    time_remaining_days = delta.days
    time_remaining_hours = delta.hours
    time_remaining_minutes = delta.minutes
    today = date(date.today().year, date.today().month, date.today().day)
    year = date.today().year
    month = date.today().month
    day = date.today().day
    target_date= date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )
    # 1st month
    last_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month1.day)

    # 2nd month
    last_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=last_day_of_prev_month2.day)

    # 3rd month
    last_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=last_day_of_prev_month3.day)

    return (today,year, month,day,target_date,
            time_remaining_days,time_remaining_hours,time_remaining_minutes,
            payday,deadline_date,last_day_of_prev_month1,last_day_of_prev_month2,
            start_day_of_prev_month3,last_day_of_prev_month3)

def loan_computation(total_pay,user_data,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    if user_data.exists():
        logger.info('training loan not only exists, but this user has loan !')
        training_loan = user_data.order_by('-id')[0]
        if round(Decimal(training_loan.balance_amount), 2)>0:
            loan_amount = round(Decimal(training_loan.balance_amount), 2)
            loan_payment = round(total_pay * payslip_config.loan_repayment_percentage, 2)
            if loan_amount < loan_payment:
                loan_payment = loan_amount
            new_balance=loan_amount-Decimal(loan_payment)
            balance_amount=new_balance

        else:
            loan_amount=Decimal(0)
            loan_payment = Decimal(0)
            new_balance=Decimal(0)
            balance_amount=new_balance
    else:
        if payslip_config:
            logger.info('training loan picked from configs !')
            loan_amount = Decimal(payslip_config.loan_amount)
            loan_payment = round(total_pay * payslip_config.loan_repayment_percentage, 2)
            if loan_amount < loan_payment:
                loan_payment = loan_amount
            new_balance=round(Decimal(loan_amount)-Decimal(loan_payment), 2)
            balance_amount = new_balance
        else:
            logger.info('Not not set or yet to be set !')
            loan_amount = Decimal(0)
            loan_payment = round(Decimal(total_pay) * Decimal(0.2), 2)
            balance_amount = Decimal(0)
    return loan_amount,loan_payment,balance_amount

def updateloantable(user_data,employee,total_pay,payslip_config):
    print("in update ")
    loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
    loan_data=user_data.update(
    user=employee,
    category="Debit",
    amount=loan_amount,
    # created_at,
    # updated_at=2022-10-10,
    # is_active,
    training_loan_amount=loan_amount,
    total_earnings_amount=total_pay,
    # deduction_date,
    deduction_amount=loan_payment,
    balance_amount=balance_amount,
    )
    return loan_data

def addloantable(loantable,employee,total_pay,payslip_config,user_data):
    if user_data.exists():
        previous_balance_amount = user_data.order_by('-id')[0].balance_amount
        print("previous_balance_amount", previous_balance_amount)
        loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
        # balance_amount = 999000
        if previous_balance_amount != balance_amount:
            loan_data=loantable(
            user=employee,
            category="Debit",
            amount=loan_amount,
            # created_at,
            # updated_at=2022-10-10,
            # is_active,
            training_loan_amount=loan_amount,
            total_earnings_amount=total_pay,
            # deduction_date,
            deduction_amount=loan_payment,
            balance_amount=balance_amount,
            )
            return loan_data

    else:
        loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
        loan_data = loantable(
            user=employee,
            category="Debit",
            amount=loan_amount,
            # created_at,
            # updated_at=2022-10-10,
            # is_active,
            training_loan_amount=loan_amount,
            total_earnings_amount=total_pay,
            # deduction_date,
            deduction_amount=loan_payment,
            balance_amount=balance_amount,
        )
        return loan_data

    return None

# def loan_update_save(loantable,user_data,employee,total_pay,payslip_config):
#     loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
#     # training_loan = user_data.order_by('-id')[0]
#     try:
#         training_loan = user_data.order_by('-id')[0]
#     except:
#         training_loan=None
#     if training_loan:
#         loan_data=user_data.update(
#         user=employee,
#         category="Debit",
#         amount=loan_amount,
#         # created_at,
#         # updated_at=2022-10-10,
#         # is_active,
#         training_loan_amount=loan_amount,
#         total_earnings_amount=total_pay,
#         # deduction_date,
#         deduction_amount=loan_payment,
#         balance_amount=balance_amount,
#         )
#     else:
#         loan_data=loantable(
#                 user=employee,
#                 category="Debit",
#                 amount=loan_amount,
#                 # created_at,
#                 # updated_at=today,
#                 # is_active,
#                 training_loan_amount=loan_amount,
#                 total_earnings_amount=total_pay,
#                 # deduction_date,
#                 deduction_amount=loan_payment,
#                 balance_amount=balance_amount,
#                 )
#         loan_data.save()
#     return 



def lap_save_bonus(userprofile,lbandls,LBLS):
    """Computes the laptop savings, Laptop Bonusloan payment and loan balance for an employee"""
    if userprofile.laptop_status == True:
        laptop_saving = Decimal(0)
        if LBLS.exists():
            # lbandls =LBandLS.objects.get(user_id=employee)
            laptop_bonus = lbandls.laptop_bonus
        else:
            laptop_bonus = Decimal(0)
    else:
        laptop_bonus = Decimal(0)
        if LBLS.exists():
            laptop_saving = lbandls.laptop_service
        else:
            laptop_saving = Decimal(0)
    return laptop_bonus,laptop_saving
    
def deductions(payslip_config,total_pay):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    if payslip_config:
       food_accomodation = payslip_config.food_accommodation
       computer_maintenance = payslip_config.computer_maintenance
       health = payslip_config.health
       kra = payslip_config.kra
       lap_saving=payslip_config.ls_amount
    else:
       food_accomodation = 1000
       computer_maintenance = 500
       health = 500
       kra = round(Decimal(total_pay) * Decimal(0.05), 2)
       lap_saving=500
    total_deductions=food_accomodation+computer_maintenance+health+kra+lap_saving
    return food_accomodation,computer_maintenance,health,kra,total_deductions

def bonus(tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    (today,year, month,day,target_date,
     time_remaining_days,time_remaining_hours,
     time_remaining_minutes,payday,deadline_date
     )=paytime()
    mxearning,points=payinitial(tasks)
    if payslip_config:
       # -------------points earning-----------
       bonus_points_ammount= points.get("Your_Total_Points")
       if bonus_points_ammount is None:
           bonus_points_ammount = Decimal(0)
       # -------------holiday earning-----------
       if month in (12, 1) and day in (24, 25, 26, 31, 1, 2):
           offpay = payslip_config.holiday_pay
       else:
           offpay = Decimal(0)
       # -------------late Night earning-----------
       latenight_Bonus =round(total_pay * payslip_config.rp_increment_max_percentage, 2)
       yearly = round(payslip_config.rp_starting_amount + (total_pay * payslip_config.rp_increment_percentage), 2)
    else:
       latenight_Bonus =round(total_pay * Decimal(0.05), 2)
       bonus_points_ammount= points.get("Your_Total_Points")
       if bonus_points_ammount is None:
           bonus_points_ammount = Decimal(0)
       offpay =Decimal(0)
       yearly = Decimal(12000)
    return bonus_points_ammount,latenight_Bonus,offpay,yearly

def additional_earnings(user_data,tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    # ================BONUS============================
    pointsearning,latenight_Bonus,offpay,yearly=bonus(tasks,total_pay,payslip_config)
    sub_bonus=Decimal(pointsearning)+Decimal(latenight_Bonus)+Decimal(offpay)
    # ===============DEDUCTIONS=======================
    loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
    food_accomodation,computer_maintenance,health,kra,total_deductions=deductions(payslip_config,total_pay)
    total_deduction=total_deductions+loan_payment
    return total_deduction,sub_bonus

# ================================apis for slug==========================
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def email_template(subject, to, html_content):
    msg = EmailMultiAlternatives(
        subject, '', settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



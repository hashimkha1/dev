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
        point_percentage=round((Points/MaxPoints),2)*100
    except (TypeError, AttributeError):
        point_percentage = 0

    else:
        EOM = Decimal(0.00)  # employee of month
    return point_percentage

# Usint the number of points to assign employees to different groups 

def employee_group_level(historytasks,TaskGroups):                                          
    if historytasks.exists():
        count = historytasks.aggregate(total_point=Sum('point'))
        if count.get('total_point') < 100:
            group_obj = TaskGroups.objects.filter(title='Group A')
            if group_obj.exists():
                group = group_obj.first().id
            else:
                group_obj = TaskGroups.objects.create(title='Group A')
                group = group_obj.id
        if 100 <= count.get('total_point') and count.get('total_point') < 150:
            group_obj = TaskGroups.objects.filter(title='Group B')
            if group_obj.exists():
                group = group_obj.first().id
            else:
                group_obj = TaskGroups.objects.create(title='Group B')
                group = group_obj.id
        if 150 <= count.get('total_point') and count.get('total_point') < 200:
            group_obj = TaskGroups.objects.filter(title='Group C')
            if group_obj.exists():
                group = group_obj.first().id
            else:
                group_obj = TaskGroups.objects.create(title='Group C')
                group = group_obj.id
        if 200 <= count.get('total_point') and count.get('total_point') < 250:
            group_obj = TaskGroups.objects.filter(title='Group D')
            if group_obj.exists():
                group = group_obj.first().id
            else:
                group_obj = TaskGroups.objects.create(title='Group D')
                group = group_obj.id
        if 250 <= count.get('total_point'):
            group_obj = TaskGroups.objects.filter(title='Group E')
            if group_obj.exists():
                group = group_obj.first().id
            else:
                group_obj = TaskGroups.objects.create(title='Group E')
                group = group_obj.id
    else:
        group_obj = TaskGroups.objects.filter(title='Group A')
        if group_obj.exists():
            group = group_obj.first().id
        else:
            group_obj = TaskGroups.objects.create(title='Group A')
            group = group_obj.id   
    return group
    
def payinitial(tasks):
    num_tasks = tasks.count()
    Points = tasks.aggregate(Your_Total_Points=Sum("point"))
    Maxpoints = tasks.aggregate(Your_Total_MaxPoints=Sum("mxpoint"))
    Earning = tasks.aggregate(Your_Total_Pay=Sum("mxearning"))
    Maxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    # current Pay Values
    points = Points.get("Your_Total_Points")
    mxpoints = Maxpoints.get("Your_Total_MaxPoints")
    pay = Earning.get("Your_Total_Pay")
    GoalAmount = Maxearning.get("Your_Total_AssignedAmt")
    try:
        pointsbalance = Decimal(mxpoints) - Decimal(points)
    except (TypeError, AttributeError):
        pointsbalance = 0
    return (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance)

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
    last_month=last_day_of_prev_month1.strftime("%m")
    return (today,year,deadline_date,month,last_month,day,target_date,
            time_remaining_days,time_remaining_hours,time_remaining_minutes,
            payday,last_day_of_prev_month1,last_day_of_prev_month2,
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
    
def deductions(user_data,payslip_config,total_pay):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    if payslip_config:
       food_accomodation = payslip_config.food_accommodation
       computer_maintenance = payslip_config.computer_maintenance
       health = payslip_config.health
       kra = payslip_config.kra
       lap_saving=payslip_config.ls_amount
       loan_payment=loan_computation(total_pay,user_data,payslip_config)[1]
    else:
       food_accomodation = 1000
       computer_maintenance = 500
       health = 500
       kra = round(Decimal(total_pay) * Decimal(0.05), 2)
       lap_saving=500
       loan_payment=0
    total_deductions=food_accomodation+computer_maintenance+health+kra+lap_saving
    return food_accomodation,computer_maintenance,health,kra,lap_saving,loan_payment,total_deductions

def bonus(tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    month=paytime()[3]
    day=paytime()[5]
    print(month)
    print(day)
    (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance)=payinitial(tasks)
    if payslip_config:
        # -------------points earning-----------
        bonus_points_ammount= points
        if bonus_points_ammount is None:
                bonus_points_ammount = Decimal(0)
                # EOM =payslip_config.eom_bonus   # employee of month
        # -------------Laptop Bonus-----------
        Lap_Bonus = payslip_config.lb_amount
        # -------------holiday earning-----------
        offpay = payslip_config.holiday_pay if month in (12, 1) and day in (24, 25, 26, 31, 1, 2) else Decimal(0.00)
        # -------------late Night earning-----------
        latenight_Bonus =round(total_pay * payslip_config.rp_increment_max_percentage, 2)
        yearly = round(payslip_config.rp_starting_amount + (total_pay * payslip_config.rp_increment_percentage), 2)
        # -------------Employee of Award(EOM,EOQ,EOY)-----------
        point_percentage=employee_reward(tasks)
        EOM = payslip_config.eom_bonus if point_percentage>=0.75 else Decimal(0.00)
        EOQ =  Decimal(0.00)
        EOY =  Decimal(0.00)
    else:
        EOM = Decimal(0.00)  # employee of month
        EOQ =  Decimal(0.00)
        EOY =  Decimal(0.00)
        latenight_Bonus =round(total_pay * Decimal(0.05), 2)
        bonus_points_ammount= Decimal(0.00)
        yearly = Decimal(12000)
        Lap_Bonus =  Decimal(0.00)
    return bonus_points_ammount,latenight_Bonus,yearly,offpay,EOM,EOQ,EOY,Lap_Bonus

def additional_earnings(user_data,tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    # ================BONUS============================
    bonus_points_ammount,latenight_Bonus,yearly,offpay,EOM,EOQ,EOY,Lap_Bonus=bonus(tasks,total_pay,payslip_config)
    sub_bonus=(Decimal(bonus_points_ammount)+Decimal(latenight_Bonus)+
              +Decimal(EOM)+Decimal(EOQ)+Decimal(EOY)+
              Decimal(Lap_Bonus))
    # ===============DEDUCTIONS=======================
    # loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
    # *_,total_deductions=deductions(payslip_config,total_pay)
    total_deduction=deductions(user_data,payslip_config,total_pay)[-1]
    print(f'LOAN AMOUNT={total_deduction}')
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

def split_num_str(my_str):
    num = [x for x in my_str if x.isdigit()]
    num = "".join(num)
    if not num:
        num = None
    return num

def text_num_split(item):
    for index, letter in enumerate(item, 0):
        if letter.isdigit():
            return [item[:index],item[index:]]

def task_assignment_random(employees):
    # departments=[department.name for department in dept_obj ]
    departments=['HR','IT','Finance','Health','Marketing','Basics','Projects']
    departments_per_worker = len(departments) / len(employees)
    random.shuffle(departments)
    rand_departments = zip(*[iter(departments)] * int(departments_per_worker))
    return employees,rand_departments
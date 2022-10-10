import random
from django.db.models import Sum,Max
from decimal import Decimal
import calendar,string
from django.utils.text import slugify
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, redirect, render
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

def payinitial(tasks):
    # tasks = Task.objects.all().filter(employee=employee)
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    # GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    return mxearning,points

def paymentconfigurations(PayslipConfig,employee):
    payslip_config = get_object_or_404(PayslipConfig, user=employee)
    return payslip_config

def paytime():
    today = date(date.today().year, date.today().month, date.today().day)
    year = date.today().year
    month = date.today().month
    day = date.today().day
    target_date= date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )
    return today,year,month,day,target_date

def loan_deductions(total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    if payslip_config:
        loan_amount = Decimal(payslip_config.loan_amount)
        loan_payment = round(total_pay * payslip_config.loan_repayment_percentage, 2)
        balance_amount = round(Decimal(loan_amount - loan_payment), 2)
    else:
        loan_amount = Decimal(0)
        loan_payment = Decimal(0)
        balance_amount = Decimal(0)
    return loan_amount,loan_payment,balance_amount

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
    
def deductions(payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    if payslip_config:
       food_accomodation = payslip_config.food_accommodation
       computer_maintenance = payslip_config.computer_maintenance
       health = payslip_config.health
       kra = payslip_config.kra
    else:
       food_accomodation = 1000
       computer_maintenance = 500
       health = 500
       kra = 0
    return food_accomodation,computer_maintenance,health,kra

def bonus(tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    today,year,month,day,target_date= paytime()
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
       latenight_Bonus = total_pay * 0.05
       bonus_points_ammount= points.get("Your_Total_Points")
       offpay = 0
       yearly = 12000
    return bonus_points_ammount,latenight_Bonus,offpay,yearly

def additional_earnings(tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    # ================BONUS============================
    pointsearning,latenight_Bonus,offpay,yearly=bonus(tasks,total_pay,payslip_config)
    sub_bonus=pointsearning+latenight_Bonus+offpay
    # ===============DEDUCTIONS=======================
    loan_amount,loan_payment,balance_amount=loan_deductions(total_pay,payslip_config)
    food_accomodation,computer_maintenance,health,kra=deductions(payslip_config)
    total_deductions=food_accomodation+computer_maintenance+health+kra+loan_payment
    return total_deductions,sub_bonus



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





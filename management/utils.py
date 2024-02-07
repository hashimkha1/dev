import random
from django.db.models import Sum,Max
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from decimal import Decimal
import calendar,string
from django.urls import reverse
from django.utils.text import slugify
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)

# from .models import Task

# ================================client assessment==========================
def compute_total_points(instance):
    delta=1
    totalpoints = 0
    try:
        pc=instance.projectcharter-delta
    except:
        pass
    try:
        ra=instance.requirementsAnalysis-delta
    except:
        pass
    try:
        rpt=instance.reporting-delta
    except:
        pass
    try:
        etl=instance.etl-delta
    except:
        pass
    try:
        db=instance.database-delta
    except:
        pass
    try:
        test=instance.testing-delta
    except:
        pass
    try:
        dep=instance.deployment-delta
    except:
        pass
    try:
        frontend=instance.frontend-delta
    except:
        pass
    try:
        backend=instance.backend-delta
    except:
        pass
    
    ############################
    # developer points
    ############################
    #calculation
    #1 days effective hour of work is 6(avg)
    #here 1 sprint = 10 days
    #1 month = 2 sprint
    #we minus 1 year of experiance and only half of it will be counted because half of the year counted as learning
    try:
        developer_point = 0
      
        if instance.it_exp > 0:
            one_year_point = 1440 #24*10*6
            
            it_expiriance = instance.it_exp-1
            developer_point = it_expiriance*one_year_point + (one_year_point/2)

    except:
        pass


    # totalpoints=pc+ra+rpt+etl+db+test+dep+nie+ie+frontend+backend
    totalpoints=pc+ra+rpt+etl+db+test+dep+frontend+backend
    return totalpoints, developer_point


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
        total_point = count.get('total_point')

        if historytasks[0].group == 'Group I':
            
            group_obj = TaskGroups.objects.filter(title='Group I')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title
            else:
                group_obj = TaskGroups.objects.create(title='Group I')
                group = group_obj.id
                group_name = group_obj.title

        elif historytasks[0].group == 'Group H':
            
            group_obj = TaskGroups.objects.filter(title='Group H')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title
            else:
                group_obj = TaskGroups.objects.create(title='Group H')
                group = group_obj.id
                group_name = group_obj.title

        elif count.get('total_point') < 350:
            group_obj = TaskGroups.objects.filter(title='Group A')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title

            else:
                group_obj = TaskGroups.objects.create(title='Group A')
                group = group_obj.id
                group_name = group_obj.title

        elif 350 <= count.get('total_point') and count.get('total_point') < 600:
            group_obj = TaskGroups.objects.filter(title='Group B')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title

            else:
                group_obj = TaskGroups.objects.create(title='Group B')
                group = group_obj.id
                group_name = group_obj.title

        elif 600 <= count.get('total_point') and count.get('total_point') < 800:
            group_obj = TaskGroups.objects.filter(title='Group C')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title

            else:
                group_obj = TaskGroups.objects.create(title='Group C')
                group = group_obj.id
                group_name = group_obj.title

        elif 800 <= count.get('total_point') and count.get('total_point') < 1000:
            group_obj = TaskGroups.objects.filter(title='Group D')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title

            else:
                group_obj = TaskGroups.objects.create(title='Group D')
                group = group_obj.id
                group_name = group_obj.title

        elif 1000 <= count.get('total_point'):
            group_obj = TaskGroups.objects.filter(title='Group E')
            if group_obj.exists():
                group = group_obj.first().id
                group_name = group_obj.first().title

            else:
                group_obj = TaskGroups.objects.create(title='Group E')
                group = group_obj.id
                group_name = group_obj.title

    else:
        total_point = 0
        group_obj = TaskGroups.objects.filter(title='Group A')
        if group_obj.exists():
            group = group_obj.first().id
            group_name = group_obj.first().title

        else:
            group_obj = TaskGroups.objects.create(title='Group A')
            group = group_obj.id   
            group_name = group_obj.title

    
    return group, group_name, total_point

def increment_in_graduation_of_employee(employee, max_earning, new_group, PayslipConfig):
        
    payslipconfig_obj = PayslipConfig.objects.filter(user=employee)

    if payslipconfig_obj.exists():
        
        increment_percentage = payslipconfig_obj.first().web_delta
    
    else:
        payslipconfig_admin_obj = PayslipConfig.objects.filter(user__username='coda_info')
        
        if payslipconfig_admin_obj.exists():
        
            increment_percentage = payslipconfig_admin_obj.first().web_delta
        
        else:

            increment_percentage = 1

    
    return max_earning + (max_earning*increment_percentage/100)
    
    


def payinitial(tasks):
    num_tasks = tasks.count()
    Points = tasks.aggregate(Your_Total_Points=Sum("point"))
    Maxpoints = tasks.aggregate(Your_Total_MaxPoints=Sum("mxpoint"))
    Earning = tasks.aggregate(Your_Total_Pay=Sum("mxearning"))
    Maxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    point_percentage = employee_reward(tasks)
    try:
    # current Pay Values
        points = round(Points.get("Your_Total_Points"))
        mxpoints = round(Maxpoints.get("Your_Total_MaxPoints"))
        pay = Earning.get("Your_Total_Pay")
        GoalAmount = Maxearning.get("Your_Total_AssignedAmt")
        pointsbalance = Decimal(mxpoints) - Decimal(points)
    except (TypeError, AttributeError):
        points=0.00
        mxpoints=0.00
        pay=0.00
        GoalAmount=0.00
        pointsbalance=0.00
        pointsbalance=0.00
    return (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance,point_percentage)

def paymentconfigurations(PayslipConfig, employee):
    try:
        payslip_config = PayslipConfig.objects.get(user=employee)
    except:
        # If the employee does not have a PayslipConfig object, then use a default PayslipConfig object.
        payslip_config = PayslipConfig.objects.latest('id')

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
            payday,start_day_of_prev_month2,last_day_of_prev_month1,last_day_of_prev_month2,
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
    # print("in update ")
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
        # print("previous_balance_amount", previous_balance_amount)
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

def lap_save_bonus(userprofile,payslip_config):
    """Computes the laptop savings, Laptop Bonusloan payment and loan balance for an employee"""
    # payslip_config=paymentconfigurations(PayslipConfig,employee)
    if userprofile.laptop_status == True:
        laptop_saving =Decimal(0.00)
        laptop_bonus=payslip_config.lb_amount
    else:
        laptop_bonus=Decimal(0.00)
        laptop_saving =Decimal(payslip_config.ls_amount)

    return laptop_bonus,laptop_saving



def deductions(employee, user_data, payslip_config, total_pay):
    """
    Computes the deductions for an employee, including food, accommodation, maintenance, health, KRA, lap saving, and loan payment.
    """
    # Default deduction values as Decimal
    food_accommodation = Decimal('1000')
    computer_maintenance = Decimal('500')
    health = Decimal('500')
    kra_percentage = Decimal('0.05')
    lap_saving = Decimal('500')
    loan_payment = Decimal('0')

    if employee.category == 2 and employee.sub_category == 5:
        # print(employee.category, employee.sub_category)
        food_accommodation = Decimal('0.00')
        computer_maintenance = Decimal('0.00')
        health = Decimal('500.00')
        kra = round(Decimal(total_pay) * kra_percentage, 2)
        lap_saving = Decimal('0.00')
    else:
        if payslip_config:
            # print(employee.category, employee.sub_category)
            food_accommodation = Decimal(payslip_config.food_accommodation)
            computer_maintenance = Decimal(payslip_config.computer_maintenance)
            health = Decimal(payslip_config.health)
            kra_percentage = Decimal(0.05)
            lap_saving = Decimal(payslip_config.ls_amount)
            loan_payment = Decimal(loan_computation(total_pay, user_data, payslip_config)[1])

    kra = round(Decimal(total_pay) * kra_percentage, 2)
    total_deductions = (
        food_accommodation
        + computer_maintenance
        + health
        + kra
        + lap_saving
        + loan_payment
    )

    return (
        food_accommodation,
        computer_maintenance,
        health,
        kra,
        lap_saving,
        loan_payment,
        total_deductions,
    )

def bonus(tasks,total_pay,payslip_config):
    """Computes the loan amount, loan payment and loan balance for an employee"""
    # laptop_bonus,laptop_saving=lap_save_bonus(userprofile,payslip_config,employee)
    month=paytime()[3]
    day=paytime()[5]
    (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance,point_percentage)=payinitial(tasks)
    if payslip_config:
        # -------------points earning-----------
        bonus_points_ammount= points
        if bonus_points_ammount is None:
                bonus_points_ammount = Decimal(0)
                # EOM =payslip_config.eom_bonus   # employee of month
        # -------------Laptop Bonus-----------
        # Lap_Bonus = laptop_bonus #payslip_config.lb_amount
        # -------------holiday earning-----------
        offpay = payslip_config.holiday_pay if month in (12, 1) and day in (24, 25, 26, 31, 1, 2) else Decimal(0.00)
        # -------------late Night earning-----------
        latenight_Bonus =round(total_pay * payslip_config.rp_increment_max_percentage, 2)
        # print("latenight_Bonus====>",latenight_Bonus)
        yearly = round(payslip_config.rp_starting_amount + (total_pay * payslip_config.rp_increment_percentage), 2)
        # -------------Employee of Award(EOM,EOQ,EOY)-----------
        point_percentage=employee_reward(tasks)
        EOM = payslip_config.eom_bonus if point_percentage>=75 else Decimal(0.00)
        EOQ =  Decimal(0.00)
        EOY =  Decimal(0.00)
    else:
        EOM = Decimal(0.00)  # employee of month
        EOQ =  Decimal(0.00)
        EOY =  Decimal(0.00)
        latenight_Bonus =round(total_pay * Decimal(0.05), 2)
        bonus_points_ammount= Decimal(0.00)
        yearly = Decimal(12000)
        offpay = Decimal(0.00)
        # Lap_Bonus =  Decimal(0.00)

    sub_bonus=(Decimal(bonus_points_ammount)+Decimal(latenight_Bonus)+
              +Decimal(EOM)+Decimal(EOQ)+Decimal(EOY)
              +Decimal(offpay))
    return bonus_points_ammount,latenight_Bonus,yearly,offpay,EOM,EOQ,EOY,sub_bonus#,Lap_Bonus

# def additional_earnings(employee,user_data,tasks,total_pay,payslip_config):
#     """Computes the loan amount, loan payment and loan balance for an employee"""
#     # ================BONUS============================
#     *_,sub_bonus=bonus(tasks,total_pay,payslip_config)
#     # ===============DEDUCTIONS=======================
#     total_deduction=deductions(employee,user_data,payslip_config,total_pay)[-1]
#     return total_deduction,sub_bonus


def calculate_total_pay(tasks):
    """Calculate total pay from tasks."""
    total_pay = 0
    for task in tasks:
        total_pay += task.get_pay
    return total_pay

def get_points_and_earnings(tasks):
    """Calculate points and earnings from tasks."""
    num_tasks = tasks.count()
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    mxpoints = tasks.aggregate(Your_Total_MaxPoints=Sum("mxpoint"))
    earning = tasks.aggregate(Your_Total_Pay=Sum("mxearning"))
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    pointsbalance = Decimal(mxpoints) - Decimal(points)
    point_percentage = employee_reward(tasks)
    pay = earning.get("Your_Total_Pay")
    GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    return num_tasks,points,mxpoints,pointsbalance, point_percentage, pay, GoalAmount

def get_bonus_and_summary(employee,tasks,total_pay,user_data,payslip_config):
    """Calculate bonus and summary values."""
    bonus_points_ammount, latenight_Bonus, yearly, offpay, EOM, EOQ, EOY, sub_bonus = bonus(tasks, total_pay, payslip_config)
    *_,sub_bonus=bonus(tasks,total_pay,payslip_config)
    # ===============DEDUCTIONS=======================
    total_deduction=deductions(employee,user_data,payslip_config,total_pay)[-1]
    total_bonus = sub_bonus #+ laptop_bonus
    return bonus_points_ammount, latenight_Bonus, yearly, offpay, EOM, EOQ, EOY, sub_bonus, total_deduction, total_bonus

def emp_average_earnings(request,TaskHistory,GoalAmount,employee):
    start_day_of_prev_month2=paytime()[-5]
    last_day_of_prev_month1=paytime()[-4]
    last_day_of_prev_month2=paytime()[-3]
    start_day_of_prev_month3=paytime()[-2]
    # print("last_day_of_prev_month1======>",last_day_of_prev_month1)
    # print("last_day_of_prev_month2======>",last_day_of_prev_month2)
    # print("start_day_of_prev_month3======>",start_day_of_prev_month3)
    last_day_of_prev_month1=paytime()[-3]
    start_day_of_prev_month3=paytime()[-2]
        # print("average_earnings======>",average_earnings)
    history = TaskHistory.objects.filter(
        Q(submission__lte=last_day_of_prev_month1),
        Q(submission__gte=start_day_of_prev_month3),
        Q(employee=employee)
        # Q(employee__username=request.user)
    )
    last3month_history = TaskHistory.objects.filter(
        Q(submission__lte=last_day_of_prev_month1),
        Q(submission__gte=start_day_of_prev_month3),
        Q(employee=employee)
        # Q(employee__username=request.user)
    )
    last2monthhistory = TaskHistory.objects.filter(
        Q(submission__lte=last_day_of_prev_month1),
        Q(submission__gte=start_day_of_prev_month2),
        Q(employee=employee)
        # Q(employee__username=request.user)
    )
    lastmonthhistory = TaskHistory.objects.filter(
        Q(submission__gte=last_day_of_prev_month1),
        Q(employee=employee)
        # Q(employee__username=request.user)
    )

    average_earnings = 0
    counter = 3
    for data in history.all():
        average_earnings += data.get_pay
        # counter = counter+1 
        counter = 3
    average_earnings = round((average_earnings / counter),2)
    if average_earnings == 0:
        average_earnings = GoalAmount
    return average_earnings

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
    departments=['HR','IT','Finance','Health','Marketing','Basics','IT Projects','Field Projects','Security']
    try:
        departments_per_worker = len(departments) / len(employees)
    except ZeroDivisionError:
        departments_per_worker = len(departments) / 1
    random.shuffle(departments)
    rand_departments = zip(*[iter(departments)] * int(departments_per_worker))
    return employees,rand_departments

def defined_links(request):
    links = {
        'My Meetings': reverse('management:meetings', kwargs={'status': 'company'}),
        'My Schedule': reverse('main:my_availability'),
        'My Sessions': reverse('management:user_session', args=[request.user]),
        'Edit Profile': reverse('main:update_profile', args=[request.user.profile.id]),
    }

    # Conditional links based on user category
    if request.user.category == 1 or request.user.is_applicant:
        links.update({
            'My Application':reverse('application:policies'),
            'My Interview':reverse('application:interview'),
            'Apply for Internship':reverse('main:contact'),
            'Apply for Training':reverse('main:contact'),
             'Company Policies': reverse('application:policies'),
        })
    elif request.user.is_staff:
        links.update({
            'My DAF': reverse('management:user_task', args=[request.user]),
            'Last DAF': reverse('management:user_task_history', args=[request.user]),
            'My Evidence': reverse('management:user_evidence', args=[request.user]),
            'My Sessions': reverse('management:user_session', args=[request.user]),
            'Evidence': reverse('management:evidence'),
        })
    elif request.user.is_client:
        links.update({
            'Assessment': reverse('management:clientassessment'),
            'My Training': reverse('data:train'),
            'My Interview': reverse('data:question-detail', kwargs={'question_type': 'resume'}),
            'Job Support': reverse('data:start_training', kwargs={'slug': 'interview'}),
            'My Time': reverse('accounts:user-list', args=[request.user]),
            'My Contract': reverse('finance:mycontract', args=[request.user]),
            'New Contract': reverse('main:display_service', kwargs={'slug': 'data_analysis'}),
            'Make Payment': reverse('finance:pay'),
            
        })

    if request.user.is_superuser:
        links.update({
            'Tasks':reverse('management:tasks'),
            'History Tasks':reverse('management:taskhistory'),
            'Evidence': reverse('management:evidence'),
        })
    return links
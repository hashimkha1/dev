import datetime
import dateutil.relativedelta
from django.db.models import Sum, Max
from .models import TrainingLoan
from management.models import TaskHistory


def calculate_loan(user):
    debit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.DEBIT
    ).aggregate(Sum('value'))
    if debit['value__sum'] == None:
        debit['value__sum'] = 0
    credit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.CREDIT
    ).aggregate(Sum('value'))
    if credit['value__sum'] == None:
        credit['value__sum'] = 0
    loan = debit['value__sum'] - credit['value__sum']
    return loan

def balance_loan(user):
    debit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.DEBIT
    ).aggregate(Sum('value'))
    if debit['value__sum'] == None:
        debit['value__sum'] = 0
    credit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.CREDIT
    ).aggregate(Sum('value'))
    if credit['value__sum'] == None:
        credit['value__sum'] = 0
    balloan = debit['value__sum'] - credit['value__sum']
    return balloan


def EOM():
    today = datetime.date.today()
    lastMonth = today + dateutil.relativedelta.relativedelta(months=-1)
    task_max_point = TaskHistory.objects.filter(
        date__contains=lastMonth.strftime('%Y-%m')
    ).aggregate(Max('point'))['point__max']
    if(task_max_point > 0):
        return TaskHistory.objects.filter(point=task_max_point)
    return False

def EOQ():
    today = datetime.date.today()
    lastMonth = today + dateutil.relativedelta.relativedelta(months=-3)
    task_max_point = TaskHistory.objects.filter(
        date__gte=lastMonth
    ).aggregate(Max('point'))['point__max']
    if(task_max_point > 0):
        return TaskHistory.objects.filter(point=task_max_point)
    return False

def EOY():
    today = datetime.date.today()
    lastYear = today + dateutil.relativedelta.relativedelta(years=-1)
    task_max_point = TaskHistory.objects.filter(
        date__gte=lastYear
    ).aggregate(Max('point'))['point__max']
    if(task_max_point > 0):
        return TaskHistory.objects.filter(point=task_max_point)
    return False

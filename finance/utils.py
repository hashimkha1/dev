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


def sum_of_points(user_id):
    today = datetime.date.today()
    lastMonth = today + dateutil.relativedelta.relativedelta(months=-1)
    lastMonth_month = lastMonth.strftime('%m')

    # if the month is december, calculate and store the sum of points for a year
    # else for a month.
    if lastMonth_month == 12:
        lastMonth_year = lastMonth.strftime('%Y')
        last_year_points = TaskHistory.objects.filter(
            employee=user_id,
            date__contains=lastMonth_year
        ).aggregate(Sum('point'))
        UserYearlyPoints.objects.create(
            user_id=user_id,
            year=lastMonth_year,
            points=last_year_points
        )

    else:
        lastMonth_month_and_year = lastMonth.strftime('%Y-%m')
        last_month_points = TaskHistory.objects.filter(
            employee=user,
            date__contains=lastMonth_month_and_year
        ).aggregate(Sum('point'))
        UserMonthlyPoints.objects.create(
            user_id=user_id,
            month=lastMonth_month_and_year,
            points=last_month_points
        )

#
# def EOQ():
#     today = datetime.date.today()
#     lastMonth = today + dateutil.relativedelta.relativedelta(months=-3)
#     task_max_point = TaskHistory.objects.filter(
#         date__gte=lastMonth
#     ).aggregate(Max('point'))['point__max']
#     if(task_max_point > 0):
#         return TaskHistory.objects.filter(point=task_max_point)
#     return False
#
# def EOY():
#     today = datetime.date.today()
#     lastYear = today + dateutil.relativedelta.relativedelta(years=-1)
#     task_max_point = TaskHistory.objects.filter(
#         date__gte=lastYear
#     ).aggregate(Max('point'))['point__max']
#     if(task_max_point > 0):
#         return TaskHistory.objects.filter(point=task_max_point)
#     return False

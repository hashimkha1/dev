import calendar,string
from logging import exception

import requests
from django import template
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from mail.custom_email import send_email
from application.models import UserProfile
from management.utils import email_template
from management.forms import (
    DepartmentForm,
    PolicyForm,
    ManagementForm,
    RequirementForm,
    EvidenceForm,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from management.models import (
    Advertisement,
    Policy,
    Tag,
    Estimate,
    Task,
    TaskHistory,
    TaskLinks,
    Requirement,
    LBandLS,
    Training
)
from data.models import DSU
from finance.models import Default_Payment_Fees, LoanUsers, TrainingLoan

from django.conf import settings
from django.contrib.auth import get_user_model

from coda_project import settings
from datetime import date, timedelta
from django.db.models import Q
from django.db.models import Max

from accounts.models import Tracker, Department, TaskGroups
from finance.models import  PayslipConfig
from management.utils import (
                               paytime,payinitial,paymentconfigurations,
                               deductions,loan_computation,
                               bonus,additional_earnings,best_employee,updateloantable,
                               addloantable
                        )

from django.contrib import messages
    

import logging
logger = logging.getLogger(__name__)

# User=settings.AUTH_USER_MODEL
User = get_user_model()
register = template.Library()


def home(request):
    return render(
        request, "main/home_templates/management_home.html", {"title": "home"}
    )


# ================================DEPARTMENT SECTION================================
def department(request):
    departments = Department.objects.filter(is_active=True)
    return render(request, "management/departments/departments.html", {'departments': departments})


def newdepartment(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:departments')
    else:
        form = DepartmentForm()
    return render(request, "management/tag_form.html", {"form": form})


class DepartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    success_url = "/management/departments"
    fields = ["name", "slug", "description", "is_active", "is_featured"]
    form = DepartmentForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return True
        return False


def contract(request):
    return render(request, "management/doc_templates/trainingcontract_form.html")
    # if request.user == employee:
    #     # return render(request, 'management/daf/paystub.html', context)
    #     return render(request, "management/doc_templates/studentcontract_form.html")
    # elif request.user.is_superuser:
    #     # return render(request, 'management/daf/paystub.html', context)
    #     return render(request, "management/doc_templates/supportcontract_form.html")


# ==============================PLACE HOLDER MODELS=======================================

# Summary information for tasks


tasksummary = [
    {
        "Target": "1",
        "Description": "Total Amount Assigned",
    },
    {
        "Target": "2",
        "Description": " progress	",
    },
    {
        "Target": "3",
        "Description": "Keep making progress	",
    },
]

# ----------------------REPORTS--------------------------------

import json


def companyagenda(request):
    # f = open(settings.SITE_URL+settings.STATIC_URL+'companyagenda.json')
    # data = json.load(f)
    # f.close()
    request.session["siteurl"] = settings.SITEURL
    with open(settings.STATIC_ROOT + '/companyagenda.json', 'r') as file:
        data = json.load(file)

    return render(request, "management/companyagenda.html", {"title": "Company Agenda", "data": data})


def updatelinks_companyagenda(request):
    department = request.POST["department"]
    subdepartment = request.POST["subdepartment"]
    linkname = request.POST["linkname"]
    link_url = request.POST["link_url"]

    with open(settings.STATIC_ROOT + '/companyagenda.json', "r") as jsonFile:
        data = json.load(jsonFile)

    if subdepartment == "":
        data[department][linkname] = link_url
    else:
        data[department][subdepartment][linkname] = link_url

    with open(settings.STATIC_ROOT + '/companyagenda.json', "w") as jsonFile:
        json.dump(data, jsonFile)

    return JsonResponse({"success": True})


def finance(request):
    return render(
        request, "finance\reports\finance.html", {"title": "Finance"}

    )


def hr(request):
    return render(request, "management/companyagenda.html", {"title": "HR"})


# ----------------------MANAGEMENT POLICIES& OTHER VIEWS--------------------------------
def policy(request):
    if request.method == "POST":
        form = PolicyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management:policies")
    else:
        form = PolicyForm()
    return render(request, "management/departments/hr/policy.html", {"form": form})


def policies(request):
    day_name = date.today().strftime("%A")
    policies = Policy.objects.filter(is_active=True, day=day_name).order_by("upload_date")
    applicant_policies = Policy.objects.filter(Q(is_active=True), Q(is_internal=False)).order_by("upload_date")
    reporting_date = date.today() + timedelta(days=7)
    context = {
        "policies": policies,
        "applicant_policies": applicant_policies,
        "reporting_date": reporting_date,
        "day_name": day_name,
    }
    # if request.user.is_applicant or request.user.is_admin or request.user.is_superuser:
    #     return render(request, "application/orientation/policies.html", context)
    # else:
    return render(request, "management/departments/hr/policies.html", context)


class PolicyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Policy
    # success_url="/management/transaction"
    fields = ["staff", "type", "department", "day", "description", "link", "is_active", "is_featured", "is_internal"]
    form = PolicyForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("management:policies")

    def test_func(self):
        policy = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == policy.staff:
            return True
        return False


def benefits(request):
    reporting_date = date.today()
    day_name = date.today().strftime("%A")
    uploads = Policy.objects.all().order_by("upload_date")
    context = {
        "uploads": uploads,
        "reporting_date": reporting_date,
        "day_name": day_name,
    }
    return render(request, "management/hr/benefits.html", context)


# ===================================ACTIVITY CLASS-BASED VIEWS=========================================

# ======================TAG=======================
class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    success_url = "/management/newtask"
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskGroupCreateView(LoginRequiredMixin, CreateView):
    model = TaskGroups
    # success_url = "/management/newtask"
    success_url = "/management/tasks/"
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ======================TASKS=======================
def task(request, slug=None, *args, **kwargs):
    # qs=Info.objects.filter(id=pk)
    # if qs.exists and qs.count()==1:
    #     instance=qs.first()
    # else:
    #     raise Http404("User does not exist")
    instance = Task.objects.get_by_slug(slug)
    if instance is None:
        raise Http404("Task does not exist")

    context = {"object": instance}
    return render(request, "management/daf/task.html", context)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    success_url = "/management/tasks"
    fields = [
        "groupname",
        "category",
        "employee",
        "activity_name",
        "description",
        "point",
        "mxpoint",
        "mxearning",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def newtaskcreation(request):
    if request.method == "POST":
        group = request.POST["group"]
        category = request.POST["category"]
        description = request.POST["description"]
        point = request.POST["point"]
        mxpoint = request.POST["mxpoint"]
        mxearning = request.POST["mxearning"]

        employee = request.POST["employee"].split(",")
        activitys = request.POST["activitys"].split(",")

        for emp in employee:
            for act in activitys:
                if Task.objects.filter(category_id=category, activity_name=act).count() > 0:
                    des, po, maxpo, maxear = \
                    Task.objects.values_list("description", "point", "mxpoint", "mxearning").filter(
                        category_id=category, activity_name=act)[0]

                    if Task.objects.filter(groupname_id=group, category_id=category, activity_name=act).count() == 0:
                        Task.objects.create(groupname_id=group, category_id=category, employee_id=emp,
                                            activity_name=act, description=des, point=0.00, mxpoint=mxpoint,
                                            mxearning=mxearning)
                    else:
                        Task.objects.create(groupname_id=group, category_id=category, employee_id=emp,
                                            activity_name=act, description=des, point=0.00, mxpoint=maxpo,
                                            mxearning=maxear)

                else:
                    Task.objects.create(groupname_id=group, category_id=category, employee_id=emp, activity_name=act,
                                        description=description, point=point, mxpoint=mxpoint, mxearning=mxearning)

        # return redirect("management:tasks")
        return JsonResponse({"success": True})

    else:
        tag = Tag.objects.all()
        group = TaskGroups.objects.all()
        employess = User.objects.filter(Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True)).all()

    return render(request, "management/tasknew_form.html", {"group": group, "category": tag, "employess": employess})


def gettasksuggestions(request):
    category = request.POST["category"]
    tasks = list(Task.objects.values_list("activity_name", flat=True).filter(category__id=category))
    return JsonResponse({"tasklist": tasks})


def verifytaskgroupexists(request):
    group = request.POST["group"]
    category = request.POST["category"]
    activity = request.POST["activity"]
    count = Task.objects.filter(groupname__id=group, category__id=category, activity_name=activity).count()
    mxpoint = Task.objects.values_list("mxpoint", flat=True).filter(category__id=category, activity_name=activity)[0]

    return JsonResponse({"count": count, "mxpoint": mxpoint})


def getaveragetargets(request):
    print("+++++++++getaveragetargets+++++++++")
    taskname = request.POST["taskname"]
    # 1st month
    last_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month1.day)

    last_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=last_day_of_prev_month2.day)

    # 3rd month
    last_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=last_day_of_prev_month3.day)

    history = TaskHistory.objects.filter(Q(activity_name=taskname), Q(created_at__gte=start_day_of_prev_month3),
                                         Q(created_at__lte=last_day_of_prev_month1))

    results = {"target_points": 0, "target_amount": 0}
    counter = 0
    for data in history.all():
        results["target_points"] += data.mxpoint
        results["target_amount"] += data.mxearning
        counter = counter + 1
    try:
        results["target_points"] = results["target_points"] / counter
        results["target_amount"] = results["target_amount"] / counter
    except Exception as ZeroDivisionError:
        results["target_points"] = 0.0
        results["target_amount"] = 0.0

    return JsonResponse(results)


class TaskListView(ListView):
    queryset = Task.objects.all()
    template_name = "management/daf/tasklist.html"


def FilterUsersByLoan(request):
    user_loan_filter = request.POST["user_loan_filter"]
    reslist = []

    if user_loan_filter == "all_user":
        tasklist = Task.objects.all()
        res = filterdatset(tasklist)
        reslist = res.copy()
    else:
        loanusers = LoanUsers.objects.filter(is_loan=user_loan_filter).values_list("user", flat=True)
        loanusers = list(loanusers)
        tasklist = Task.objects.filter(employee__in=loanusers)
        res = filterdatset(tasklist)
        reslist = res.copy()
    return JsonResponse(reslist, safe=False)


def filterdatset(obj):
    result = []
    details = {}
    for data in obj:
        details["groupname"] = str(data.groupname)
        details["deadline"] = data.deadline.strftime("%d %b %Y")
        details["submission"] = data.submission.strftime("%d %b %Y")
        details["point"] = data.point
        details["mxpoint"] = data.mxpoint
        details["mxearning"] = float(data.mxearning)
        details["get_pay"] = float(data.get_pay)
        details["id"] = data.id
        details["employee"] = data.employee.username
        details["first_name"] = data.employee.first_name
        details["last_name"] = data.employee.last_name
        details["description"] = data.description
        details["activity_name"] = data.activity_name
        details["get_absolute_url"] = str(data.category.get_absolute_url)
        result.append(details.copy())
    return result


def filterbycategory(request):
    category = request.POST["category"]

    tasks = Task.objects.filter(category__title=category)
    result = []
    details = {}
    for data in tasks.all():
        details["groupname"] = data.groupname
        details["deadline"] = data.deadline.strftime("%d %b %Y")
        details["submission"] = data.submission.strftime("%d %b %Y")
        details["point"] = data.point
        details["mxpoint"] = data.mxpoint
        details["mxearning"] = float(data.mxearning)
        details["get_pay"] = float(data.get_pay)
        details["id"] = data.id
        details["employee"] = data.employee.username
        details["first_name"] = data.employee.first_name
        details["last_name"] = data.employee.last_name
        details["description"] = data.description
        details["activity_name"] = data.activity_name
        details["get_absolute_url"] = str(data.category.get_absolute_url)
        result.append(details.copy())

    print(result)
    return JsonResponse({"result": result}, safe=False)


class TaskHistoryView(ListView):
    queryset = TaskHistory.objects.all()
    template_name = "management/daf/taskhistory.html"


def task_payslip(request, *args, **kwargs):
    task_history = TaskHistory.objects.get(pk=kwargs.get("pk"))
    today = date(date.today().year, date.today().month, date.today().day)
    year = task_history.submission.strftime("%Y")
    month = task_history.submission.strftime("%b")
    day = task_history.submission.strftime("%d")
    last_date = calendar.monthrange(
        int(year), int(task_history.submission.strftime("%m"))
    )[1]
    # deadline_date = year+'-'+task_history.submission.strftime("%m")+'-'+str(last_date)
    deadline_date = datetime.strptime(
        year + "-" + task_history.submission.strftime("%m") + "-" + str(last_date),
        "%Y-%m-%d",
    ).date()
    employee = get_object_or_404(User, username=task_history.employee.username)
    tasks = TaskHistory.objects.all().filter(
        employee=employee, submission__month=task_history.submission.strftime("%m")
    )
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay

    # Deductions

    loan = Decimal(total_pay) * Decimal("0.2")
    computer_maintenance = 500
    food_accomodation = 1000
    health = 500
    laptop_saving = 1000
    total_deduction = (
            Decimal(loan)
            + Decimal(computer_maintenance)
            + Decimal(food_accomodation)
            + Decimal(health)
            + Decimal(laptop_saving)
    )

    # Bonus
    Lap_Bonus = 500
    if points.get("Your_Total_Points") == None:
        pointsearning = 0
    else:
        pointsearning = points.get("Your_Total_Points")

    Night_Bonus = Decimal(total_pay) * Decimal("0.02")
    if month in (12, 1) and day in (24, 25, 26, 31, 1, 2):
        holidaypay = 3000.00
    else:
        holidaypay = 0.00
    EOM = 0
    EOQ = 0
    EOY = 0
    yearly = 12000
    total_bonus = (
            Decimal(pointsearning)
            + Decimal(holidaypay)
            + Decimal(EOM)
            + Decimal(EOQ)
            + Decimal(EOY)
            + Night_Bonus
    )
    # Net Pay
    try:
        net = total_pay - total_bonus - total_deduction
    except (TypeError, AttributeError):
        net = total_pay

    context = {
        # deductions
        "laptop_saving": laptop_saving,
        "computer_maintenance": computer_maintenance,
        "food_accomodation": food_accomodation,
        "health": health,
        "loan": loan,
        "total_deduction": total_deduction,
        # bonus
        "Night_Bonus": Night_Bonus,
        "pointsearning": pointsearning,
        "holidaypay": holidaypay,
        "yearly": yearly,
        # General
        "tasks": tasks,
        "deadline_date": deadline_date,
        "today": today,
        "total_pay": total_pay,
        "net": net,
    }

    if request.user == employee:
        # return render(request, 'management/daf/paystub.html', context)
        return render(request, "management/daf/payslip.html", context)
    elif request.user.is_superuser:
        # return render(request, 'management/daf/paystub.html', context)
        return render(request, "management/daf/payslip.html", context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')


activities = ["one one one", "one one one session", "one one one sessions"]
myactivities = ["oneoneone", "oneoneonesession", "oneoneonesessions"]
activitiesmodified = [activity.lower().translate({ord(c): None for c in string.whitespace}) for activity in activities]
print(activitiesmodified)


@register.filter(name='activitieslist')
def activitieslist(value, myactivities):
    return True if value in myactivities else False


def usertask(request, user=None, *args, **kwargs):
    request.session["siteurl"] = settings.SITEURL
    # tasks=Task.objects.all().order_by('-submission')
    # user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
    # Amount=Task.objects.all().aggregate(Your_Total_GoalAmount=Sum('mxearning'))
    # total_duration=Task.objects.all().aggregate(Sum('duration'))
    # mxearning=Task.objects.filter().aggregate(Your_Total_AssignedAmt=Sum('mxearning'))
    # paybalance=round(bal,2)
    # balance=paybalance.quantize(Decimal('0.01'))
    # salary = [task.pay for pay in Task.objects.all().values()]
    computer_maintenance = 500
    food_accomodation = 1000
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
    current_user = request.user
    employee = get_object_or_404(User, username=kwargs.get("username"))
    tasks = Task.objects.all().filter(employee=employee)
    # tasks = Task.objects.filter(user__username=request.user)
    points_count = Task.objects.filter(
        description__in=['Meetings', 'General', 'Sprint', 'DAF', 'Recruitment', 'Job Support', 'BI Support'],
        employee=employee)
    point_check = points_count.aggregate(Your_Total_Points=Sum("point"))
    num_tasks = tasks.count()
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    mxpoints = tasks.aggregate(Your_Total_MaxPoints=Sum("mxpoint"))
    earning = tasks.aggregate(Your_Total_Pay=Sum("mxearning"))
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    Points = points.get("Your_Total_Points")
    MaxPoints = mxpoints.get("Your_Total_MaxPoints")
    pay = earning.get("Your_Total_Pay")
    GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    pay = earning.get("Your_Total_Pay")
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay
    try:
        paybalance = Decimal(GoalAmount) - Decimal(total_pay)
    except (TypeError, AttributeError):
        paybalance = 0

    loan = Decimal(total_pay) * Decimal("0.2")

    try:
        net = total_pay - computer_maintenance - food_accomodation - loan
    except (TypeError, AttributeError):
        net = total_pay - computer_maintenance - food_accomodation
    try:
        pointsbalance = Decimal(MaxPoints) - Decimal(Points)
    except (TypeError, AttributeError):
        pointsbalance = 0

    # 1st month
    last_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month1.day)

    last_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=last_day_of_prev_month2.day)

    # 3rd month
    last_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=last_day_of_prev_month3.day)
    # employee__username=request.user
    print(request.user)
    # print(employee__username)
    history = TaskHistory.objects.filter(
        Q(submission__gte=start_day_of_prev_month3),
        Q(submission__lte=last_day_of_prev_month1),
        Q(employee__username=request.user)
    )

    average_earnings = 0
    counter = 3
    for data in history.all():
        average_earnings += data.get_pay
        # counter = counter+1 
        counter = 3
    average_earnings = average_earnings / counter
    if average_earnings == 0:
        average_earnings = GoalAmount

    # try:
    #     average_earnings = average_earnings / counter 
    # except Exception as ZeroDivisionError:
    #     average_earnings = GoalAmount
    # activitysession="one one one session"
    activities = ["one one one", "one one one session", "one one one sessions"]
    activitiesmodified = [activity.lower().translate({ord(c): None for c in string.whitespace}) for activity in
                          activities]
    print(activitiesmodified)
    deadline_date_modify = deadline_date.strftime("%Y/%m/%d")
    context = {
        'activitiesmodified': activitiesmodified,
        "payday": payday,
        "num_tasks": num_tasks,
        "tasks": tasks,
        "Points": Points,
        "MaxPoints": MaxPoints,
        "pay": pay,
        "GoalAmount": GoalAmount,
        "paybalance": paybalance,
        "pointsbalance": pointsbalance,
        "time_remaining_days": time_remaining_days,
        "time_remaining_hours": time_remaining_hours,
        "time_remaining_minutes": time_remaining_minutes,
        "total_pay": total_pay,
        "loan": loan,
        "net": net,
        "point_check": point_check,
        "average_earnings": average_earnings,
        "enddate": deadline_date_modify
    }

    # setting  up session
    request.session["employee_name"] = kwargs.get("username")

    if request.user.is_superuser or request.user == employee:
        return render(request, "management/daf/usertasks.html", context)
    elif request.user.is_superuser:
        return render(request, "management/daf/tasklist.html", context)
    else:
        # raise Http404("Login/Wrong Page: Contact Admin Please!")
        return redirect("main:layout")


def usertaskhistory(request, user=None, *args, **kwargs):
    # tasks=Task.objects.all().order_by('-submission')
    # user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
    # Amount=Task.objects.all().aggregate(Your_Total_GoalAmount=Sum('mxearning'))
    # total_duration=Task.objects.all().aggregate(Sum('duration'))
    # mxearning=Task.objects.filter().aggregate(Your_Total_AssignedAmt=Sum('mxearning'))
    # paybalance=round(bal,2)
    # balance=paybalance.quantize(Decimal('0.01'))
    # salary = [task.pay for pay in Task.objects.all().values()]
    computer_maintenance = 500
    food_accomodation = 1000
    deadline_date = date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )
    delta = deadline_date - date.today()
    time_remaining = delta.days
    current_user = request.user
    try:
        task_history = TaskHistory.objects.get(pk=kwargs.get("pk"))
    except TaskHistory.DoesNotExist:
        print("You dont have any matching records in the database")
    employee = get_object_or_404(User, username=task_history.employee)
    tasks = TaskHistory.objects.all().filter(
        employee=employee, submission__month=task_history.submission.strftime("%m")
    )
    # tasks = Task.objects.filter(user__username=request.user)
    num_tasks = tasks.count()
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    mxpoints = tasks.aggregate(Your_Total_MaxPoints=Sum("mxpoint"))
    earning = tasks.aggregate(Your_Total_Pay=Sum("mxearning"))
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    Points = points.get("Your_Total_Points")
    MaxPoints = mxpoints.get("Your_Total_MaxPoints")
    pay = earning.get("Your_Total_Pay")
    GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    pay = earning.get("Your_Total_Pay")
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay
    try:
        paybalance = Decimal(GoalAmount) - Decimal(total_pay)
    except (TypeError, AttributeError):
        paybalance = 0

    loan = Decimal(total_pay) * Decimal("0.2")

    try:
        net = total_pay - computer_maintenance - food_accomodation - loan
    except (TypeError, AttributeError):
        net = total_pay - computer_maintenance - food_accomodation
    try:
        pointsbalance = Decimal(MaxPoints) - Decimal(Points)
    except (TypeError, AttributeError):
        pointsbalance = 0

    context = {
        "tasksummary": tasksummary,
        "num_tasks": num_tasks,
        "tasks": tasks,
        "Points": Points,
        "MaxPoints": MaxPoints,
        "pay": pay,
        "GoalAmount": GoalAmount,
        "paybalance": paybalance,
        "pointsbalance": pointsbalance,
        "time_remaining": time_remaining,
        "total_pay": total_pay,
        "loan": loan,
        "net": net,
    }

    # setting  up session
    request.session["task_id"] = kwargs.get("pk")

    if request.user == employee:
        return render(request, "management/daf/usertaskhistory.html", context)
    elif request.user.is_superuser:
        return render(request, "management/daf/usertaskhistory.html", context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")


def prefix_zero(month:int) -> str:
    return str(month) if month > 9 else '0' + str(month)


def normalize_period(year:int, month:int) -> str:
    if month > 12:
        year = year + (month//12)
        month = month % 12
    elif month < 1:
        year = year - (-month//12)
        month = (-month) % 12

    if month == 0:
        month = 12

    if month > 0 and month < 10:
        month = '0' + str(month)

    return str(year) + '-' + str(month)

def loan_update_save(loantable,user_data,employee,total_pay,payslip_config):
    # loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
    # training_loan = user_data.order_by('-id')[0]
    if not user_data.exists():
        loan_data=addloantable(loantable, employee, total_pay, payslip_config, user_data)
        loan_data.save()
    else:
        try:
            training_loan = user_data.order_by('-id')[0]
        except:
            training_loan=None
        if training_loan:
            loan_data = addloantable(loantable, employee, total_pay, payslip_config, user_data)
            if loan_data:
                loan_data.save()
            # loan_data=updateloantable(user_data,employee,total_pay,payslip_config)
        else:
            loan_data = updateloantable(user_data, employee, total_pay, payslip_config)
            # loan_data=addloantable(loantable,employee,total_pay,payslip_config,user_data)

def pay(request, user=None, *args, **kwargs):
    employee = get_object_or_404(User, username=kwargs.get("username"))
    userprofile = UserProfile.objects.get(user_id=employee)
    tasks = Task.objects.all().filter(employee=employee)
    LBLS=LBandLS.objects.filter(user=employee)
    user_data=TrainingLoan.objects.filter(user=employee, is_active=True)
    loantable=TrainingLoan
    # lbandls = LBandLS.objects.get(user_id=employee)
    try:
        payslip_config = paymentconfigurations(PayslipConfig,employee)
    except PayslipConfig.DoesNotExist:
        link=f"finance:paymentconfigs"
        title='CONFIGURATIONS'
        message=f'We dont have existing configs for this employee/admin,proceed to set configs'
        context={
            "link":link,
            "title":title,
            "message":message
        }
        return render(request,'main/errors/generalerrors.html',context)
    today,year,month,day,deadline_date=paytime()
    task_obj=Task.objects.filter(submission__contains=year)
    mxearning,points=payinitial(tasks)
    total_pay = Decimal(0)
    for task in tasks:
        total_pay = total_pay + task.get_pay
    # Deductions
    # print(loan_amount,loan_payment,balance_amount)
    # loan_payment = round(total_pay * payslip_config.loan_repayment_percentage, 2)
    loan_amount, loan_payment, balance_amount = loan_computation(total_pay, user_data, payslip_config)
    print(loan_amount, loan_payment, balance_amount)
    logger.debug(f'balance_amount: {balance_amount}')
    loan_update_save(loantable,user_data,employee,total_pay,payslip_config)
    food_accomodation,computer_maintenance,health,kra=deductions(payslip_config,total_pay)
    # print("what is this----->",loan_update_save(loantable,user_data,employee,total_pay,payslip_config))
    userprofile = UserProfile.objects.get(user_id=employee)
    if userprofile.laptop_status == True:
        laptop_saving = Decimal(0)
        if LBandLS.objects.filter(user=employee).exists():
            lbandls = LBandLS.objects.get(user_id=employee)
            laptop_bonus = lbandls.laptop_bonus
        else:
            laptop_bonus = Decimal(0)
    else:
        laptop_bonus = Decimal(0)
        if LBandLS.objects.filter(user=employee).exists():
            lbandls = LBandLS.objects.get(user_id=employee)
            laptop_saving = lbandls.laptop_service
        else:
            laptop_saving = Decimal(0)
    laptop_bonus = round(Decimal(laptop_bonus), 2)
    laptop_saving = round(Decimal(laptop_saving), 2)
    # laptop_bonus,laptop_saving=lap_save_bonus(userprofile,LBLS,lbandls)
    # ====================Bonus Section=============================
    pointsearning,Night_Bonus,holidaypay,yearly=bonus(tasks,total_pay,payslip_config)
    # print(pointsearning,Night_Bonus,holidaypay,yearly)

    EOM = Decimal(0.00)  # employee of month
    EOQ = Decimal(0.00)  # employee of quarter
    EOY = Decimal(0.00)  # employee of year
    if month == 12:
        task_obj = Task.objects.filter(submission__contains=year)
        logger.debug(f'task_obj: {task_obj}')
        eoy_users = best_employee(task_obj)
        if (employee,) in eoy_users:
            logger.info('this employee is EOY!')
            EOY = payslip_config.eoy_bonus
    elif month % 3 == 0:
        task_obj = Task.objects.filter(Q(submission__contains=normalize_period(year, month-2))
                                | Q(submission__contains=normalize_period(year, month-1))
                                | Q(submission__contains=normalize_period(year, month)))
        logger.debug(f'task_obj: {task_obj}')
        eoq_users = best_employee(task_obj)
        user_tuple = (employee.username,)
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
    total_deduction,total_bonus= additional_earnings(user_data,tasks,total_pay,payslip_config)
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
    context = {
        # bonus
        "pointsearning": pointsearning,
        "EOM": EOM,
        "EOQ": EOQ,
        "EOY": EOY,
        "laptop_bonus": laptop_bonus,
        "holidaypay": holidaypay,
        "Night_Bonus": Night_Bonus,
        "yearly": yearly,
            # deductions
            "loan": loan_payment,
            "food_accomodation": food_accomodation,
            "computer_maintenance": computer_maintenance,
            "health": health,
            "laptop_saving": laptop_saving,
            "kra": kra,
    
            # General
            "total_pay": total_pay,
            'total_value': total_value,
            "total_deduction": total_deduction,
            'net': net,
            'net_pay': net_pay,
            "balance_amount": balance_amount,
            "tasks": tasks,
            "deadline_date": deadline_date,
            "today": today,
        }
    if request.user == employee or request.user.is_superuser:
        return render(request, "management/daf/payslip.html", context)
    else:
        message="Either you are not Login or You are forbidden from visiting this page-contact admin at info@codanalytics.net"
        return render(request, "main/errors/404.html",{"message":message})

class TaskDetailView(DetailView):
    queryset = Task.objects.all()
    template_name = "management/daf/task_detail.html"

    # ordering = ['-datePosted']

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetailView, self).get_context_data(*args, **kwargs)
        # print(context)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get("pk")
        return Task.objects.filter(pk=pk)


class UserTaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "management/daf/employee_tasks.html"

    # paginate_by = 5
    def get_queryset(self):
        # request=self.request
        # user=self.kwargs.get('user')
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        # tasks=Task.objects.all().filter(employee=user)

        return Task.objects.all().filter(employee=user)


@method_decorator(login_required, name="dispatch")
class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    success_url = "/management/tasks"
    fields = [
        "groupname",
        "category",
        "employee",
        "activity_name",
        "description",
        "point",
        "mxpoint",
        "mxearning",
    ]

    # fields=['user','activity_name','description','point']
    def form_valid(self, form):
        # form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return redirect("management:tasks")

    def test_func(self):
        task = self.get_object()
        if self.request.user.is_superuser:
            return True
        # elif self.request.user == task.employee:
        #     return True
        return False


@method_decorator(login_required, name="dispatch")
class UsertaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task

    # success_url = "/management/thank"
    def get_success_url(self):
        task = self.get_object()
        return reverse("management:user_task", kwargs={"username": str(task.employee)})

    # fields=['group','category','user','activity_name','description','slug','point','mxpoint','mxearning']
    fields = ["category", "employee", "activity_name", "description", "point"]

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user.is_superuser or self.request.user.is_admin:
            return True
        elif self.request.user == task.employee:
            return True
        return False


@login_required
def gettotalduration(request):
    employee_duration = Tracker.objects.filter(author=request.POST["name"])
    total_duration = 0
    for data in employee_duration.all():
        total_duration += data.duration

    return JsonResponse({"success": True, "value": total_duration})


@method_decorator(login_required, name="dispatch")
class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = "/accounts/tasklist"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


# =============================EMPLOYEE EVIDENCE========================================
def newevidence(request, taskid):
    if request.method == "POST":
        form = EvidenceForm(request.POST)
        # Check whether the task exist then only we allow to create evidence
        try:
            task = Task.objects.get(id=taskid)
            activity_name = task.activity_name
        except:
            return render(request, "errors/404.html")

        if form.is_valid():
            points, maxpoints, taskname = \
                Task.objects.values_list("point", "mxpoint", "activity_name").filter(id=taskid)[0]
            jobsup_list = ["job support", "job_support", "jobsupport"]
            if points != maxpoints and taskname.lower() not in jobsup_list:
                Task.objects.filter(id=taskid).update(point=points + 1)

            # User will taken from the request
            data = form.cleaned_data
            link = data['link']
            if not link:
                messages.error(request, "please provide evidence link")
                return render(request, "management/daf/evidence_form.html", {"form": form})
            try:
                a=requests.get(link)
                if a.status_code == 200:
                    user_list=[]
                    check = TaskLinks.objects.filter(link=link)
                    if check.exists():
                        users = check.values_list('added_by__username')
                        for username in users:
                            user_list.append(username[0])
                        act_list = ['BOG', 'BI Sessions', 'DAF Sessions']
                        if activity_name in act_list:
                            if request.user.username in user_list:
                                messages.error(request, "you have already uploaded this link")
                                return render(request, "management/daf/evidence_form.html", {"form": form})
                            form.save()
                            return redirect("management:evidence")
                        else:
                            messages.error(request, "this link is already uploaded")
                            return render(request, "management/daf/evidence_form.html", {"form": form})

                    form.save()
                    return redirect("management:evidence")
                else:
                    messages.error(request, "link is not valid,please check again")
                    return render(request, "management/daf/evidence_form.html", {"form": form})

            except:
                messages.error(request, "Please check your link")
                return render(request, "management/daf/evidence_form.html", {"form": form})

    else:
        form = EvidenceForm()

    return render(request, "management/daf/evidence_form.html", {"form": form})


def evidence(request):
    links = TaskLinks.objects.all().order_by("-created_at")
    return render(request, "management/daf/evidence.html", {"links": links})


def userevidence(request, user=None, *args, **kwargs):
    # current_user = request.user
    employee = get_object_or_404(User, username=kwargs.get("username"))
    userlinks = TaskLinks.objects.all().filter(added_by=employee).order_by("-created_at")
    return render(request, "management/daf/userevidence.html", {"userlinks": userlinks})

def evidence_update_view(request, id, *args, **kwargs):
    context = {}
    # fetch the object related to passed id
    obj = get_object_or_404(TaskLinks, id=id)
    # pass the object as instance in form
    form = EvidenceForm(request.POST or None, instance=obj)
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        # try:
        #     username=kwargs.get("username")
        #     return redirect("management:user_evidence", username)
        # except:
        return redirect('management:evidence')
    # add form dictionary to context
    # context["form"] = form
    message='Edit Evidence'
    context={
        "form":form,
        "message":message
    }
    return render(request, "main/snippets_templates/generalform.html", context)

# @method_decorator(login_required, name="dispatch")
# class EvidenceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = TaskLinks
#     success_url = "/management/evidence"
#     message="Edit Evidence"
   
#     fields = [
#             #    "task",
#             #    "added_by",
#                "link_name",
#                "linkpassword",
#                "description",
#                "doc",
#                "link",
#                "linkpassword",
#                "is_active",
#                "is_featured",
#            ]
#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         evidence = self.get_object()
#         if self.request.user.is_admin or self.request.user.is_superuser:
#             return True
#         elif self.request.user == evidence.added_by:
#             return True
#         return False



# =============================EMPLOYEE SESSIONS========================================
class SessionCreateView(LoginRequiredMixin, CreateView):
    model=Training
    success_url = "/management/session"
    fields= "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SessionListView(ListView):
    # queryset = DSU.objects.all(type="Staff").order_by("-created_at")
    queryset=Training.objects.all().order_by("-created_date")
    template_name = "management/departments/hr/sessions.html"

class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Training
    success_url = "/management/sessions"
    # fields = ["name", "slug", "description", "is_active", "is_featured"]
    fields = "__all__"
    # form = DepartmentForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if  self.request.user or self.request.user.is_admin or self.request.user.is_superuser:
            return True
        return False

# =============================EMPLOYEE ASSESSMENTS========================================
@login_required
def assess(request):
    if request.method == "POST":
        form = ManagementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management:assessment")
    else:
        form = ManagementForm()
    return render(request, "management/departments/hr/assess_form.html", {"form": form})


class AssessListView(ListView):
    # queryset = DSU.objects.all(type="Staff").order_by("-created_at")
    queryset=DSU.objects.all().order_by("-created_at")
    template_name = "management/departments/hr/assessment.html"

    # -----------------------------REQUIREMENTS---------------------------------


def active_requirements(request, Status=None, *args, **kwargs):
    active_requirements = Requirement.objects.all().filter(is_active=True)
    context = {"active_requirements": active_requirements}
    return render(request, "management/doc_templates/active_requirements.html", context)


def requirements(request):
    requirements = Requirement.objects.all().order_by("-id")
    return render(
        request,
        "management/doc_templates/requirementlist.html",
        {"requirements": requirements},
    )


def newrequirement(request):
    if request.method == "POST":
        form = RequirementForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.creator=request.user
            print(instance.creator)
            instance.save()
            # form.save()
            if (
                    not get_user_model().objects.get(pk=request.POST["assigned_to"])
                        == request.user
            ):
                subject = "Task assign on CodaTraining"
                to = get_user_model().objects.get(pk=request.POST["assigned_to"]).email
                if request.is_secure():
                    protocol = "https://"
                else:
                    protocol = "http://"
                # html_content = f"""
                #     <span><h3>Requirement: </h3>{request.POST['what']}<br>
                #     <a href='{protocol+request.get_host()+reverse('management:RequirementDetail',
                #     kwargs={'pk':form.instance.id})}'>click here</a><br>
                #     <b>Dead Line: </b><b style='color:red;'>
                #     {request.POST['delivery_date']}</b><br><b>Created by:
                #     {request.user}</b></span>"""
                # email_template(subject, to, html_content)
                context = {
                    'request_what': request.POST['what'],
                    'url': protocol + request.get_host() + reverse('management:RequirementDetail',
                                                                   kwargs={'pk': form.instance.id}),
                    'delivery_date': request.POST['delivery_date'],
                    'user': request.user,
                }
                # send_email(category=request.user.category, to_email=[to, ], subject=subject,
                #            html_template='email/newrequirement.html', context=context)
            return redirect("management:requirements-active")
    else:
        form = RequirementForm()
    return render(
        request, "management/doc_templates/requirement_form.html", {"form": form}
    )


class RequirementDetailView(DetailView):
    template_name = "management/doc_templates/single_requirement.html"
    model = Requirement
    ordering = ["created_at "]

class RequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = Requirement
    success_url = "/management/requirements"
    fields = [
                "status","assigned_to","requestor","company",
                "category","app","delivery_date","duration","what",
                "why","how","comments","doc","is_active",
             ]
    form = RequirementForm
    def form_valid(self, form):
        # form.instance.author=self.request.user
        if self.request.user.is_superuser or self.request.user :
            if (
                not get_user_model().objects.get(pk=self.request.POST["assigned_to"])
                == self.request.user
                and not get_user_model().objects.get(
                    pk=self.request.POST["assigned_to"]
                )
                == Requirement.objects.get(pk=form.instance.id).assigned_to
            ):
                subject = "Task assign on CodaTraining"
                to = (
                    get_user_model()
                    .objects.get(pk=self.request.POST["assigned_to"])
                    .email
                )
                if self.request.is_secure():
                    protocol = "https://"
                else:
                    protocol = "http://"
                html_content = f"""
                    <span><h3>Requirement: </h3>{self.request.POST['what']}<br>
                    <a href='{protocol+self.request.get_host()+reverse('management:RequirementDetail',
                    kwargs={'pk':form.instance.id})}'>click here</a><br>
                    <b>Dead Line: </b><b style='color:red;'>
                    {self.request.POST['delivery_date']}</b><br><b>Created by: 
                    {self.request.user}</b></span>"""
                email_template(subject, to, html_content)
            return super().form_valid(form)
        else:
            return redirect("management:requirements-active")

    def test_func(self):
        requirement = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        # elif self.request.user == requirement.created_by:
        #     return True
        return False


# class RequirementUpdateView(LoginRequiredMixin, UpdateView):
#     model = Requirement
#     success_url = "/management/activerequirements"
#     fields = [
#         "created_by",
#         "assigned_to",
#         "requestor",
#         "company",
#         "category",
#         "app",
#         "delivery_date",
#         "duration",
#         "what",
#         "why",
#         "how",
#         "doc",
#         "is_active",
#     ]
#     form = RequirementForm

#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         if self.request.user.is_superuser:
#             req_obj = Requirement.objects.get(pk=form.instance.id)
#             old_dev = req_obj.assigned_to

#             if (not get_user_model().objects.get(pk=self.request.POST["assigned_to"]) == self.request.user
#                     and not get_user_model().objects.get(pk=self.request.POST["assigned_to"]
#                                                          ) == old_dev
#             ):
#                 if self.request.is_secure():
#                     protocol = "https://"
#                 else:
#                     protocol = "http://"

#                 subject = 'Task has been reassigned on CodaTraining'
#                 old_dev_obj = get_user_model().objects.get(username=old_dev)
#                 old_dev_email = old_dev_obj.email
#                 context = {
#                     'user': old_dev,
#                     'url': protocol + self.request.get_host() + reverse('management:RequirementDetail',
#                                                                         kwargs={'pk': form.instance.id}),
#                     'req_id': req_obj.id,
#                     'delivery_date': req_obj.delivery_date,
#                 }
#                 # logger.debug(f'old_dev_email: {old_dev_email}')
#                 # logger.debug(f'context: {context}')
#                 send_email(
#                     category=old_dev_obj.category,
#                     to_email=[old_dev_email, ],
#                     subject=subject,
#                     html_template='email/requirement_reassigned.html',
#                     context=context
#                 )

#                 subject = "Task assign on CodaTraining"
#                 to = (
#                     get_user_model()
#                     .objects.get(pk=self.request.POST["assigned_to"])
#                     .email
#                 )
#                 context = {
#                     'request_what': self.request.POST['what'],
#                     'url': protocol + self.request.get_host() + reverse('management:RequirementDetail',
#                                                                         kwargs={'pk': form.instance.id}),
#                     'delivery_date': self.request.POST['delivery_date'],
#                     'user': self.request.user,
#                 }
#                 send_email(
#                     category=self.request.user.category,
#                     to_email=[to, ],
#                     subject=subject,
#                     html_template='email/RequirementUpdateView.html',
#                     context=context
#                 )

#             return super().form_valid(form)
#         else:
#             return redirect("management:requirements-active")

#     def test_func(self):
#         requirement = self.get_object()
#         if self.request.user.is_superuser:
#             return True
#         elif self.request.user == requirement.created_by:
#             return True
#         return False


class RequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = Requirement
    success_url = "/management/requirements"

    def test_func(self):
        # creator = self.get_object()
        # if self.request.user == creator.username:
        if self.request.user.is_superuser:
            return True
        return False
# ====================ESTIMATEVIEWS===============================
class EstimateCreateView(LoginRequiredMixin, CreateView):
    model=Estimate
    success_url = "/management/activerequirements"
    fields= "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EstimateListView(ListView):
    model = Estimate
    template_name = "management/doc_templates/estimates.html"
    context_object_name = "estimates"
    ordering = ["-created_at"]

def getaveragetargets(request):
    print("+++++++++getaveragetargets+++++++++")
    taskname = request.POST["taskname"]
    # 1st month
    last_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month1.day)

    last_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=last_day_of_prev_month2.day)

    # 3rd month
    last_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=last_day_of_prev_month3.day)

    history = TaskHistory.objects.filter(Q(activity_name=taskname), Q(created_at__gte=start_day_of_prev_month3),
                                         Q(created_at__lte=last_day_of_prev_month1))

    results = {"target_points": 0, "target_amount": 0}
    counter = 0
    for data in history.all():
        results["target_points"] += data.mxpoint
        results["target_amount"] += data.mxearning
        counter = counter + 1
    try:
        results["target_points"] = results["target_points"] / counter
        results["target_amount"] = results["target_amount"] / counter
    except Exception as ZeroDivisionError:
        results["target_points"] = 0.0
        results["target_amount"] = 0.0

    return JsonResponse(results)


def filterbycategory(request):
    category = request.POST["category"]
    print("category", category)

    tasks = Task.objects.filter(category__title=category)
    result = []
    details = {}
    for data in tasks.all():
        details["group"] = data.groupname
        details["deadline"] = data.deadline.strftime("%d %b %Y")
        details["submission"] = data.submission.strftime("%d %b %Y")
        details["point"] = data.point
        details["mxpoint"] = data.mxpoint
        details["mxearning"] = float(data.mxearning)
        details["get_pay"] = float(data.get_pay)
        details["id"] = data.id
        details["employee"] = data.employee.username
        details["first_name"] = data.employee.first_name
        details["last_name"] = data.employee.last_name
        details["description"] = data.description
        details["activity_name"] = data.activity_name
        details["get_absolute_url"] = str(data.category.get_absolute_url)
        result.append(details.copy())
    # print(result)
    return JsonResponse({"result": result}, safe=False)


class AdsContent(ListView):
    model = Advertisement
    template_name = "management/advertisement.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class AdsCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    template_name = "management/create_advertisement.html"
    fields = "__all__"
    success_url = "/management/advertisement"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    template_name = "management/create_advertisement.html"
    fields = "__all__"
    success_url = "/management/advertisement"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

import calendar, string
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
from django.db.models import Q
from mail.custom_email import send_email
from application.models import UserProfile
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
    # TaskGroups,
    Task,
    TaskHistory,
    TaskLinks,
    Requirement,
    LBandLS
)
from data.models import DSU
from finance.models import Default_Payment_Fees, LoanUsers, TrainingLoan

from django.conf import settings
from django.contrib.auth import get_user_model

from coda_project import settings
from datetime import date, timedelta
from django.db.models import Q

from accounts.models import Tracker, Department, TaskGroups
from .models import (
    PayslipConfig,
    Payslip,
    RetirementPackage,
    Loan,
    LaptopBonus,
    LaptopSaving,
    MonthlyPoints
)

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
    success_url = "/management/newtask"
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
                    des, po, maxpo, maxear = Task.objects.values_list("description", "point", "mxpoint", "mxearning").filter(
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


def payslip(request, user=None, *args, **kwargs):
    default_payment_fees = Default_Payment_Fees.objects.all().first()

    deadline_date = date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )
    today = date(date.today().year, date.today().month, date.today().day)
    year = date.today().year
    month = date.today().month
    day = date.today().day

    employee = get_object_or_404(User, username=kwargs.get("username"))
    tasks = Task.objects.all().filter(employee=employee)
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    GoalAmount = mxearning.get("Your_Total_AssignedAmt")
    points = tasks.aggregate(Your_Total_Points=Sum("point"))
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay

    # Deductions
    # if loan already paid so, no need add to the deductions
    # currently, one of the employee from coda mannually calculate
    # the loan amount and add to the deductions. We need to create
    # new database table to store the loan amount and add to the database.
    loan = Decimal(total_pay) * Decimal("0.2")
    balance_amount = 0
    if TrainingLoan.objects.filter(user=employee).exists():
        training_loan = TrainingLoan.objects.filter(user=employee).order_by('-id')[0]
        loan = training_loan.detection_amount
        if LoanUsers.objects.filter(user=employee, is_loan=True).exists():
            balance_amount = training_loan.balance_amount
        else:
            balance_amount = 0
    else:
        if default_payment_fees:
            loan_amount = Decimal(default_payment_fees.loan_amount)
            balance_amount = loan_amount - loan
        else:
            loan_amount = 0

    userprofile = UserProfile.objects.get(user_id=employee)
    if userprofile.laptop_status == True:
        laptop_saving = 0
        if LBandLS.objects.filter(user=employee).exists():
            lbandls = LBandLS.objects.get(user_id=employee)
            laptop_bonus = lbandls.laptop_bonus
        else:
            laptop_bonus = 0
    else:
        laptop_bonus = 0
        if LBandLS.objects.filter(user=employee).exists():
            lbandls = LBandLS.objects.get(user_id=employee)
            laptop_saving = lbandls.laptop_service
        else:
            laptop_saving = 0

    laptop_bonus = '{0:.2f}'.format(laptop_bonus)
    laptop_saving = '{0:.2f}'.format(laptop_saving)

    loan = round(loan, 2)
    balance_amount = round(balance_amount, 2)

    kra = Decimal(total_pay) * Decimal("0.30")
    # if employee use company computer, add the charge to the deductions.
    computer_maintenance = 500
    # if user self paid the food accomodation, no need to add to the deductions
    food_accomodation = 1000
    # same as food accomodation.
    health = 500
    # if company gave the laptop to the employee. They will charge or deduct from the total pay. We are currently charging 1000 until it gets to the 20000.
    # if employee achieved the 20000 threshold it will then no deduction.
    # if the employee buy a laptop in 2, or so months. Then we'll stop dedcuting and
    # the amount that we deducted the last month will be added to the total pay.
    # laptop_saving = 1000
    total_deduction = (
            Decimal(loan)
            + Decimal(computer_maintenance)
            + Decimal(food_accomodation)
            + Decimal(health)
            + Decimal(laptop_saving)
    )

    # Bonus
    # if you have your own laptop company will give you a bonus.
    Lap_Bonus = 500  # make it 1000 later.
    if points.get("Your_Total_Points") == None:
        pointsearning = 0
    else:
        pointsearning = points.get("Your_Total_Points")

    # if a employee working on night or different timezone will get a bonus.
    Night_Bonus = Decimal(total_pay) * Decimal("0.02")  # 2% of the total pay.
    # we should create an attendance system, who mark an attendance of every employee.
    # leave it for the time being.
    if month in (12, 1) and day in (24, 25, 26, 31, 1, 2):
        holidaypay = 3000.00
    else:
        holidaypay = 0.00
    # for employee of year, we need to filter out the most daf points of the month.
    # for message point we need to divide the points with 10 (we need an API to get the message points)
    # for rating points we need to divide it by 2 (we already have rating model)
    # DAF (tasks points) points will be multiplied by 2 (we already have tasks table for tasks points)
    # 1-1 (second level tasks) session points will be multiplied by 3
    # total number of meetings points.
    # mainly 'go to meetings'(1-1 meetings) and 'zoom meetings'.
    EOM = 0  # employee of month
    EOQ = 0  # employee of quarter
    EOY = 0  # employee of year

    # if user.joining_date > 12 months ago he will get 12000ksh bonus.
    # if user spent 25 months, the program will check if user already
    # claimed the previous 12000 bonus. If not, he will get double bonus.
    # # Transaction => will note every transaction of the employee.
    # # if user earnt 1000 we'll add this to the transaction module.
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
        net = total_pay + total_bonus - total_deduction
    except (TypeError, AttributeError):
        net = total_pay

    context = {
        # deductions
        "laptop_saving": laptop_saving,
        "computer_maintenance": computer_maintenance,
        "food_accomodation": food_accomodation,
        "health": health,
        "loan": loan,
        "kra": kra,
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
        "balance_amount": balance_amount,
        "laptop_bonus": laptop_bonus
    }

    if request.user == employee:
        # return render(request, 'management/daf/paystub.html', context)
        return render(request, "management/daf/payslip.html", context)
    elif request.user.is_superuser:
        # return render(request, 'management/daf/paystub.html', context)
        return render(request, "management/daf/payslip.html", context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")


def default_payslip(request, *args, **kwargs):
    received_username = kwargs.get('username')
    employee = None
    if request.user.is_superuser and received_username is not None:
        logger.debug(f'received_username: {received_username}')
        try:
           employee = get_user_model().objects.get(username=received_username)
        except:
            pass
    elif request.user.id:
        logger.debug(f'request.user.id: {request.user.id}')
        # employee = get_object_or_404(User, id=int(request.user.id))
        try:
            employee = get_user_model().objects.get(id=int(request.user.id))
        except:
            pass
    logger.debug(f'employee: {employee}')
    if not employee:
        logger.error('employee is not found!')
        raise Http404("Login and try again!")

    today = date.today()
    month = today.strftime("%Y-%m")
    logger.debug(f'month: {month}')

    tasks = Task.objects.all().filter(employee=employee, submission__contains=month)
    logger.debug(f'tasks: {tasks}')

    if not tasks:
        logger.error('there is no task in the database!')
        raise Http404("No tasks found!")

    earned_salary = Decimal(0)
    points_earned = Decimal(0)
    for t in tasks:
        earned_salary = earned_salary + t.get_pay
        points_earned = points_earned + Decimal(t.point)
    logger.debug(f'earned_salary: {earned_salary}')
    logger.debug(f'points: {points_earned}')

    try:
        payslip_config_obj = PayslipConfig.objects.get(user=employee)
    except:
        logger.error('payslip configuration for this employee is not found!')
        raise Http404("No Payslip Configuration found!")
    # logger.debug(f'payslip_config_obj: {payslip_config_obj}')

    # Bonus and Deductions
    loan_status = payslip_config_obj.loan_status
    computer_maintenance = Decimal(0)
    if loan_status is True:
        loan_deduction = earned_salary * payslip_config_obj.loan_repayment_percentage
        logger.debug(f'loan_deduction: {loan_deduction}')

        # loan_balance = Loan.objects.filter(user=employee).latest('balance')
        # loan_balance = Decimal(0)

        last_month = today + relativedelta(months=-1)
        last_month = last_month.strftime("%Y-%m")
        logger.debug(f'last_month: {last_month}')

        try:
            loan_balance = Loan.objects.filter(user=employee, period__contains=last_month).balance
            if loan_balance <= loan_deduction:
                loan_deduction = loan_balance
                loan_balance = Decimal(0)
            else:
                loan_balance = loan_balance - loan_deduction
        except:
            loan_balance = 0
            loan_deduction = 0
        logger.debug(f'loan_balance: {loan_balance}')

    else:
        # if employee use company computer, add the charge to the deductions.
        computer_maintenance = payslip_config_obj.computer_maintenance

    lb_amount = Decimal(0)
    ls_amount = Decimal(0)
    laptop_status = payslip_config_obj.laptop_status
    if laptop_status:
        lb_amount = payslip_config_obj.lb_amount
    else:
        ls_amount = payslip_config_obj.ls_amount
        ls_total = LaptopSaving.objects.filter(user=employee).latest('total')
        ls_max_limit = payslip_config_obj.ls_max_limit

        if (ls_amount + ls_total) > ls_max_limit:
            ls_amount = ls_max_limit - ls_total

    kra = earned_salary * payslip_config_obj.kra_percentage
    food_accommodation = payslip_config_obj.food_accommodation
    health = payslip_config_obj.health

    deductions = {
        'computer_maintenance': round(computer_maintenance, 2),
        'food_accommodation': round(food_accommodation, 2),
        'health': round(health, 2),
        'kra': round(kra, 2),
        'loan_deduction': round(loan_deduction, 2),
        'ls_amount': round(ls_amount, 2),
    }

    total_deductions = Decimal(0)
    for val in deductions.values():
        total_deductions = total_deductions + val

    # if employee working on night or different timezone will get a bonus. 2% of the total pay.
    night_bonus = earned_salary * payslip_config_obj.night_bonus_percentage

    # we should create an attendance system, who mark an attendance of every employee.
    # leave it for the time being.
    if month in (12, 1):
        holiday_pay = payslip_config_obj.holiday_pay
    else:
        holiday_pay = Decimal(0)

    monthly_point_obj = MonthlyPoints.objects.get(user=employee, period__contains=month)
    if not monthly_point_obj:
        monthly_point_obj = MonthlyPoints(user=employee, period=today, points=points_earned)
    else:
        monthly_point_obj.points = points_earned
    monthly_point_obj.save()

    EOM = Decimal(0)  # employee of month
    EOQ = Decimal(0)  # employee of quarter
    EOY = Decimal(0)  # employee of year

    # retirement package
    rp_amount = payslip_config_obj.rp_starting_amount + (earned_salary * payslip_config_obj.rp_increment_percentage)

    bonus = {
        'EOM': round(EOM, 2),
        'EOQ': round(EOQ, 2),
        'EOY': round(EOY, 2),
        'holiday_pay': round(holiday_pay, 2),
        'lb_amount': round(lb_amount, 2),
        'night_bonus': round(night_bonus, 2),
        'points_earned': round(points_earned, 2),
    }

    total_bonus = Decimal(0)
    for val in bonus.values():
        total_bonus = total_bonus + val

    # Net Pay
    total_earning = earned_salary + total_bonus
    net_earning = total_earning - total_deductions
    round_off = round(net_earning) - net_earning
    net_pay = net_earning + round_off

    deadline_date = date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )

    context = {
        'user': employee,
        'earned_salary': round(earned_salary, 2),
        'bonus': bonus,
        'total_bonus': round(total_bonus, 2),
        'deductions': deductions,
        'total_deductions': round(total_deductions, 2),
        'rp_amount': round(rp_amount, 2),
        'total_earning': round(total_earning, 2),
        'net_earning': round(net_earning, 2),
        'net_pay': round(net_pay, 2),
        'loan_balance': round(loan_balance, 2),
    }
    return render(request, "management/daf/payslip.html", context)


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
            Task.objects.get(id=taskid)
        except:
            return render(request, "errors/404.html")

        if form.is_valid():
            points, maxpoints, taskname = \
            Task.objects.values_list("point", "mxpoint", "activity_name").filter(id=taskid)[0]
            jobsup_list = ["job support", "job_support", "jobsupport"]
            if points != maxpoints and taskname.lower() not in jobsup_list:
                Task.objects.filter(id=taskid).update(point=points + 1)

            # User will taken from the request 
            form.save()
            return redirect("management:evidence")

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
    context["form"] = form
    return render(request, "management\daf\evidence_form.html", context)


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
    queryset = DSU.objects.filter(type="Staff").order_by("-created_at")
    # queryset=DSU.objects.all()
    template_name = "management/departments/hr/assessment.html"

    # -----------------------------REQUIREMENTS---------------------------------


def active_requirements(request, Status=None, *args, **kwargs):
    active_requirements = Requirement.objects.all().filter(is_active=True)
    context = {"active_requirements": active_requirements}
    return render(request, "management/doc_templates/active_requirements.html", context)


def requirements(request):
    requirements = Requirement.objects.all().order_by("-created_by")
    return render(
        request,
        "management/doc_templates/requirements.html",
        {"requirements": requirements},
    )


def newrequirement(request):
    if request.method == "POST":
        form = RequirementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
                send_email(category=request.user.category, to_email=[to, ], subject=subject,
                           html_template='email/newrequirement.html', context=context)
            return redirect("management:requirements-active")
    else:
        form = RequirementForm()
    return render(
        request, "management/doc_templates/requirement_form.html", {"form": form}
    )


class RequirementDetailView(DetailView):
    template_name = "management/doc_templates/single_requirement.html"
    model = Requirement
    ordering = ["-created_at "]


class RequirementUpdateView(LoginRequiredMixin, UpdateView):
    model = Requirement
    success_url = "/management/activerequirements"
    fields = [
        "created_by",
        "assigned_to",
        "requestor",
        "company",
        "category",
        "app",
        "delivery_date",
        "duration",
        "what",
        "why",
        "how",
        "doc",
        "is_active",
    ]
    form = RequirementForm

    def form_valid(self, form):
        # form.instance.author=self.request.user
        if self.request.user.is_superuser:
            req_obj = Requirement.objects.get(pk=form.instance.id)
            old_dev = req_obj.assigned_to

            if (not get_user_model().objects.get(pk=self.request.POST["assigned_to"]) == self.request.user
                    and not get_user_model().objects.get(pk=self.request.POST["assigned_to"]
            ) == old_dev
            ):
                if self.request.is_secure():
                    protocol = "https://"
                else:
                    protocol = "http://"

                subject = 'Task has been reassigned on CodaTraining'
                old_dev_obj = get_user_model().objects.get(username=old_dev)
                old_dev_email = old_dev_obj.email
                context = {
                    'user': old_dev,
                    'url': protocol + self.request.get_host() + reverse('management:RequirementDetail',
                                                                        kwargs={'pk': form.instance.id}),
                    'req_id': req_obj.id,
                    'delivery_date': req_obj.delivery_date,
                }
                # logger.debug(f'old_dev_email: {old_dev_email}')
                # logger.debug(f'context: {context}')
                send_email(
                    category=old_dev_obj.category,
                    to_email=[old_dev_email,],
                    subject=subject,
                    html_template='email/requirement_reassigned.html',
                    context=context
                )

                subject = "Task assign on CodaTraining"
                to = (
                    get_user_model()
                    .objects.get(pk=self.request.POST["assigned_to"])
                    .email
                )
                context = {
                    'request_what': self.request.POST['what'],
                    'url': protocol + self.request.get_host() + reverse('management:RequirementDetail',
                                                                        kwargs={'pk': form.instance.id}),
                    'delivery_date': self.request.POST['delivery_date'],
                    'user': self.request.user,
                }
                send_email(
                    category=self.request.user.category,
                    to_email=[to,],
                    subject=subject,
                    html_template='email/RequirementUpdateView.html',
                    context=context
                )

            return super().form_valid(form)
        else:
            return redirect("management:requirements-active")

    def test_func(self):
        requirement = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == requirement.created_by:
            return True
        return False


class RequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = Requirement
    success_url = "/management/requirements"

    def test_func(self):
        # creator = self.get_object()
        # if self.request.user == creator.username:
        if self.request.user.is_superuser:
            return True
        return False


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

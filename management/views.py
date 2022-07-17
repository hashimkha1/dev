import calendar
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q
from management.utils import email_template
from .forms import (
    DepartmentForm,
    TransactionForm,
    OutflowForm,
    InflowForm,
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
from .models import (
    Transaction,
    Policy,
    Inflow,
    Outflow,
    Tag,
    Task,
    TaskHistory,
    TaskLinks,
    Requirement,
)
from data.models import DSU
from django.contrib.auth import get_user_model
from accounts.models import Tracker,Department
from coda_project import settings

# User=settings.AUTH_USER_MODEL
User = get_user_model()


def home(request):
    return render(
        request, "main/home_templates/management_home.html", {"title": "home"}
    )

def department(request):
    departments=Department.objects.all()
    return render(request, "management/doc_templates/departmentlist.html" , {'departments':departments})

def newdepartment(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:management-department')
    else:
        form=DepartmentForm()
    return render(request, "management/doc_templates/department_form.html", {"form":form})


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
    with open(settings.STATIC_ROOT+'/companyagenda.json','r') as file:
        data = json.load(file)

    return render(request, "management/companyagenda.html", {"title": "Company Agenda","data":data})


def updatelinks_companyagenda(request):
    department = request.POST["department"]
    subdepartment = request.POST["subdepartment"]
    linkname = request.POST["linkname"]
    link_url = request.POST["link_url"]
   
    with open(settings.STATIC_ROOT+'/companyagenda.json', "r") as jsonFile:
        data = json.load(jsonFile)

    if subdepartment == "":
        data[department][linkname] = link_url
    else:
        data[department][subdepartment][linkname] = link_url

    with open(settings.STATIC_ROOT+'/companyagenda.json', "w") as jsonFile:
        json.dump(data, jsonFile)

    return JsonResponse({"success":True})


def finance(request):
    return render(
        request, "management/company_finances/finance.html", {"title": "Finance"}
    )


def hr(request):
    return render(request, "management/company_finances/hr.html", {"title": "HR"})


# ----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------

def transact(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/management/transaction/")
    else:
        form = TransactionForm()
    return render(request, "management/company_finances/transact.html", {"form": form})


class TransactionListView(ListView):
    model = Transaction
    template_name = "management/company_finances/transaction.html"
    context_object_name = "transactions"
    # ordering=['-transaction_date']


@method_decorator(login_required, name="dispatch")
class OutflowDetailView(DetailView):
    template_name = "management/outflow_detail.html"
    model = Transaction
    ordering = ["-transaction_date"]


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    # success_url="/management/transaction"
    fields = [
        "sender",
        "receiver",
        "phone",
        "department",
        "category",
        "type",
        "payment_method",
        "qty",
        "amount",
        "transaction_cost",
        "description",
        "receipt_link",
    ]
    form = TransactionForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("management:transaction-list")


# ----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------


def outflow_entry(request):
    if request.method == "POST":
        form = OutflowForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.employee = request.user
            form.save()
            return redirect("/management/outflows/")
    else:
        form = OutflowForm()
    return render(
        request, "management/company_finances/outflow_entry.html", {"form": form}
    )


def outflowlist(request):
    outflows = Outflow.objects.all().order_by("-activity_date")
    # total_duration=Tracker.objects.all().aggregate(Sum('duration'))
    # total_communication=Rated.objects.all().aggregate(Sum('communication'))
    total = Outflow.objects.all().aggregate(Total_Cashoutflows=Sum("amount"))
    expenses = total.get("Total_Cashoutflows")
    context = {"outflows": outflows, "expenses": expenses}
    return render(request, "management/cash_outflow/outflows.html", context)


@method_decorator(login_required, name="dispatch")
class OutflowDetailView(DetailView):
    template_name = "management/cash_outflow/outflow_detail.html"
    model = Outflow
    ordering = ["-activity_date"]


@method_decorator(login_required, name="dispatch")
class OutflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Outflow
    success_url = "/management/outflows"
    fields = [
        "sender",
        "receiver",
        "phone",
        "department",
        "category",
        "type",
        "payment_method",
        "qty",
        "amount",
        "transaction_cost",
        "description",
    ]

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)

    def test_func(self):
        outflow = self.get_object()
        if self.request.user == outflow.employee:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class OutflowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Outflow
    success_url = "/management/outflows"

    def test_func(self):
        outflow = self.get_object()
        if self.request.user == outflow.employee:
            return True
        return False


# ----------------------CASH INFLOW CLASS-BASED VIEWS--------------------------------
def inflow(request):
    if request.method == "POST":
        form = InflowForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.sender = request.user
            form.save()
            return redirect("/management/inflows/")
    else:
        form = InflowForm()
    return render(
        request, "management/company_finances/inflow_entry.html", {"form": form}
    )

@method_decorator(login_required, name="dispatch")
class InflowDetailView(DetailView):
    template_name = "management/cash_inflow/inflow_detail.html"
    model = Inflow
    ordering = ["-transaction_date"]


def inflows(request):
    inflows = Inflow.objects.all().order_by("-transaction_date")
    # total_duration=Tracker.objects.all().aggregate(Sum('duration'))
    # total_communication=Rated.objects.all().aggregate(Sum('communication'))
    total = Inflow.objects.all().aggregate(Total_Cashinflows=Sum("amount"))
    revenue = total.get("Total_Cashinflows")
    context = {"inflows": inflows, "revenue": revenue}
    return render(request, "management/cash_inflow/inflows.html", context)


@method_decorator(login_required, name="dispatch")
class UserInflowListView(ListView):
    model = Inflow
    template_name = "management/cash_inflow/user_inflow.html"
    context_object_name = "inflows"
    ordering = ["-transaction_date"]


@method_decorator(login_required, name="dispatch")
class InflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Inflow
    success_url = "/management/inflow"
    fields = [
        "sender",
        "receiver",
        "phone",
        "category",
        "task",
        "method",
        "period",
        "qty",
        "amount",
        "transaction_cost",
        "description",
    ]

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def test_func(self):
        inflow = self.get_object()
        if self.request.user == inflow.sender:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class InflowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Inflow
    success_url = "/management/inflow"

    def test_func(self):
        inflow = self.get_object()
        # if self.request.user == inflow.sender:
        if self.request.user.is_superuser:
            return True
        return False


# ----------------------MANAGEMENT POLICIES& OTHER VIEWS--------------------------------
def policy(request):
    if request.method == "POST":
        form = PolicyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management:policies")
    else:
        form = PolicyForm()
    return render(request, "management/hr/policy.html", {"form": form})


def policies(request):
    reporting_date = date.today()
    day_name = date.today().strftime("%A")
    #policies from management app
    policies = Policy.objects.filter(is_active=True).order_by("upload_date")
    context = {
        "policies": policies,
        "reporting_date": reporting_date,
        "day_name": day_name,
    }
    return render(request, "management/hr/policies.html", context)

class PolicyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Policy
    # success_url="/management/transaction"
    fields = ["staff","type","department","description","link"]
    form = PolicyForm()
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("management:policies")
    
    def test_func(self):
        if self.request.is_admin:
            return True
        if self.request.is_superuser:
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
        "group",
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

from datetime import date, timedelta
from django.db.models import Q

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

    history = TaskHistory.objects.filter(Q(activity_name=taskname), Q(created_at__gte=start_day_of_prev_month3) , Q(created_at__lte=last_day_of_prev_month1))

    results = { "target_points":0, "target_amount":0 }
    counter = 0
    for data in history.all():
        results["target_points"] += data.mxpoint
        results["target_amount"] += data.mxearning
        counter = counter+1
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

def filterbycategory(request):
    category = request.POST["category"]
    print("category",category)

    tasks = Task.objects.filter(category__title=category)
    result = []
    details = {}
    for data in tasks.all():
        details["group"] = data.group
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
    return JsonResponse({"result":result},safe =False)

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
    delta = deadline_date - date.today()
    time_remaining = delta.days
    current_user = request.user
    employee = get_object_or_404(User, username=kwargs.get("username"))
    tasks = Task.objects.all().filter(employee=employee)
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

    # 1st month
    last_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month1 = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month1.day)

    last_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month2 = last_day_of_prev_month1.replace(day=1) - timedelta(days=last_day_of_prev_month2.day)

    # 3rd month
    last_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=1)
    start_day_of_prev_month3 = last_day_of_prev_month2.replace(day=1) - timedelta(days=last_day_of_prev_month3.day)

    history = TaskHistory.objects.filter(Q(submission__gte=start_day_of_prev_month3) , Q(submission__lte=last_day_of_prev_month1))

    average_earnings = 0
    counter = 0
    for data in history.all():
        average_earnings += data.get_pay
        counter = counter+1
    try:
        average_earnings = average_earnings / counter
    except Exception as ZeroDivisionError:
        average_earnings = 0.0

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
        "average_earnings":average_earnings
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
    task_history = TaskHistory.objects.get(pk=kwargs.get("pk"))
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
    laptop_saving = 1000
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
        "group",
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
    fields = ["employee", "activity_name", "description", "point"]

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
def newevidence(request,taskid):
    if request.method == "POST":
        form = EvidenceForm(request.POST)
        # Check whether the task exist then only we allow to create evidence
        try:
            Task.objects.get(id=taskid)
        except:
            return render(request, "errors/404.html")

        if form.is_valid():
            points,maxpoints = Task.objects.values_list("point","mxpoint").filter(employee=request.user,id=taskid)[0]
        
            if points != maxpoints:
                Task.objects.filter(employee=request.user,id=taskid).update(point=points+1)

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
    context ={}
    # fetch the object related to passed id
    obj = get_object_or_404(TaskLinks, id = id)
    # pass the object as instance in form
    form = EvidenceForm(request.POST or None, instance = obj)
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
    return render(request, "management/hr/assess_form.html", {"form": form})


class AssessListView(ListView):
    queryset = DSU.objects.filter(type="Staff").order_by("-created_at")
    # queryset=DSU.objects.all()
    template_name = "management/hr/assessment.html"

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
                html_content = f"""
                    <span><h3>Requirement: </h3>{request.POST['what']}<br>
                    <a href='{protocol+request.get_host()+reverse('management:RequirementDetail',
                    kwargs={'pk':form.instance.id})}'>click here</a><br>
                    <b>Dead Line: </b><b style='color:red;'>
                    {request.POST['delivery_date']}</b><br><b>Created by: 
                    {request.user}</b></span>"""
                email_template(subject, to, html_content)
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

    history = TaskHistory.objects.filter(Q(activity_name=taskname), Q(created_at__gte=start_day_of_prev_month3) , Q(created_at__lte=last_day_of_prev_month1))

    results = { "target_points":0, "target_amount":0 }
    counter = 0
    for data in history.all():
        results["target_points"] += data.mxpoint
        results["target_amount"] += data.mxearning
        counter = counter+1
    try:
        results["target_points"] = results["target_points"] / counter
        results["target_amount"] = results["target_amount"] / counter
    except Exception as ZeroDivisionError:
        results["target_points"] = 0.0
        results["target_amount"] = 0.0

    return JsonResponse(results)

def filterbycategory(request):
    category = request.POST["category"]
    print("category",category)

    tasks = Task.objects.filter(category__title=category)
    result = []
    details = {}
    for data in tasks.all():
        details["group"] = data.group
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
    return JsonResponse({"result":result},safe =False)
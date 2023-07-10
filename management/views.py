import calendar,string,requests
from django.contrib import messages
from django import template
from datetime import date, datetime, timedelta
from django.db import transaction
from decimal import Decimal
from django.utils.text import capfirst
from django.db.models import Q,Sum,F
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from mail.custom_email import send_email
from management.forms import (
    DepartmentForm,
    PolicyForm,
    ManagementForm,
    RequirementForm,
    EvidenceForm,
    EmployeeContractForm,
    MonthForm,
    MeetingForm
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from application.models import UserProfile
from management.models import (
    Advertisement,
    Policy,
    TaskCategory,
    Task,
    TaskHistory,
    TaskLinks,
    Requirement,
    Training,
    ProcessJustification,
    ProcessBreakdown,
    Meetings
)
from data.models import DSU
from finance.models import Default_Payment_Fees, LoanUsers,LBandLS, TrainingLoan,PayslipConfig
from accounts.models import Tracker, Department, TaskGroups
from main.filters import RequirementFilter,TaskHistoryFilter,TaskFilter
from django.conf import settings
from django.contrib.auth import get_user_model

from coda_project import settings

from management.utils import (email_template,text_num_split,
                               paytime,payinitial,paymentconfigurations,
                               deductions,loan_computation,emp_average_earnings,
                               bonus,additional_earnings,best_employee,updateloantable,
                               addloantable,employee_reward,split_num_str,employee_group_level,lap_save_bonus
                        )
from main.utils import countdown_in_month,path_values
    

import logging
logger = logging.getLogger(__name__)

# User=settings.AUTH_USER_MODEL
User = get_user_model()
register = template.Library()


def home(request):
    return redirect('main:layout')
    # return render(
        # request, "main/home_templates/management_home.html", {"title": "home"}
        # request, "management/doc_templates/contract.html", {"title": "home"}
    # )

def dckdashboard(request):
    # departments = Department.objects.filter(is_active=True)
    # return render(request, "management/departments/agenda/dck_dashboard.html", {'title': "DCK DASHBOARD"})
    return render(request, "management/departments/agenda/user_dashboard.html", {'title': "DCK DASHBOARD"})

# ================================ DEPARTMENT SECTION ================================
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

def meetings(request):
    # sessions=Meetings.objects.all().order_by("created_at")
    sessions = Meetings.objects.filter(is_active=True).order_by("created_at")
    categories_list = Meetings.objects.values_list('category__title', flat=True).distinct()
    meeting_categories=sorted(categories_list)
    context={
        "meeting_categories":meeting_categories,
        "sessions":sessions

    }
    return render(request, "management/departments/hr/meetings.html",context)

def newmeeting(request):
    if request.method == "POST":
        form = MeetingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:meetings')
    else:
        form = MeetingForm()
        return render(request, "main/snippets_templates/generalform.html",{"form": form})


class MeetingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meetings
    success_url = "/management/meetings"
    fields = "__all__"
    form = MeetingForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return True
        return False

def contract(request):
    return render(request, "management/contracts/trainingcontract_form.html")

def employee_contract(request):
    submitted = False
    if request.user.is_employee_contract_signed:
        return (redirect('accounts:account-profile'))
    else:
        context = {}
        form = None
        try:
            profile = UserProfile.objects.get(user=request.user)
        except:
            profile = None

        # print(profile)
        if request.method == 'POST':
            if profile:
                profile.national_id_no = request.POST['national_id_no']
                profile.id_file = request.POST['id_file']
                profile.emergency_name = request.POST['emergency_name']
                profile.emergency_address = request.POST['emergency_address']
                profile.emergency_citizenship = request.POST['emergency_citizenship']
                profile.emergency_phone = request.POST['emergency_phone']
                profile.emergency_email = request.POST['emergency_email']
                profile.emergency_national_id_no = request.POST['emergency_national_id_no']
                profile.save()
                submitted = True

        form = EmployeeContractForm()
        context['user'] = request.user
        context['profile'] = profile
        context['form'] = form

        if submitted:
            return redirect("management:employee_contract")
        else:
            return render(request, "management/contracts/employee_contract.html", {'context': context})
            # return render(request, "main/snippets_templates/modify.html", {'context': context})

def read_employee_contract(request):
    (today,year,deadline_date,month,last_month,day,
     target_date,time_remaining_days,time_remaining_hours,
     time_remaining_minutes,payday,*_)=paytime()
    user = UserProfile.objects.get(user=request.user)
    context={
        "title":"Employee Contract",
        "today":today,
        "deadline_date":deadline_date
    }
    # if user.national_id_no:
    return render(request, "management/contracts/read_employee_contract.html",context)



def confirm_employee_contract(request):
    user = UserProfile.objects.get(user=request.user)

    # if user.national_id_no:
    user = request.user
    user.is_employee_contract_signed = True
    user.save()

    try:
        group = TaskGroups.objects.all().first()
        cat = TaskCategory.objects.all().first()
        try:
            max_point = Task.objects.filter(groupname=group, category=cat).first()
            max_point = max_point.mxpoint
        except:
            max_point = 0

        create_task('Group A', group, cat, user, 'General Meeting', 'General Meeting description, auto added', '0', '0', max_point, '0')
        create_task('Group A', group, cat, user, 'BI Session', 'BI Session description, auto added', '0', '0', max_point, '0')
        create_task('Group A', group, cat, user, 'One on One', 'One on One description, auto added', '0', '0', max_point, '0')
        create_task('Group A', group, cat, user, 'Video Editing', 'Video Editing description, auto added', '0', '0', max_point, '0')
        create_task('Group A', group, cat, user, 'Dev Recruitment', 'Dev Recruitment description, auto added', '0', '0', max_point, '0')
        create_task('Group A', group, cat, user, 'Sprint', 'Sprint description, auto added', '0', '0', max_point, '0')
    except:
        print("Something wrong in task creation")

    return(redirect('accounts:account-profile'))
    # else:
    #     return redirect("management:employee_contract")


def create_task(group, groupname, cat, user, activity, description, duration, point, mxpoint, mxearning):
    x = Task()
    x.group = group
    x.groupname = groupname
    x.category = cat
    x.employee = user
    x.activity_name = activity
    x.description = description
    x.duration = duration
    x.point = point
    x.mxpoint = mxpoint
    x.mxearning = mxearning
    x.save()

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

@login_required
def companyagenda(request):
    request.session["siteurl"] = settings.SITEURL
    with open(settings.STATIC_ROOT + '/companyagenda.json', 'r') as file:
        data = json.load(file)
    if request.user.is_superuser or (request.user.is_staff):
        return render(request, "management/departments/agenda/general_agenda.html", {"title": "Company Agenda", "data": data})
    else:
        return render(request, "management/departments/agenda/users_dashboard.html", {"title": "Client dashboard"})


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

# ======================TaskCategory=======================
class TaskCategoryCreateView(LoginRequiredMixin, CreateView):
    model = TaskCategory
    success_url = "/management/newtask"
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskGroupCreateView(LoginRequiredMixin, CreateView):
    model = TaskGroups
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
            historytasks = TaskHistory.objects.filter(employee__is_staff=True, employee__is_active=True,
                                                      employee_id=emp)
            group=employee_group_level(historytasks,TaskGroups)                                        
         
            for act in activitys:
                #check if activity exist
                count=Task.objects.filter(category_id=category, activity_name=act).count()
                if count > 0:
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
        task_categories = TaskCategory.objects.all()
        group = TaskGroups.objects.all()
        employess = User.objects.filter(Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True)).all()

    return render(request, "management/tasknew_form.html", {"group": group, "category": task_categories, "employess": employess})


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
    # print("+++++++++getaveragetargets+++++++++")
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

    # print(result)
    return JsonResponse({"result": result}, safe=False)


class TaskHistoryView(ListView):
    pass
#     queryset = TaskHistory.objects.all()
#     myfilter=TaskHistoryFilter(request.GET,queryset=queryset)
#     template_name = "management/daf/taskhistory.html"


def historytasks(request):
    historytask=TaskHistory.objects.filter(employee__is_staff=True,employee__is_active=True)
    # historytasks=TaskHistory.objects.all().order_by('-submission')
    myfilter=TaskHistoryFilter(request.GET,queryset=historytask)
    context={
        "historytasks":historytask,
        "TaskHistoryFilter":myfilter
    }
    return render(request,"management/daf/taskhistory.html", context)


def task_payslip(request, employee=None, *args, **kwargs):
    date = datetime.now()
    selected_month = date.month
    selected_year = date.year

    if selected_month == 1:
        selected_month = 12
        selected_year -= selected_year
    else:
        selected_month -= 1

    if request.method == "POST":
        form = MonthForm(request.POST)
        if form.is_valid():
            selected_month = int(form.cleaned_data['month'])
            selected_year = int(form.cleaned_data['year'])
    else:
        form = MonthForm()

    # task_history = TaskHistory.objects.get(pk=kwargs.get("pk"))
    today,year, deadline_date,month,last_month,*_=paytime()
    employee = get_object_or_404(User, username=kwargs.get("username"))
    sessions = Training.objects.all().filter(presenter=employee).order_by('-created_date')
    num_sessions = sessions.count()
    userprofile = UserProfile.objects.get(user_id=employee)
    tasks = Task.objects.all().filter(employee=employee)
    LBLS=LBandLS.objects.filter(user=employee)
    user_data=TrainingLoan.objects.filter(user=employee, is_active=True)
    # task_history = TaskHistory.objects.get_by_employee(employee)
    task_history = TaskHistory.objects.all().filter(employee=employee)
    # print(f'OBJECT:{task_history}')
    if task_history is None:
        message=f'Hi {request.user}, you do not have history information,kindly contact admin!'
        return render(request, "main/errors/404.html",{"message":message})
    payslip_config=paymentconfigurations(PayslipConfig,employee)

    tasks =TaskHistory.objects.filter(employee=employee,submission__month=selected_month,submission__year=selected_year)
    (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance)=payinitial(tasks)
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay

    # Deductions & Bonus
    laptop_bonus,laptop_saving=lap_save_bonus(userprofile,payslip_config)
    total_deduction,sub_bonus= additional_earnings(user_data,tasks,total_pay,payslip_config)
    food_accomodation,computer_maintenance,health,kra,lap_saving,loan_payment,total_deductions=deductions(user_data,payslip_config,total_pay)
    loan = Decimal(total_pay) * Decimal("0.2")

    # Deductions & Bonus
    laptop_bonus, laptop_saving = lap_save_bonus(userprofile, payslip_config)
    total_deduction, sub_bonus = additional_earnings(user_data, tasks, total_pay, payslip_config)
    food_accomodation, computer_maintenance, health, kra, lap_saving, loan_payment, total_deductions = deductions(
        user_data, payslip_config, total_pay)
    loan = Decimal(total_pay) * Decimal("0.2")

    # Net Pay
    total_bonus = sub_bonus + laptop_bonus
    total_value=total_pay + total_bonus
    try:
        net = total_value - total_deduction
    except (TypeError, AttributeError):
        net = total_pay
    bonus_points_ammount, latenight_Bonus,yearly,offpay,EOM,EOQ,EOY,sub_bonus=bonus(tasks,total_pay,payslip_config)
    net = total_value - total_deduction

    # Total LS
    tasks = TaskHistory.objects.filter(employee=employee, submission__month__lte=selected_month)
    month_set = set()

    for task in tasks:
        month_set.add(str(task.submission.month) + str(task.submission.year))

    total_lap_saving = len(month_set) * lap_saving
    if total_lap_saving >= 20000:
        total_lap_saving = 20000
        lap_saving = 0


    # Retirement Yearly Package
    tasks = TaskHistory.objects.filter(employee=employee, submission__month__lte=selected_month, submission__year=selected_year)
    month_year = {}
    for task in tasks:
        month_year[str(task.submission.month) + str(task.submission.year)] = {'month': str(task.submission.month), 'year': str(task.submission.year)}

    this_year_point = 0
    for month_year_obj in month_year.values():
        _tasks = TaskHistory.objects.filter(employee=employee, submission__month=month_year_obj['month'], submission__year=month_year_obj['year'])
        _total_pay = 0
        for task in tasks:
            _total_pay = total_pay + task.get_pay

        _bonus_points_ammount, _latenight_Bonus, _yearly, _offpay, _EOM, _EOQ, _EOY, _sub_bonus = bonus(_tasks, _total_pay, payslip_config)

        this_year_point += (_bonus_points_ammount + num_sessions)

    context = {
        "selected_month":selected_month,
        "selected_year":selected_year,
        "form": form,
        # deductions
        "laptop_saving": lap_saving,
        "total_laptop_saving": total_lap_saving,
        "computer_maintenance": computer_maintenance,
        "food_accomodation": food_accomodation,
        "health": health,
        "loan": loan,
        "kra": kra,
        "total_deduction": total_deduction,
        # bonus
        "latenight_Bonus": latenight_Bonus,
        "EOM": EOM,
        # "pointsearning": bonus_points_ammount,
        "pointsearning": bonus_points_ammount + num_sessions,
        "holidaypay": offpay,
        "yearly": 12000 + this_year_point,
        # General
        "tasks": tasks,
        "deadline_date": deadline_date,
        "today": today,
        "total_pay": total_pay,
        "total_value": total_value,
        "net": net,
        "employee": employee,
    }

    if request.user == employee or request.user.is_superuser:
        # return render(request, 'management/daf/paystub.html', context)
        return render(request, "management/daf/payslip.html", context)
    elif request.user.is_superuser:
        # return render(request, 'management/daf/paystub.html', context)
        return render(request, "management/daf/payslip.html", context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")


def usertask(request, user=None, *args, **kwargs):
    request.session["siteurl"] = settings.SITEURL
    employee = get_object_or_404(User, username=kwargs.get("username"))
    userprofile = UserProfile.objects.get(user_id=employee)
    LBLS=LBandLS.objects.filter(user=employee)
    user_data=TrainingLoan.objects.filter(user=employee, is_active=True)
    tasks = Task.objects.all().filter(employee=employee)
    (
                remaining_days,
                remaining_seconds ,
                remaining_minutes ,
                remaining_hours 
    )=countdown_in_month()

    # -----------Time from utils------------------
    deadline_date=paytime()[2]
    payday=paytime()[10]

     # -----------Points/Earnings from utils------------------
    (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance)=payinitial(tasks)
    points_count = Task.objects.filter(
        description__in=['Meetings', 'General', 'Sprint', 'DAF', 'Recruitment', 'Job Support', 'BI Support'],
        employee=employee)
    point_check = points_count.aggregate(Your_Total_Points=Sum("point"))
    num_tasks = tasks.count()
    earning = tasks.aggregate(Your_Total_Pay=Sum("mxearning"))
    mxearning = tasks.aggregate(Your_Total_AssignedAmt=Sum("mxearning"))
    point_percentage=employee_reward(tasks)
    # print("MY % IS :", point_percentage)
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
    payslip_config=paymentconfigurations(PayslipConfig,employee)
    total_deduction,sub_bonus= additional_earnings(user_data,tasks,total_pay,payslip_config)
    message=f'VALES ARE :{total_deduction},{sub_bonus}'
    # print(message)
    try:
        net = total_pay - total_deduction
    except (TypeError, AttributeError):
        net = 0.00
    # average_earnings=emp_average_earnings(request,TaskHistory,GoalAmount)
    average_earnings=GoalAmount

    activities = ["one one one", "one one one session", "one one one sessions"]
    activitiesmodified = [activity.lower().translate({ord(c): None for c in string.whitespace}) for activity in
                          activities]
    # print(activitiesmodified)
    deadline_date_modify = deadline_date.strftime("%Y/%m/%d")
    context = {
        'activitiesmodified': activitiesmodified,
        "payday": payday,
        "num_tasks": num_tasks,
        "tasks": tasks,
        "Points": points,
        "MaxPoints": mxpoints,
        "point_percentage": point_percentage,
        "pay": pay,
        "GoalAmount": GoalAmount,
        "paybalance": paybalance,
        "pointsbalance": pointsbalance,
        "total_pay": total_pay,
        "loan": loan,
        "net": net,
        "point_check": point_check,
        "average_earnings": average_earnings,
        "enddate": deadline_date_modify,
        "remaining_days":remaining_days,
        "remaining_seconds ":remaining_seconds ,
        "remaining_minutes ":remaining_minutes ,
        "remaining_hours":remaining_hours,
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


def usertaskhistory(request, user=None,  *args, **kwargs):
    date = datetime.now()
    month = date.month
    year = date.year

    if month == 1:
        month = 12
        year -= year
    else:
        month -= 1

    if request.method == "POST":
        form = MonthForm(request.POST)
        if form.is_valid():
            month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])
    else:
        form = MonthForm()

    employee = get_object_or_404(User, username=kwargs.get("username"))
    user_data=TrainingLoan.objects.filter(user=employee, is_active=True)
    userprofile = UserProfile.objects.get(user_id=employee)
    LBLS=LBandLS.objects.filter(user=employee)
    tasks =TaskHistory.objects.filter(employee=employee, submission__month=str(month+1), submission__year=str(year))
    if tasks is None:
        message=f'Hi {request.user}, you do not have history information for last month,kindly contact admin!'
        return render(request, "main/errors/404.html",{"message":message})
    # ------------POINTS AND EARNINGS--------------------
    point_percentage=employee_reward(tasks)
    (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance)=payinitial(tasks)
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay
    try:
        paybalance = Decimal(GoalAmount) - Decimal(total_pay)
    except (TypeError, AttributeError):
        paybalance = 0
    payslip_config=paymentconfigurations(PayslipConfig,employee)
    loan_amount,loan_payment,balance_amount=loan_computation(total_pay,user_data,payslip_config)
    total_deduction,sub_bonus= additional_earnings(user_data,tasks,total_pay,payslip_config)
    *_,loan_payment,total_deductions=deductions(user_data,payslip_config,total_pay)
    loan=loan_payment
    point_percentage=point_percentage
    try:
        net = total_pay - total_deduction+sub_bonus
    except (TypeError, AttributeError):
        net = 0.00
    # ==================PRINT=================
    context = {
        'form': form,
        'employee':employee,
        "tasksummary": tasksummary,
        "num_tasks": num_tasks,
        "tasks": tasks,
        "points": points,
        "mxpoints": mxpoints,
        "point_percentage": point_percentage,
        "pay": pay,
        "GoalAmount": GoalAmount,
        "paybalance": paybalance,
        "pointsbalance": pointsbalance,
        "total_pay": total_pay,
        "loan": loan,
        "net": net,
    }
    # setting  up session
    request.session["employee_name"] = kwargs.get("username")

    if request.user == employee or request.user.is_superuser:
        return render(request, "management/daf/usertaskhistory.html", context)
    elif request.user.is_superuser:
        return render(request, "management/daf/usertaskhistory.html", context)
    else:
        message=f'Hi {request.user}, You are Prohibited from accessing this Page!'
        return render(request, "main/errors/403.html",{"message":message})


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
    payslip_config=paymentconfigurations(PayslipConfig,employee)
    #  ===========Time==============
    today,year,deadline_date,*_=paytime()
    #  ===========Points and Pay==============
    (num_tasks,points,mxpoints,pay,GoalAmount,pointsbalance)=payinitial(tasks)
    task_obj=Task.objects.filter(submission__contains=year)
    total_pay = Decimal(0)
    for task in tasks:
        total_pay = total_pay + task.get_pay
    # Deductions
    loan_amount, loan_payment, balance_amount = loan_computation(total_pay, user_data, payslip_config)
    logger.debug(f'balance_amount: {balance_amount}')
    # loan_update_save(loantable,user_data,employee,total_pay,payslip_config)
    # total_deduction,sub_bonus,sub_total= additional_earnings(user_data,tasks,total_pay,payslip_config,userprofile,LBLS)
    food_accomodation,computer_maintenance,health,kra,lap_saving,loan_payment,total_deductions=deductions(user_data,payslip_config,total_pay)
    userprofile = UserProfile.objects.get(user_id=employee)
    laptop_bonus,laptop_saving=lap_save_bonus(userprofile,payslip_config)
    # ====================Bonus Section=============================
    bonus_points_ammount,latenight_Bonus,yearly,offpay,EOM,EOQ,EOY,sub_bonus=bonus(tasks,total_pay,payslip_config)

    # ====================Summary Section=============================
    total_deduction,sub_bonus= additional_earnings(user_data,tasks,total_pay,payslip_config)
    total_bonus = sub_bonus + laptop_bonus
    # Net Pay
    total_value=total_pay + total_bonus
    # print(loan_amount, loan_payment, balance_amount)
    # print("laptop_bonus===>",laptop_bonus,"laptop_saving====>",laptop_saving)
    # print('======================================')
    # print('total_bonus=======>',total_bonus)
    # print('total_deduction=======>',total_deduction)
    # print('total_pay=======>',total_pay)
    # print('total_value=====>',total_value)
    net = total_value - total_deduction
    # print('======================================')
    round_off = round(net) - net
    net_pay = net + round_off
    logger.debug(f'total deductions: {total_deduction}')
    logger.debug(f'total_bonus: {total_bonus}')
    logger.debug(f'net: {net}')
    logger.debug(f'net_pay: {net_pay}')
    # print(f'total deductions: {total_deduction}')
    # print(f'total_bonus: {total_bonus}')
    # print(f'net: {net}')
    # print(f'net_pay: {net_pay}')
    context = {
        # bonus
        # "pointsearning": bonus_points_ammount,
        "pointsearning": bonus_points_ammount,
        "EOM": EOM,
        "EOQ": EOQ,
        "EOY": EOY,
        "laptop_bonus": laptop_bonus,
        "holidaypay": offpay,
        "Night_Bonus": latenight_Bonus,
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
    template_name='main/snippets_templates/generalform.html'
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
    template_name='main/snippets_templates/generalform.html'
    
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


JOB_SUPPORTS = ["job support", "job_support", "jobsupport"]
ACTIVITY_LIST = ['BOG', 'BI Sessions', 'DAF Sessions', 'Project', 'web sessions']

def newevidence(request, taskid):
    task = get_object_or_404(Task, id=taskid)

    if request.method == "POST":
        form = EvidenceForm(request.POST)
        if form.is_valid():
            points, maxpoints = Task.objects.values_list("point", "mxpoint").get(id=taskid)
            
            if points != maxpoints and task.activity_name.lower() not in JOB_SUPPORTS:
                Task.objects.filter(id=taskid).update(point=points + 1)

            data = form.cleaned_data
            link = data['link']
            
            if not link:
                messages.error(request, "Please provide evidence link")
                return render(request, "management/daf/evidence_form.html", {"form": form})
            
            try:
                a = requests.get(link)
                if a.status_code == 200:
                    check = TaskLinks.objects.filter(link=link)
                    
                    if check.exists():
                        users = check.values_list('added_by__username', flat=True)
                        
                        if request.user.username in users:
                            messages.error(request, "You have already uploaded this link")
                            return render(request, "management/daf/evidence_form.html", {"form": form})
                        
                        if task.activity_name in ACTIVITY_LIST:
                            form.save()
                            return redirect("management:evidence")
                        else:
                            messages.error(request, "This link is already uploaded")
                            return render(request, "management/daf/evidence_form.html", {"form": form})
                        
                    form.save()
                    return redirect("management:evidence")
                else:
                    messages.error(request, "Link is not valid, please check again")
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

    # Calculate the date range for the last 2 months
    now = timezone.localtime()
    print(now)
    two_months_ago = now - timezone.timedelta(days=60)

    # Filter the TaskLinks based on the created_at field within the date range
    userlinks = TaskLinks.objects.filter(added_by=employee, created_at__range=[two_months_ago, now]).order_by("-created_at")
    return render(request, "management/daf/userevidence.html", {"userlinks": userlinks})

# def userevidence(request, user=None, *args, **kwargs):
#     # current_user = request.user
#     employee = get_object_or_404(User, username=kwargs.get("username"))
#     userlinks = TaskLinks.objects.all().filter(added_by=employee).order_by("-created_at")
#     return render(request, "management/daf/userevidence.html", {"userlinks": userlinks})

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


# =============================EMPLOYEE SESSIONS========================================
class SessionCreateView(LoginRequiredMixin, CreateView):
    model=Training
    success_url = "/management/sessions"
    # fields= "__all__"
    fields = ["department","category","subcategory","topic","level","session","session_link","expiration_date","description","is_active","featured"]

    def form_valid(self, form):
        form.instance.presenter = self.request.user
        return super().form_valid(form)

def sessions(request):
    # total_sessions=Training.objects.all().count()
    sessions=Training.objects.all()
    client_sessions=Training.objects.filter(presenter__is_client=True,presenter__is_active=True).order_by("-created_date")
    employee_sessions=Training.objects.filter(presenter__is_staff=True).order_by("-created_date")
    # myfilter=TaskHistoryFilter(request.GET,queryset=historytasks)
    context_a={
       "object_list":client_sessions,
        "title":"Client_Sessions"
    }
    context_b={
        "object_list":employee_sessions,
        "title":"Employee_Sessions"
    }
    if request.user.is_client :
        return render(request,"management/departments/hr/sessions.html", context_a)
    elif request.user.is_staff :
        return render(request,"management/departments/hr/sessions.html", context_b)
    else:
        return render(request,"management/departments/hr/sessions.html", {"object_list":sessions})


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

def usersession(request, user=None, *args, **kwargs):
    request.session["siteurl"] = settings.SITEURL
    deadline_date=paytime()[2]
    # print(f'Write Value:{deadline_date}')
    employee = get_object_or_404(User, username=kwargs.get("username"))
    sessions = Training.objects.all().filter(presenter=employee).order_by('-created_date')
    emp_target_sessions =75
    client_target_sessions =27
    num_sessions = sessions.count()
    # points = sessions.aggregate(Your_Total_Points=Sum("point"))
    # Points = points.get("Your_Total_Points")
    bal_session = emp_target_sessions - num_sessions
    client_bal_session = client_target_sessions - num_sessions
    context = {
        "sessions":sessions,
        'emp_target_sessions': emp_target_sessions,
        'client_target_sessions': client_target_sessions,
        'client_bal_session': client_bal_session,
        "num_sessions": num_sessions,
        "bal_session": bal_session,
        "deadline_date": deadline_date,
    }
    # setting  up session
    request.session["employee_name"] = kwargs.get("username")

    if request.user.is_superuser or request.user.is_staff:
        return render(request, "management/departments/hr/usersessions.html", context)
    elif request.user.is_superuser:
        return render(request, "management/departments/hr/sessions.html", context)
    elif request.user.is_superuser or request.user.is_client:
        return render(request, "management/departments/hr/clientsessions.html", context)
    else:
        return redirect("main:layout")


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
    path_list,subtitle,pre_sub_title=path_values(request)
    if subtitle == 'dyc_requirements':
        requirements = Requirement.objects.filter(requestor__iexact='client', company__iexact='dyc').order_by('-id')
    elif subtitle == 'client_requirements':
        requirements = Requirement.objects.exclude(company__iexact='dyc').filter(requestor__iexact='client').order_by('-id')
    elif subtitle == 'coda_requirements':
        requirements = Requirement.objects.filter(requestor__iexact='management', company__iexact='coda').order_by('-id')
    elif subtitle == 'reviewed':
        requirements = Requirement.objects.filter(is_reviewed=True).order_by('-id')
    else:
        requirements = Requirement.objects.all().order_by("-id")

    requirement_filters=RequirementFilter(request.GET,queryset=requirements)

    context={
        "requirements": requirements,
        "requirement_filters": requirement_filters
    }
    return render(request,"management/doc_templates/requirements.html",context)


def newrequirement(request):
    request.session["siteurl"] = settings.SITEURL
    if request.method == "POST":
        form = RequirementForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.creator=request.user
            # print(instance.creator)
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
                context = {
                    'request_what': request.POST['what'],
                    'url': protocol + request.get_host() + reverse('management:RequirementDetail',
                                                                   kwargs={'pk': form.instance.id}),
                    'delivery_date': request.POST['delivery_date'],
                    'user': request.user,
                }
                send_email(category=request.user.category,
                to_email=[request.user.email,],
                subject=subject,
                html_template='email/newrequirement.html', 
                context=context)
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
                "why","how","comments","doc","pptlink","videolink","is_active","is_tested","is_reviewed"
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

class RequirementDeleteView(LoginRequiredMixin, DeleteView):
    model = Requirement
    success_url = "/management/requirements"

    def test_func(self):
        # creator = self.get_object()
        # if self.request.user == creator.username:
        if self.request.user.is_superuser:
            return True
        return False


def videolink(request,detail_id):
    task_links=TaskLinks.objects.all()
    mylist=[link.lowerlinkname for link in task_links]
    new_list=[val for val in mylist if val !=None]
    mylinkname="requirement"+str(detail_id)
    if mylinkname in new_list:
        obj=TaskLinks.objects.filter(link_name__icontains=str(detail_id))
        # print("obj",obj)
        for link in obj:
            site=link.link
            # print(site)
    else:
        context = {
             "title":'Requirement Elaboration',
             "message":f'There is no video for this requirement'
            } 
        return render(request, "main/messages/general.html",context)
    context = {
      "title":'Requirement Elaboration',
      "site":site,
      "message":f'Access the explanation for this requirement'
    } 
    return render(request, "main/messages/general.html",context)


def getaveragetargets(request):
    # print("+++++++++getaveragetargets+++++++++")
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
    # print("category", category)

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
    template_name = "main/snippets_templates/generalform.html"
    fields = "__all__"
    success_url = "/management/advertisement"
    page_title = 'Advertisement Details'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = capfirst(self.page_title)
        return context


class AdsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advertisement
    template_name = "main/snippets_templates/generalform.html"
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
    

# ====================ESTIMATEVIEWS===============================

def justification(request, *args, **kwargs):
    justifications = ProcessJustification.objects.filter(requirements_id=kwargs.get('pk'))\
        .values("id", "justification", breakdown=F("Process_in_breakdown__breakdown"),
                time=F("Process_in_breakdown__time"), requirement_id=F("requirements__id"),
                Qty=F("Process_in_breakdown__Quantity"), total=F("Process_in_breakdown__total"))
    if justifications:
        justofication_dict = {}
        justifications_ids = ProcessJustification.objects.filter(requirements_id=kwargs.get('pk')) \
            .values_list("id", flat=True)
        obj = ProcessBreakdown.objects.filter(process__id__in=justifications_ids)
        total_time = obj.aggregate(Sum('total'))
        total_qty = obj.aggregate(Sum('Quantity'))
        for justification in justifications:
            if justification.get('breakdown') == 'testing' or justification.get('breakdown') == 'creation':
                justofication_dict.update({justification.get('justification'): justification.get('justification'),
                                           justification.get('justification') + justification.get('breakdown'):
                                               justification.get('breakdown'),
                                           justification.get('breakdown') + 'time': justification.get('time'),
                                           justification.get('justification') + justification.get('breakdown') +
                                           'quantity': justification.get('Qty'),
                                           justification.get('justification') + justification.get('breakdown') +
                                           'total': justification.get('total'),
                                           'requirement_id': justification.get('requirement_id'),
                                           })
            else:
                justofication_dict.update({justification.get('justification'): justification.get('justification'),
                                           justification.get('justification')+justification.get('breakdown'):
                                               justification.get('breakdown'),
                                           justification.get('breakdown')+'time': justification.get('time'),
                                           justification.get('breakdown')+'quantity': justification.get('Qty'),
                                           justification.get('breakdown')+'total': justification.get('total'),
                                           'requirement_id': justification.get('requirement_id'),
                                           })
        return render(request, "management/doc_templates/req_justifications.html", {"justifications": justofication_dict,
                                                                   "total_time": total_time.get('total__sum'),
                                                                    "total_qty": total_qty.get('Quantity__sum')
        })
    return render(request, "management/doc_templates/req_justifications.html", {"active_requirement": kwargs.get('pk')})

def add_requirement_justification(request):
    requirement_id = request.POST.get('requirement_id')

    requirement_obj = Requirement.objects.filter(id=requirement_id).first()
    # print("requirement_obj:==>",requirement_obj)
    if not requirement_obj:
        messages.warning(
            request, "requirement id is wrong"
        )
        context={
            "message":request.path_info
        }
        # return  HttpResponseRedirect(request.path_info)
        return render (request, "main/messages/general.html",context) 
        
    with transaction.atomic():
        table = request.POST.get('Table')
        if table:
            justification_obj = None
            obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="table")
            if obj:
                justification_obj = obj.first()
            else:
                justification_obj = ProcessJustification.objects.create(requirements=requirement_obj, justification="table")
            dictionary = request.POST.get('Dictionary')
            if dictionary:
                time = int(request.POST.get('dictionary_time'))
                qty = int(request.POST.get('dictionary_quantity'))
                obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="dictionary")
                if obj:
                    dictionary_obj = obj.first()
                    dictionary_obj.Quantity = qty
                    dictionary_obj.total = time*qty
                    dictionary_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=justification_obj, breakdown="dictionary", time=time,
                                                    Quantity=qty, total=time*qty)
            erd = request.POST.get('Erd')
            if erd:
                time = int(request.POST.get('Erd_time'))
                qty = int(request.POST.get('Erd_quantity'))
                obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="erd")
                if obj:
                    erd_obj = obj.first()
                    erd_obj.Quantity = qty
                    erd_obj.total = time * qty
                    erd_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=justification_obj, breakdown="erd", time=time, Quantity=qty,
                                                    total=time*qty)
            table_model = request.POST.get('Table_model')
            if table_model:
                time = int(request.POST.get('Table_time'))
                qty = int(request.POST.get('Table_quantity'))
                obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="table_model")
                if obj:
                    table_model_obj = obj.first()
                    table_model_obj.Quantity = qty
                    table_model_obj.total = time * qty
                    table_model_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=justification_obj, breakdown="table_model", time=time,
                                                    Quantity=qty, total=time*qty)
            testing = request.POST.get('Testing')
            if testing:
                time = int(request.POST.get('Testing_time'))
                qty = int(request.POST.get('Testing_quantity'))
                obj = ProcessBreakdown.objects.filter(process=justification_obj, breakdown="testing")
                if obj:
                    testing_obj = obj.first()
                    testing_obj.Quantity = qty
                    testing_obj.total = time * qty
                    testing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=justification_obj, breakdown="testing", time=time,
                                                    Quantity=qty, total=time*qty)
        view_obj = request.POST.get('view')
        if view_obj:
            view_instance = None
            obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="view")
            if obj:
                view_instance = obj.first()
            else:
                view_instance = ProcessJustification.objects.create(requirements=requirement_obj, justification="view")
            flow_diagram = request.POST.get('flow_diagram')
            if flow_diagram:
                time = int(request.POST.get('flow_diagram_time'))
                qty = int(request.POST.get('flow_diagram_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="flow_diagram")
                if obj:
                    flow_diagram_obj = obj.first()
                    flow_diagram_obj.Quantity = qty
                    flow_diagram_obj.total = time * qty
                    flow_diagram_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="flow_diagram", time=time,
                                                    Quantity=qty, total=time*qty)
            create = request.POST.get('view_create')
            if create:
                time = int(request.POST.get('create_time'))
                qty = int(request.POST.get('create_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="create")
                if obj:
                    create_obj = obj.first()
                    create_obj.Quantity = qty
                    create_obj.total = time * qty
                    create_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="create", time=time,
                                                    Quantity=qty, total=time*qty)
            detail = request.POST.get('detail')
            if detail:
                time = int(request.POST.get('detail_time'))
                qty = int(request.POST.get('detail_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="detail")
                if obj:
                    testing_obj = obj.first()
                    testing_obj.Quantity = qty
                    testing_obj.total = time * qty
                    testing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="detail", time=time,
                                                Quantity=qty, total=time*qty)
            list_obj = request.POST.get('list')
            if list_obj:
                time = int(request.POST.get('list_time'))
                qty = int(request.POST.get('list_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="list")
                if obj:
                    list_obj = obj.first()
                    list_obj.Quantity = qty
                    list_obj.total = time * qty
                    list_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="list", time=time,
                                                    Quantity=qty, total=time*qty)
            update_obj = request.POST.get('update')
            if update_obj:
                time = int(request.POST.get('update_time'))
                qty = int(request.POST.get('update_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="update")
                if obj:
                    update_obj = obj.first()
                    update_obj.Quantity = qty
                    update_obj.total = time * qty
                    update_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="update", time=time,
                                                    Quantity=qty, total=time*qty)
            delete_obj = request.POST.get('delete')
            if delete_obj:
                time = int(request.POST.get('delete_time'))
                qty = int(request.POST.get('delete_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="delete")
                if obj:
                    delete_obj = obj.first()
                    delete_obj.Quantity = qty
                    delete_obj.total = time * qty
                    delete_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="delete", time=time,
                                                    Quantity=qty, total=time*qty)
            testing_view = request.POST.get('testing_view')
            if testing_view:
                time = int(request.POST.get('testing_view_time'))
                qty = int(request.POST.get('testing_view_quantity'))
                obj = ProcessBreakdown.objects.filter(process=view_instance, breakdown="testing")
                if obj:
                    testing_obj = obj.first()
                    testing_obj.Quantity = qty
                    testing_obj.total = time * qty
                    testing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=view_instance, breakdown="testing", time=time,
                                                    Quantity=qty, total=time*qty)

        template_obj = request.POST.get('template')
        if template_obj:
            template_instance = None
            obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="template")
            if obj:
                template_instance = obj.first()
            else:
                template_instance = ProcessJustification.objects.create(requirements=requirement_obj,
                                                                        justification="template")
            template_creation = request.POST.get('template_creation')
            if template_creation:
                time = int(request.POST.get('template_creation_time'))
                qty = int(request.POST.get('template_creation_quantity'))
                obj = ProcessBreakdown.objects.filter(process=template_instance, breakdown="creation")
                if obj:
                    creation_obj = obj.first()
                    creation_obj.Quantity = qty
                    creation_obj.total = time * qty
                    creation_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=template_instance, breakdown="creation", time=time,
                                                    Quantity=qty, total=time*qty)
            template_testing = request.POST.get('template_testing')
            if template_testing:
                time = int(request.POST.get('template_testing_time'))
                qty = int(request.POST.get('template_testing_quantity'))
                obj = ProcessBreakdown.objects.filter(process=template_instance, breakdown="testing")
                if obj:
                    testing_obj = obj.first()
                    testing_obj.Quantity = qty
                    testing_obj.total = time * qty
                    testing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=template_instance, breakdown="testing", time=time,
                                                    Quantity=qty, total=time*qty)
        forms = request.POST.get('forms')
        if forms:
            forms_instance = None
            obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="forms")
            if obj:
                forms_instance = obj.first()
            else:
                forms_instance = ProcessJustification.objects.create(requirements=requirement_obj,
                                                                     justification="forms")
            form_creation = request.POST.get('form_creation')
            if form_creation:
                time = int(request.POST.get('form_creation_time'))
                qty = int(request.POST.get('form_creation_quantity'))
                obj = ProcessBreakdown.objects.filter(process=forms_instance, breakdown="creation")
                if obj:
                    creation_obj = obj.first()
                    creation_obj.Quantity = qty
                    creation_obj.total = time * qty
                    creation_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=forms_instance, breakdown="creation", time=time,
                                                    Quantity=qty, total=time*qty)
            form_testing = request.POST.get('form_testing')
            if form_testing:
                time = int(request.POST.get('form_testing_time'))
                qty = int(request.POST.get('form_testing_quantity'))
                obj = ProcessBreakdown.objects.filter(process=forms_instance, breakdown="testing")
                if obj:
                    testing_obj = obj.first()
                    testing_obj.Quantity = qty
                    testing_obj.total = time * qty
                    testing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=forms_instance, breakdown="testing", time=time,
                                                    Quantity=qty, total=time*qty)
        apis = request.POST.get('apis')
        if apis:
            apis_instance = None
            obj = ProcessJustification.objects.filter(requirements=requirement_obj, justification="apis")
            if obj:
                apis_instance = obj.first()
            else:
                apis_instance = ProcessJustification.objects.create(requirements=requirement_obj,
                                                                    justification="apis")
            new_api = request.POST.get('new_api')
            if new_api:
                time = int(request.POST.get('new_api_time'))
                qty = int(request.POST.get('new_api_quantity'))
                obj = ProcessBreakdown.objects.filter(process=apis_instance, breakdown="new")
                if obj:
                    new_obj = obj.first()
                    new_obj.Quantity = qty
                    new_obj.total = time * qty
                    new_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=apis_instance, breakdown="new", time=time,
                                                    Quantity=qty, total=time * qty)
            existing_api = request.POST.get('existing_api')
            if existing_api:
                time = int(request.POST.get('existing_api_time'))
                qty = int(request.POST.get('existing_api_quantity'))
                obj = ProcessBreakdown.objects.filter(process=apis_instance, breakdown="existing")
                if obj:
                    existing_obj = obj.first()
                    existing_obj.Quantity = qty
                    existing_obj.total = time * qty
                    existing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=apis_instance, breakdown="existing", time=time,
                                                    Quantity=qty, total=time * qty)
            api_testing = request.POST.get('api_testing')
            if api_testing:
                time = int(request.POST.get('api_testing_time'))
                qty = int(request.POST.get('api_testing_quantity'))
                obj = ProcessBreakdown.objects.filter(process=apis_instance, breakdown="testing")
                if obj:
                    testing_obj = obj.first()
                    testing_obj.Quantity = qty
                    testing_obj.total = time * qty
                    testing_obj.save()

                else:
                    ProcessBreakdown.objects.create(process=apis_instance, breakdown="testing", time=time,
                                                    Quantity=qty, total=time * qty)

        active_requirements = Requirement.objects.all().filter(is_active=True)
        context = {"active_requirements": active_requirements}
        return render(request, "management/doc_templates/active_requirements.html", context)


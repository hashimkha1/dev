import datetime
import json
import ast
from datetime import date, timedelta
import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.urls import reverse, reverse_lazy

# from django.contrib.auth.views import PasswordChangeView ,PasswordSetView
# from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.utils.decorators import method_decorator
from management.utils import email_template
from .decorators import unauthenticated_user
from django.db.models.aggregates import Avg, Sum
from .forms import UserForm, LoginForm, CredentialCategoryForm, CredentialForm
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import CustomerUser, Tracker, CredentialCategory, Credential, Department
from django.db.models import Q
from management.models import Task
from application.models import UserProfile
from finance.models import Default_Payment_Fees,Payment_History
from management.utils import email_template
from django.http import QueryDict
import string, random
from management.utils import email_template

# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/layout.html")


# @allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, "accounts/clients/thank.html")


# ---------------ACCOUNTS VIEWS----------------------


def join(request):
    if request.method == "POST":
        if request.POST.get("category") == "3":
            student_data = {}
            student_data["first_name"] = request.POST.get("first_name")
            student_data["last_name"] = request.POST.get("last_name")
            student_data["address"] = request.POST.get("address")
            student_data["category"] = request.POST.get("category")
            student_data["sub_category"] = request.POST.get("sub_category")
            student_data["username"] = request.POST.get("username")
            student_data["password1"] = request.POST.get("password1")
            student_data["password2"] = request.POST.get("password2")
            student_data["email"] = request.POST.get("email")
            student_data["phone"] = request.POST.get("phone")
            student_data["gender"] = request.POST.get("gender")
            student_data["city"] = request.POST.get("city")
            student_data["state"] = request.POST.get("state")
            student_data["country"] = request.POST.get("country")
            student_data["resume_file"] = request.POST.get("resume_file")
            today = date.today()

            contract_date = today.strftime("%d %B, %Y")
            check_default_fee = Default_Payment_Fees.objects.all()
            if check_default_fee:
                default_fee = Default_Payment_Fees.objects.get(id=1)
            else:
                default_payment_fees = Default_Payment_Fees(
                    job_down_payment_per_month=500,
                    job_plan_hours_per_month=40,
                    student_down_payment_per_month=500,
                    student_bonus_payment_per_month=100,
                )
                default_payment_fees.save()
                default_fee = Default_Payment_Fees.objects.get(id=1)
            if (
                request.POST.get("category") == "3"
                and request.POST.get("sub_category") == "1"
            ):
                return render(
                    request,
                    "management/doc_templates/supportcontract_form.html",
                    {
                        "job_support_data": student_data,
                        "contract_date": contract_date,
                        "default_fee": default_fee,
                    },
                )
            if (
                request.POST.get("category") == "3"
                and request.POST.get("sub_category") == "2"
            ):
                return render(
                    request,
                    "management/doc_templates/trainingcontract_form.html",
                    {
                        "student_data": student_data,
                        "contract_date": contract_date,
                        "default_fee": default_fee,
                    },
                )
        else:
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                print("category", form.cleaned_data.get("category"))

        if form.is_valid():
            print("category", form.cleaned_data.get("category"))

            # if form.cleaned_data.get('category') == 2:# Staff-->Full,Agent,Other
            #     if form.cleaned_data.get('sub_category') == 6:
            #         form.instance.is_admin = True
            #         form.instance.is_superuser = True
            #     else:
            #         form.instance.is_employee = True
            # elif form.cleaned_data.get('category') == 3:# Client
            #     form.instance.is_client = True
            # else:
            #     form.instance.is_applicant = True
            if form.cleaned_data.get("category") == 1:
                form.instance.is_applicant = True
            elif form.cleaned_data.get("category") == 2:
                form.instance.is_employee = True
            elif form.cleaned_data.get("category") == 3:
                form.instance.is_client = True
            else:
                form.instance.is_admin = True

            form.save()

            username = form.cleaned_data.get('username')
            category = form.cleaned_data.get('category')
            gender = form.cleaned_data.get('gender')
            country = form.cleaned_data.get('country')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:account-login')
    else:
        msg = "error validating form"
        form = UserForm()
        print(msg)
    return render(request, "accounts/registration/join.html", {"form": form})


def CreateProfile():
    users = CustomerUser.objects.filter(profile=None)
    for user in users:
        UserProfile.objects.create(user=user)


def login_view(request):

    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            request.session["siteurl"] = settings.SITEURL
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            account = authenticate(username=username, password=password)
            CreateProfile()
            # If Category is Staff/employee
            if account is not None and account.category == 2:
                if account.sub_category == 2:  # contractual
                    login(request, account)
                    return redirect("management:requirements-active")
                else:  # parttime (agents) & Fulltime
                    login(request, account)
                    return redirect("management:user_task", username=request.user)

            # If Category is client/customer
            elif account is not None and account.category == 3:
                if account.sub_category == 1:  # Job Support
                    login(request, account)
                    return redirect("accounts:user-list", username=request.user)
                else:  # Student
                    login(request, account)
                    return redirect("data:bitraining")

            # If Category is applicant
            elif account is not None and account.profile.section is not None:
                if account.profile.section == "A":
                    login(request, account)
                    return redirect("application:section_a")
                elif account.profile.section == "B":
                    login(request, account)
                    return redirect("application:section_b")
                elif account.profile.section == "C":
                    login(request, account)
                    return redirect("application:policies")
                else:
                    login(request, account)
                    return redirect("application:first_interview")

            elif account is not None and account.category == 1:
                if account.country in ("KE", "UG", "RW", "TZ"):  # Male
                    if account.gender == 1:
                        login(request, account)
                        return redirect("application:first_interview")
                    if account.account_profile.section == "A":
                        login(request, account)
                        return redirect("application:sectionA")
                    elif account.account_profile.section == "B":
                        login(request, account)
                        return redirect("application:sectionB")
                    elif account.account_profile.section == "C":
                        login(request, account)
                        return redirect("application:policies")
                    else:
                        login(request, account)
                        return redirect("application:first_interview")
                else:
                    login(request, account)
                    return redirect("application:first_interview")

            elif account is not None and account.is_admin:
                login(request, account)
                return redirect("main:layout")
            else:
                messages.success(request, f"Invalid credentials.Kindly Try again!!")

            # elif section is not None:
            #         if section == "B":
            #         login(request, account)
            #         return redirect("application:sectionA")
            #     elif section == "C":
            #         login(request, account)
            #         return redirect("application:sectionB")
            #     else:
            #         login(request, account)
            #         return redirect("application:sectionC")

    return render(
        request, "accounts/registration/login.html", {"form": form, "msg": msg}
    )


# ================================USERS SECTION================================
def users(request):
    users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
    if request.user.is_superuser:
        return render(request, "accounts/admin/superpage.html", {"users": users})

    if request.user.is_admin:
        return render(request, "accounts/admin/adminpage.html", {"users": users})
    else:
        return redirect("main:layout")


class SuperuserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomerUser
    success_url = "/accounts/users"
    # fields=['category','address','city','state','country']
    fields = [
        "category",
        "sub_category",
        "first_name",
        "last_name",
        "date_joined",
        "email",
        "gender",
        "phone",
        "address",
        "city",
        "state",
        "country",
        "is_superuser",
        "is_admin",
        "is_employee",
        "is_client",
        "is_applicant",
        "is_active",
        "is_staff",
    ]

    def form_valid(self, form):
        # form.instance.username=self.request.user
        # if request.user.is_authenticated:
        if self.request.user.is_superuser:  # or self.request.user.is_authenticated :
            return super().form_valid(form)
        #  elif self.request.user.is_authenticated:
        #      return super().form_valid(form)
        return False

    def test_func(self):
        user = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser:  # or self.request.user == user.username:
            return True
        return False


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomerUser
    success_url = "/accounts/users"
    # fields=['category','address','city','state','country']
    fields = [
        "category",
        "sub_category",
        "first_name",
        "last_name",
        "date_joined",
        "email",
        "gender",
        "phone",
        "address",
        "city",
        "state",
        "country",
        "is_admin",
        "is_employee",
        "is_client",
        "is_applicant",
    ]

    def form_valid(self, form):
        # form.instance.username=self.request.user
        # if request.user.is_authenticated:
        if self.request.user.is_superuser or self.request.user.is_admin:
            return super().form_valid(form)
        #  elif self.request.user.is_admin:
        #       return super().form_valid(form)
        return False

    def test_func(self):
        user = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser or self.request.user.is_admin:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomerUser
    success_url = "/accounts/users"

    def test_func(self):
        user = self.get_object()
        # if self.request.user == user.username:
        if self.request.user.is_superuser:
            return True
        return False


def PasswordResetCompleteView(request):
    return render(request, "accounts/registration/password_reset_complete.html")


''' 
class PasswordsChangeView(PasswordChangeView):
    #model=CustomerUser
    from_class=PasswordChangeForm
    template_name='accounts/registration/password_change_form.html'
    success_url=reverse_lazy('accounts:account-login')

class PasswordsSetView(PasswordChangeView):
    #model=CustomerUser
    from_class=SetPasswordForm
    success_url=reverse_lazy('accounts:account-login')

def reset_password(email, from_email, template='registration/password_reset_email.html'):
    """
    Reset the password for all (active) users with given E-Mail adress
    """
    form = PasswordResetForm({'email': email})
    #form = PasswordResetForm({'email':'sample@sample.com'})
    return form.save(from_email=from_email, email_template_name=template)
''' 
#================================EMPLOYEE SECTION================================
def Employeelist(request):
    employees=CustomerUser.objects.filter(Q(category = 2)|Q(is_employee=True)).order_by('-date_joined')
    return render(request, 'accounts/employees/employees.html', {'employees': employees})

#================================CLIENT SECTION================================

def newcredentialCategory(request):
    if request.method == "POST":
        form = CredentialCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accounts:account-crendentials")
    else:
        form = CredentialCategoryForm()
    return render(
        request, "accounts/admin/forms/credentialCategory_form.html", {"form": form}
    )


def newcredential(request):
    if request.method == "POST":
        form = CredentialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accounts:account-crendentials")
    else:
        form = CredentialForm()
    return render(request, "accounts/admin/forms/credential_form.html", {"form": form})


def credential_view(request):
    categories = CredentialCategory.objects.all().order_by("-entry_date")
    credentials = Credential.objects.all().order_by("-entry_date")
    departments = Department(request)
    context = {
        "departments": departments,
        "categories": categories,
        "credentials": credentials,
        "show_password": False,
    }

    try:
        otp = request.POST["otp"]
        if otp == request.session["security_otp"]:
            del request.session["security_otp"]
            context["show_password"] = True
            return render(request, "accounts/admin/credentials.html", context)
        else:
            error_context = {"message": "Invalid OTP"}
            return render(
                request, "accounts/admin/email_verification.html", error_context
            )

    except:
        return render(request, "accounts/admin/credentials.html", context)


def security_verification(request):
    subject = "One time verification code to view passwords"
    to = request.user.email
    otp = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    request.session["security_otp"] = otp
    html_content = "Your One time verification code is " + otp
    print(to, otp)
    email_template(subject, to, html_content)
    return render(request, "accounts/admin/email_verification.html")


# ================================EMPLOYEE SECTION================================
def Employeelist(request):
    employees = CustomerUser.objects.filter(
        Q(category=2) | Q(is_employee=True)
    ).order_by("-date_joined")
    return render(
        request, "accounts/employees/employees.html", {"employees": employees}
    )


# ================================CLIENT SECTION================================
def clientlist(request):
    clients = CustomerUser.objects.filter(Q(category=3) | Q(is_client=True)).order_by(
        "-date_joined"
    )
    return render(request, "accounts/clients/clientlist.html", {"clients": clients})


@method_decorator(login_required, name="dispatch")
class ClientDetailView(DetailView):
    template_name = "accounts/clients/client_detail.html"
    model = CustomerUser
    ordering = ["-date_joined "]


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomerUser
    success_url = "/accounts/clients"
    fields = ["category", "address", "city", "state", "country"]
    form = UserForm

    def form_valid(self, form):
        # form.instance.username=self.request.user
        # if request.user.is_authenticated:
        if self.request.user.is_superuser or self.request.user.is_authenticated:
            return super().form_valid(form)
        #  elif self.request.user.is_authenticated:
        #      return super().form_valid(form)
        return False

    def test_func(self):
        client = self.get_object()
        # if self.request.user == client.username:
        #     return True
        if self.request.user.is_superuser or self.request.user == client.username:
            return True
        return False

@method_decorator(login_required, name="dispatch")
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomerUser
    success_url = "/accounts/clients"

    def test_func(self):
        client = self.get_object()
        # if self.request.user == client.username:
        if self.request.user.is_superuser:
            return True
        return False


@login_required(login_url="accounts:account-login")
def profile(request):
    return render(request, "accounts/profile.html")


# ----------------------TIME TRACKING CLASS-BASED VIEWS--------------------------------
@method_decorator(login_required, name="dispatch")
class TrackDetailView(DetailView):
    model = Tracker
    ordering = ["-login_date"]


@method_decorator(login_required, name="dispatch")
class TrackListView(ListView):
    model = Tracker
    template_name = "accounts/tracker.html"
    context_object_name = "trackers"
    ordering = ["-login_date"]
    # # total_time=Tracker.objects.all().aggregate(Your_Total_Time=Sum('duration'))
    # def get_queryset(self, *args, **kwargs):
    #     qs = super(TrackListView, self).get_queryset(*args, **kwargs)
    #     em = Tracker.objects.all().values().order_by('-pk')[0]
    #     trackers=Tracker.objects.all().filter(author=em.get('author_id')).order_by('-login_date')
    #     num =trackers.count()
    #     Used=trackers.aggregate(Used_Time=Sum('duration'))  
    #     Usedtime=Used.get('Used_Time')
    #     customer_get = CustomerUser.objects.values_list('username','email').get(id=em.get('author_id'))
    #     if Usedtime < 30:
    #         subject = "New Contract Alert"
    #         to = customer_get[1]
    #         html_content = f"""
    #             <span><h3>Hi {customer_get[0]},</h3>Your Total Time at CODA is less than 30 hours kindly click here to sign a new contract <br>
    #             <a href='http://127.0.0.1:8000/finance/new_contract/Antony/'>click here to sign new contract</a><br>
    #             </span>"""
    #         email_template(subject, to, html_content)

    #     return qs

def usertracker(request, user=None, *args, **kwargs):
    user = get_object_or_404(CustomerUser, username=kwargs.get("username"))
    trackers = Tracker.objects.all().filter(author=user).order_by("-login_date")
    em = Tracker.objects.all().values().order_by('-pk')[0]
    num = trackers.count()
    # Check on my_time=avg("time")
    my_time = trackers.aggregate(Assigned_Time=Avg("time"))
    Used = trackers.aggregate(Used_Time=Sum("duration"))
    Usedtime = Used.get("Used_Time")
    # plantime = my_time.get("Assigned_Time")
    payment_details = Payment_History.objects.filter(customer= user)
    contract_plan_hours = payment_details.aggregate(Sum('plan'))
    assigned_hours =0
    if contract_plan_hours.get('plan__sum'):
        assigned_hours = contract_plan_hours.get('plan__sum') * 40
    if my_time.get('Assigned_Time'):
        plantime=my_time.get('Assigned_Time') + assigned_hours
    plantime = assigned_hours
    try:
        delta = round(plantime - Usedtime)
    except (TypeError, AttributeError):
        delta = 0
    customer_get = CustomerUser.objects.values_list('username','email').get(id=em.get('author_id'))
    if delta < 30:
        subject = "New Contract Alert"
        to = customer_get[1]
        html_content = f"""
            <span><h3>Hi {customer_get[0]},</h3>Your Total Time at CODA is less than 30 hours kindly click here to sign a new contract <br>
            <a href='https://www.codanalytics.net/finance/new_contract/{request.user}/'>click here to sign new contract</a><br>
            
            </span>"""
        email_template(subject, to, html_content)

    context = {
        "trackers": trackers,
        "num": num,
        "plantime": plantime,
        "Usedtime": Usedtime,
        "delta": delta,
    }
    return render(request, "accounts/usertracker.html", context)


class TrackCreateView(LoginRequiredMixin, CreateView):
    model = Tracker
    success_url = "/accounts/tracker"
    # success_url="usertime"
    # fields=['category','task','duration']
    fields = [
        "employee",
        "author",
        "category",
        "sub_category",
        "task",
        "duration",
        "plan",
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            if form.instance.category == "Job_Support":
                points, targetpoints = Task.objects.values_list(
                    "point", "mxpoint"
                ).filter(
                    Q(activity_name=form.instance.category)
                    | Q(activity_name="job_support")
                    | Q(activity_name="jobsupport")
                    | Q(activity_name="Jobsupport")
                    | Q(activity_name="JobSupport")
                    | Q(activity_name="Job Support")
                    | Q(activity_name="Job support")
                    | Q(activity_name="job support"),
                    employee=form.instance.employee,
                )[
                    0
                ]

                if (
                    form.instance.sub_category == "Development"
                    or form.instance.sub_category == "Testing"
                ):
                    points = float(points) + (0.5 * form.instance.duration)
                else:
                    points = float(points) + form.instance.duration

                if points >= targetpoints:
                    targetpoints += 10

                Task.objects.filter(
                    Q(activity_name=form.instance.category)
                    | Q(activity_name="job_support")
                    | Q(activity_name="jobsupport")
                    | Q(activity_name="Jobsupport")
                    | Q(activity_name="JobSupport")
                    | Q(activity_name="Job Support")
                    | Q(activity_name="Job support")
                    | Q(activity_name="job support"),
                    employee=form.instance.employee,
                ).update(point=points, mxpoint=targetpoints)
        except:
            pass

        return super().form_valid(form)


""" 
@method_decorator(login_required, name='dispatch')
class TrackCreateView(LoginRequiredMixin, CreateView):
    model=Tracker
    success_url="/accounts/tracker"
    #success_url="usertime"
    # There is need to look at the column for client to get the id
    fields=['employee','author','category','task','duration','plan']

    def form_valid(self,form):
        form.instance.author=self.request.user
        total_duration_fil = Tracker.objects.filter(author=self.request.user)
        total_duration = 0
        for data in total_duration_fil.all():
            total_duration += data.duration
        # Needs a validation message if the employee does not have tasks

        #print("total_duration",total_duration)
        #x=Task.objects.values_list("mxpoint",flat=True).get(employee=self.request.user)
        #print("Values",x)
        if form.instance.duration+total_duration > Task.objects.values_list("mxpoint",flat=True).get(employee=self.request.user): 
            messages.error(self.request, "Total duration is greater than maximum assigned points.")
            return super().form_invalid(form)
        return super().form_valid(form)  
"""

@method_decorator(login_required, name="dispatch")
class TrackUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tracker
    success_url = "/accounts/tracker"

    fields = ["employee", "author", "plan", "category", "task", "duration", "time"]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        if self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_staff:
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        track = self.get_object()
        if self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_staff:
            return True
        # elif self.request.user ==track.author:
        #     return True
        else:
            return False

@method_decorator(login_required, name="dispatch")
class TrackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tracker
    success_url = "/accounts/tracker"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False



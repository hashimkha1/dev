from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import UserForm, LoginForm
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import  redirect, render
from django.views.generic import (
    DeleteView,
    DetailView,
    UpdateView,
)
from .models import CustomerUser
from .utils import agreement_data,employees
from main.filters import UserFilter
from .models import UserProfile
# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/newlayout.html")


# @allowed_users(allowed_roles=['admin'])
def thank(request):
    return render(request, "accounts/clients/thank.html")


# ---------------ACCOUNTS VIEWS----------------------

def join(request):
    form = UserForm()  # Define form variable with initial value
    if request.method == "POST":
        previous_user = CustomerUser.objects.filter(email=request.POST.get("email"))
        if len(previous_user) > 0:
            messages.success(request, f'User already exists with this email')
            return redirect("/password-reset")
        else:
            contract_data, contract_date = agreement_data(request)
            form = UserForm(request.POST)  # Assign form with request.POST data
            if form.is_valid():
                if form.cleaned_data.get("category") == 2:
                    form.instance.is_staff = True
                elif form.cleaned_data.get("category") == 3 or form.cleaned_data.get("category") == 4:
                    form.instance.is_client = True
                else:
                    form.instance.is_applicant = True

                form.save()
                return redirect('accounts:account-login')
    else:
        msg = "error validating form"
        print(msg)
    
    return render(request, "accounts/registration/coda/join.html", {"form": form})


# ---------------ACCOUNTS VIEWS----------------------
def create_profile():
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
           # create_profile()
            
            # If Category is Staff/employee
            if account is not None and account.category == 2:
                if account.is_staff and not account.is_employee_contract_signed:
                    login(request, account)
                    return redirect("management:employee_contract")
                
                
                else:  # parttime (agents) & Fulltime
                    login(request, account)
                    return redirect("management:companyagenda")

            # If Category is client/customer:# Student # Job Support
            elif account is not None and (account.category == 3 or account.category == 4) :
                login(request, account)
                return redirect('management:companyagenda')
            
            elif account is not None and (account.category == 5) :
                login(request, account)
                print("category,subcat",account.category,account.sub_category)
                return redirect('management:companyagenda')
           
            elif account is not None and account.profile.section is not None and account.category == 1:
                # if account.country in ("KE", "UG", "RW", "TZ"):  # Male
                # if account.gender == 1:
                #     login(request, account)
                #     return redirect("application:interview")
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
                    return redirect("application:interview")
            elif account is not None and account.profile.section is not None and account.category == 1 and account.sub_category==0:
                    login(request, account)
                    # print("account.category",account.sub_category)
                    return redirect("application:policies")
            
            elif account is not None and account.is_admin:
                login(request, account)
                # return redirect("main:layout")
                return redirect("management:companyagenda")
            else:
                msg=f"Invalid credentials.Kindly Try again!!"
                return render(
                        request, "accounts/registration/login_page.html", {"form": form, "msg": msg}
                    )
    return render(
        request, "accounts/registration/login_page.html", {"form": form, "msg": msg}
    )


# ================================USERS SECTION================================
def users(request):
    users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
    userfilters=UserFilter(request.GET,queryset=users)

    # Use the Paginator to paginate the queryset
    paginator = Paginator(userfilters.qs, 10) # Show 10 objects per page
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    context={
        # "users": queryset,
        "userfilters": userfilters,
        "objects":objects
    }
    if request.user.is_superuser:
        return render(request, "accounts/admin/superpage.html", context)
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
        "username",
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
        "is_staff",
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


# ================================EMPLOYEE SECTION================================
def Employeelist(request):
    employee_subcategories,active_employees=employees()
    context={
        "employee_subcategories":employee_subcategories,
        "active_employees":active_employees,
    }
    return render(request, 'accounts/employees/employeelist.html', context)
# ================================CLIENT SECTION================================
def clientlist(request):
    clients = {
        'students': CustomerUser.objects.filter(Q(category=4), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'jobsupport': CustomerUser.objects.filter(Q(category=3), Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'interview': CustomerUser.objects.filter(Q(category=4),  Q(is_client=True), Q(is_active=True)).order_by('-date_joined'),
        'past': CustomerUser.objects.filter(Q(is_client=True), Q(is_active=False)).order_by('-date_joined'),
    }
    template_name = "accounts/clients/clientlist.html"
    
    return render(request, template_name, clients)


@method_decorator(login_required, name="dispatch")
class ClientDetailView(DetailView):
    template_name = "accounts/clients/client_detail.html"
    model = CustomerUser
    ordering = ["-date_joined "]

@method_decorator(login_required, name="dispatch")
class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomerUser
    success_url = "/accounts/clients"
    fields = ["category", "address", "city", "state", "country"]
    form = UserForm

    def form_valid(self, form):
        # form.instance.username=self.request.user
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
            # or self.request.user.is_staff
        ):
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        # client = self.get_object()
        if (
            self.request.user.is_superuser
            or self.request.user.is_admin
            # or self.request.user.is_staff
        ):
            return True
        else:
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
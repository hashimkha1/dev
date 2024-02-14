import math
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import UserForm
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse
from .models import CustomerUser
from .utils import agreement_data,employees,compute_default_fee,get_clients_time
from main.filters import UserFilter
# from management.models import Task
#from application.models import UserProfile,Assets
# from finance.models import Payment_History,Payment_Information
# from mail.custom_email import send_email
import string, random
from .utils import generate_random_password,JOB_SUPPORT_CATEGORIES

from django.urls import reverse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from allauth.account.signals import user_logged_in
# from django.dispatch import receiver
# from allauth.socialaccount.models import SocialAccount
from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect

# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/newlayout.html")


# # @allowed_users(allowed_roles=['admin'])
# def thank(request):
#     return render(request, "accounts/clients/thank.html")


# # ---------------ACCOUNTS VIEWS----------------------

# def join(request):
#     form = UserForm()  # Define form variable with initial value
#     if request.method == "POST":
#         previous_user = CustomerUser.objects.filter(email=request.POST.get("email"))
#         if len(previous_user) > 0:
#             messages.success(request, f'User already exists with this email')
#             return redirect("/password-reset")
#         else:
#             contract_data, contract_date = agreement_data(request)
#             form = UserForm(request.POST)  # Assign form with request.POST data
#             if form.is_valid():
#                 if form.cleaned_data.get('category') in [3,4,5,6]:

#                     random_password = generate_random_password(8)
#                     form.instance.username = form.cleaned_data.get('email')
#                     form.instance.password1 = random_password
#                     form.instance.password2 = random_password
#                     form.instance.gender = None
#                     # form.instance.phone = "0000000000"

#                 if form.cleaned_data.get("category") == 2:
#                     form.instance.is_staff = True
#                 elif form.cleaned_data.get("category") == 3 or form.cleaned_data.get("category") == 4:
#                     form.instance.is_client = True
#                 else:
#                     form.instance.is_applicant = True

#                 form.save()

               
#                 return redirect('accounts:account-login')
#     else:
#         msg = "error validating form"
#         print(msg)
    
#     return render(request, "accounts/registration/coda/join.html", {"form": form})


# def join(request):
#     if request.method == "POST":
#         previous_user = CustomerUser.objects.filter(email = request.POST.get("email"))
#         if len(previous_user) > 0:
#             messages.success(request, f'User already exist with this email')
#             form = UserForm()
#             return redirect("/password-reset")
#         else:
#             contract_data,contract_date=agreement_data(request)
#             dyc_total_amount,dyc_down_payment,early_registration_bonus=DYCDefaultPayments()
#             if request.POST.get("category") == "3":
#                 check_default_fee = Default_Payment_Fees.objects.all()
#                 if check_default_fee:
#                     # default_fee = Default_Payment_Fees.objects.get(id=1)
#                     default_fee = Default_Payment_Fees.objects.all().first()
#                 else:
#                     default_payment_fees = Default_Payment_Fees(
#                         job_down_payment_per_month=1000,
#                         job_plan_hours_per_month=40,
#                         student_down_payment_per_month=500,
#                         student_bonus_payment_per_month=100,
#                     )
#                     default_payment_fees.save()
#                     # default_fee = Default_Payment_Fees.objects.get(id=1)
#                     default_fee = Default_Payment_Fees.objects.all().first()
#                 if (
#                     request.POST.get("category") == "3"
#                     and request.POST.get("sub_category") == "1"
#                 ):
#                     return render(
#                         request,
#                         "management/contracts/supportcontract_form.html",
#                         {
#                             "job_support_data": contract_data,
#                             "contract_date": contract_date,
#                             "payment_data": default_fee,
#                         },
#                     )
#                 if (
#                     request.POST.get("category") == "3"
#                     and request.POST.get("sub_category") == "2"
#                 ):
#                     return render(
#                         request,
#                         "management/contracts/trainingcontract_form.html",
#                         {
#                             "contract_data": contract_data,
#                             "contract_date": contract_date,
#                             "payment_data": default_fee,
#                         },
#                     )
#                 if (request.POST.get("category") == "4"):
#                     context={
#                                     'job_support_data': contract_data,
#                                     'student_data': contract_data,
#                                     'contract_date':contract_date,
#                                     'payments':default_fee
#                                 }
#                     return render(request, 'management/contracts/dyc_contracts/student_contract.html',context)
#                     # return render(
#                     #     request,
#                     #     "management/contracts/dyc_contracts/student_contract.html",
#                     #     {
#                     #         "contract_data": contract_data,
#                     #         "contract_date": contract_date,
#                     #         "dyc_total_amount": dyc_total_amount,
#                     #         "contract_date": dyc_down_payment,
#                     #         "early_registration_bonus": early_registration_bonus,
#                     #         "default_fee": default_fee,
#                     #     },
#                     # )
#             else:
#                 form = UserForm(request.POST, request.FILES)
#                 if form.is_valid():
#                     print("category", form.cleaned_data.get("category"))

#             if form.is_valid():
#                 if form.cleaned_data.get("category") == 2:
#                     form.instance.is_staff = True
#                 elif form.cleaned_data.get("category") == 3:
#                     form.instance.is_client = True
#                 else:
#                     form.instance.is_applicant = True

#                 form.save()
#                 # messages.success(request, f'Account created for {username}!')
#                 return redirect('accounts:account-login')
#     else:
#         msg = "error validating form"
#         form = UserForm()
#         print(msg)
#     return render(request, "accounts/registration/coda/join.html", {"form": form})


# # # ---------------ACCOUNTS VIEWS----------------------
# def create_profile():
#     users = CustomerUser.objects.filter(profile=None)
#     assets = Assets.objects.all()
#     # print(assets)
#     if not assets:
#         Assets.objects.create(
#             name='default',
#             category='default',
#             description='default',
#             image_url='default',
#         )
#     for user in users:
#         UserProfile.objects.create(user=user)



# def login_view(request):
#     form = LoginForm(request.POST or None)
#     msg = None

#     #when error occur while login/signup with social account, we are redirecting it to login page of website
#     if request.method == 'GET':
#         sociallogin = request.session.pop("socialaccount_sociallogin", None)
        
#         if sociallogin is not None:
#             msg = 'Error with social login. check your credential or try to sing up manually.'
    
#     if request.method == "POST":
#         if form.is_valid():
#             request.session["siteurl"] = settings.SITEURL
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             account = authenticate(username=username, password=password)
#             create_profile()
            
#             # If Category is Staff/employee
#             if account is not None and account.category == 2:
#                 if account.is_staff and not account.is_employee_contract_signed:
#                     login(request, account)
#                     return redirect("management:employee_contract")
                
#                 # if account.is_staff and account.is_employee_contract_signed:
#                 #     login(request, account)
#                 #     return redirect("management:companyagenda")

#                 # if account.sub_category == 2 or account.sub_category == 3:  # contractual
#                 #     login(request, account)
#                 #     return redirect("management:requirements-active")
                
#                 else:  # parttime (agents) & Fulltime
#                     login(request, account)
#                     return redirect("management:companyagenda")

#             # If Category is client/customer:# Student # Job Support
#             elif account is not None and (account.category == 3 or account.category == 4) :
#                 login(request, account)
#                 return redirect('management:companyagenda')
            
#             elif account is not None and (account.category == 5) :
#                 login(request, account)
#                 print("category,subcat",account.category,account.sub_category)
#                 return redirect('management:companyagenda')
           
#             # If Category is applicant
#             # elif account is not None and account.profile.section is not None:
#             #     if account.profile.section == "A":
#             #         login(request, account)
#             #         return redirect("application:section_a")
#             #     elif account.profile.section == "B":
#             #         login(request, account)
#             #         return redirect("application:section_b")
#             #     elif account.profile.section == "C":
#             #         login(request, account)
#             #         return redirect("application:policies")
#             #     else:
#             #         login(request, account)
#             #         return redirect("application:interview")
#             elif account is not None and account.profile.section is not None and account.category == 1:
#                 # if account.country in ("KE", "UG", "RW", "TZ"):  # Male
#                 # if account.gender == 1:
#                 #     login(request, account)
#                 #     return redirect("application:interview")
#                 if account.profile.section == "A":
#                     login(request, account)
#                     return redirect("application:section_a")
#                 elif account.profile.section == "B":
#                     login(request, account)
#                     return redirect("application:section_b")
#                 elif account.profile.section == "C":
#                     login(request, account)
#                     return redirect("application:policies")
#                 else:
#                     login(request, account)
#                     return redirect("application:interview")
#             elif account is not None and account.profile.section is not None and account.category == 1 and account.sub_category==0:
#                     login(request, account)
#                     # print("account.category",account.sub_category)
#                     return redirect("application:policies")
            
#             elif account is not None and account.is_admin:
#                 login(request, account)
#                 # return redirect("main:layout")
#                 return redirect("management:companyagenda")
#             else:
#                 # messages.success(request, f"Invalid credentials.Kindly Try again!!")
#                 msg=f"Invalid credentials.Kindly Try again!!"
#                 return render(
#                         request, "accounts/registration/login_page.html", {"form": form, "msg": msg}
#                     )
#     return render(
#         request, "accounts/registration/login_page.html", {"form": form, "msg": msg}
#     )


# # ================================USERS SECTION================================
# def users(request):
#     users = CustomerUser.objects.filter(is_active=True).order_by("-date_joined")
#     userfilters=UserFilter(request.GET,queryset=users)

#     # Use the Paginator to paginate the queryset
#     paginator = Paginator(userfilters.qs, 10) # Show 10 objects per page
#     page = request.GET.get('page')
#     objects = paginator.get_page(page)
#     context={
#         # "users": queryset,
#         "userfilters": userfilters,
#         "objects":objects
#     }
#     if request.user.is_superuser:
#         return render(request, "accounts/admin/superpage.html", context)
#     else:
#         return redirect("main:layout")


# class SuperuserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = CustomerUser
#     success_url = "/accounts/users"
#     # fields=['category','address','city','state','country']
#     fields = [
#         "category",
#         "sub_category",
#         "first_name",
#         "last_name",
#         "username",
#         "date_joined",
#         "email",
#         "gender",
#         "phone",
#         "address",
#         "city",
#         "state",
#         "country",
#         "is_superuser",
#         "is_admin",
#         "is_client",
#         "is_applicant",
#         "is_active",
#         "is_staff",
#     ]

#     def form_valid(self, form):
#         # form.instance.username=self.request.user
#         # if request.user.is_authenticated:
#         if self.request.user.is_superuser:  # or self.request.user.is_authenticated :
#             return super().form_valid(form)
#         #  elif self.request.user.is_authenticated:
#         #      return super().form_valid(form)
#         return False

#     def test_func(self):
#         user = self.get_object()
#         # if self.request.user == client.username:
#         #     return True
#         if self.request.user.is_superuser:  # or self.request.user == user.username:
#             return True
#         return False


# class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = CustomerUser
#     success_url = "/accounts/users"
#     # fields=['category','address','city','state','country']
#     fields = [
#         "category",
#         "sub_category",
#         "first_name",
#         "last_name",
#         "date_joined",
#         "email",
#         "gender",
#         "phone",
#         "address",
#         "city",
#         "state",
#         "country",
#         "is_admin",
#         "is_staff",
#         "is_client",
#         "is_applicant",
#     ]

#     def form_valid(self, form):
#         # form.instance.username=self.request.user
#         # if request.user.is_authenticated:
#         if self.request.user.is_superuser or self.request.user.is_admin:
#             return super().form_valid(form)
#         #  elif self.request.user.is_admin:
#         #       return super().form_valid(form)
#         return False

#     def test_func(self):
#         user = self.get_object()
#         # if self.request.user == client.username:
#         #     return True
#         if self.request.user.is_superuser or self.request.user.is_admin:
#             return True
#         return False


# @method_decorator(login_required, name="dispatch")
# class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = CustomerUser
#     success_url = "/accounts/users"

#     def test_func(self):
#         user = self.get_object()
#         # if self.request.user == user.username:
#         if self.request.user.is_superuser:
#             return True
#         return False


# def PasswordResetCompleteView(request):
#     return render(request, "accounts/registration/password_reset_complete.html")


# ''' 
# class PasswordsChangeView(PasswordChangeView):
#     #model=CustomerUser
#     from_class=PasswordChangeForm
#     template_name='accounts/registration/password_change_form.html'
#     success_url=reverse_lazy('accounts:account-login')

# class PasswordsSetView(PasswordChangeView):
#     #model=CustomerUser
#     from_class=SetPasswordForm
#     success_url=reverse_lazy('accounts:account-login')

# def reset_password(email, from_email, template='registration/password_reset_email.html'):
#     """
#     Reset the password for all (active) users with given E-Mail adress
#     """
#     form = PasswordResetForm({'email': email})
#     #form = PasswordResetForm({'email':'sample@sample.com'})
#     return form.save(from_email=from_email, email_template_name=template)
# ''' 

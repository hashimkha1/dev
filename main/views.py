import requests
import json
from django.http import JsonResponse
from django.db.models import Q
from celery import shared_task
from django.shortcuts import redirect, render
from django.contrib import messages
import calendar,string
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from .models import Service,Plan,Assets
from .utils import Meetings,image_view,path_values
from codablog.models import Post
from finance.models import Payment_History, Payment_Information
from management.models import Advertisement
from coda_project.task import advertisement
from coda_project import settings
from application.models import UserProfile
from management.utils import task_assignment_random
from management.models import Whatsapp
from main.forms import WhatsappForm
from whatsapp.script import whatsapp
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView,
)
from accounts.forms import LoginForm
from .forms import RegistrationForm,ContactForm
from accounts.views import CreateProfile

# from finance.utils import pay_info
# from django.core.management import call_command
# importing modules
import urllib.request
from PIL import Image
from django.contrib.auth import get_user_model
User=get_user_model()

def error400(request):
    return render(request, "main/errors/400.html", {"title": "400Error"})

def error403(request):
    return render(request, "main/errors/403.html", {"title": "403Error"})

def error404(request):
    return render(request, "main/errors/404.html", {"title": "404Error"})
    
def error500(request):
    return render(request, "main/errors/500.html", {"title": "500Error"})

#Other Error pages or no results error
# def result(request):
#     return render(request, "main/errors/result.html", {"title": "result"})

def general_errors(request):
    # return render(request, "main/errors/noresult.html")
    context={'message':'message'}
    return render(request,'main/errors/generalerrors.html',context)

#  ===================================================================================   
def hendler400(request,exception):
    return render(request, "errors/400.html")

def hendler403(request,exception):
    return render(request, "main/errors/403.html")

def hendler404(request,exception):
    return render(request, "main/errors/404.html")

def hendler404(request,exception):
    return render(request, "main/errors/404.html")

def hendler500(request):
    return render(request, "main/errors/500.html")
    
def test(request):
    return render(request, "main/test.html", {"title": "test"})

def checkout(request):
    return render(request, "main/checkout.html", {"title": "checkout"})

def layout(request):
    # advertisement()
    posts=Post.objects.all()
    services=Service.objects.all()

    context={
            "services":services,
            "posts":posts,
            "title": "layout"
        }
    return render(request, "main/home_templates/newlayout.html",context)

# =====================DC_KENYA VIEWS=======================================
def dclayout(request):
    # advertisement()
    posts=Post.objects.all()
    services=Service.objects.all()

    context={
            "services":services,
            "posts":posts,
            "title": "DCKENYA"
        }
    return render(request, "main/dc48kenya/dc_layout.html",context)

def register(request):
    if request.method == "POST":
        previous_user = User.objects.filter(email = request.POST.get("email"))
        if len(previous_user) > 0:
            messages.success(request, f'User already exist with this email')
            form = RegistrationForm()
            return redirect("/password-reset")
        else:
            if form.is_valid():
                if form.cleaned_data.get("category") == 4:
                    form.instance.is_applicant = True
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('main:dc_login')
    else:
        msg = "error validating form"
        form = RegistrationForm()
    return render(request, "main/dc48kenya/dc_register.html", {"form": form,"msg":msg})


def dc48login(request):
    form = LoginForm(request.POST or None)
    msg = f'account with that username and password does not exist!'
    if request.method == "POST":
        if form.is_valid():
            request.session["siteurl"] = settings.SITEURL
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            account = authenticate(username=username, password=password)
            CreateProfile()
            # If Category is DC48KENYA User
            if account is not None and account.category == 4:
                if account.sub_category == 6:  # contractual
                    login(request, account)
                    return redirect("finance:list-inflow")
                else:  # parttime (agents) & Fulltime
                    login(request, account)
                    # return redirect("management:user_task", username=request.user)
                    return redirect("main:dc_home")
    return render(
       request, "main/dc48kenya/dc_login.html", {"form": form, "msg": msg})
    

# =====================PLAN=======================================
class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    success_url = "/plans/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def plans(request):
    day_name = date.today().strftime("%A")
    plans = Plan.objects.filter(is_active=True)
    plan_categories_list = Plan.objects.values_list(
                    'category', flat=True).distinct()
    plan_categories=sorted(plan_categories_list)
    # print(plan_categories)
    for plan in plans:
        delivery_date=plan.created_at +  timedelta(days=plan.duration*30)
    context = {
        "plans": plans,
        "plan_categories": plan_categories,
        "delivery_date": delivery_date,
        "day_name": day_name,
    }
    if request.user.is_superuser:
        return render(request, "main/plans.html", context)
    else:
        return render(request, "main/errors/404.html", context)

class PlanUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Plan
    fields ="__all__"

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:plans")

    def test_func(self):
        plan = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == plan.staff:
            return True
        return False

def delete_plan(request,id):
    plan = Plan.objects.get(pk=id)
    if request.user.is_superuser:
        plan.delete()
    return redirect('main:plans')

def about(request):
    sub_title=path_values(request)[-1]
    date_object="01/20/2023"
    start_date = datetime.strptime(date_object, '%m/%d/%Y')
    end_date=start_date + relativedelta(months=3)
    context={
        "start_date": start_date,
        "end_date": end_date,
        "title_team": "team",
        "title_about": "about",
        "title_letter": "letter",
    }
    if sub_title == 'team':
        return render(request, "main/team.html",context)
    elif sub_title == 'letter':
        return render(request, "main/doc_templates/letter.html",context)
    elif sub_title == 'about':
        return render(request, "main/about.html",context)
    

class UserCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    success_url = "/team/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def profiles(request):
    sub_title=path_values(request)[-1]
    images = Assets.objects.values_list('name', flat=True)
    coda_team = UserProfile.objects.filter(user__is_employee=True,user__is_active=True,user__is_staff=True)
    for team in coda_team:
        profile_image=team.image2
    for image in images:
        image_name=image
    
    if profile_image=="banner_page_v1":
        print("YES")
    else:
        print("NO")
        # print(image_name,"==",profile_image)

    context={
        "coda_team":coda_team,
        "title": "team",
        "profile_image": profile_image
        # "image_name": image_name
    }
    if sub_title == 'team':
        return render(request, "main/team.html",context)
    else:
        return render(request, "main/profiles.html",context)

class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields ="__all__"

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:team")

    def test_func(self):
        profile = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == profile.user:
            return True
        return False

def it(request):
    return render(request, "main/departments/it.html", {"title": "IT"})

def finance(request):
    return render(request, "main/departments/finance_landing_page.html", {"title": "Finance"})

# def finance(request):
#     return render(request, "finance\reports\finance.html", {"title": "Finance"})

def hr(request):
    return render(request, "management/companyagenda.html", {"title": "HR"})

@login_required
def meetings(request):
    emp_obj = User.objects.filter(
                                            Q(sub_category=3),
                                            Q(is_admin=True),
                                            Q(is_employee=True),
                                            Q(is_active=True),
                                            Q(is_staff=True),
                        ).order_by("-date_joined")
    # dept_obj = Department.objects.all().distinct()
    # departments=[dept.name for dept in dept_obj ]
    employees=[employee.first_name for employee in emp_obj ]
    # print(employees)
    _,rand_departments=task_assignment_random(employees)
    context={
        "departments": rand_departments,
        "employees": employees,
        "title": "Meetings",
        "meetings":Meetings,
    }
    return render(request, "main/departments/meetings.html",context)

class MeetingsUpdateView(LoginRequiredMixin,UpdateView):
    model=Meetings
    fields = "__all__"
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:meetings') 

def testing(request):
    return render(request, "main/testing.html", {"title": "testing"})
    
def interview(request):
    return redirect('data:interview')
    # return render(request, "main/coach_profile.html", {"title": "coach_profile"})

def coach_profile(request):
    return render(request, "main/coach_profile.html", {"title": "coach_profile"})

@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        message=f'Thank You, we will get back to you within 48 hours.'
        context={
            "message":message,
            # "link":SITEURL+'/management/companyagenda'
        }
        if form.is_valid():
            # form.save()
            instance=form.save(commit=False)
            # instance.client_name='admin',
            instance.task='NA',
            instance.plan='NA',
            instance.trained_by=request.user
            instance.save()
            # return redirect("management:assessment")
            return render(request, "main/errors/generalerrors.html",context)
    else:
        form = ContactForm()
    return render(request, "main/contact/contact_message.html", {"form": form})

def report(request):
    return render(request, "main/report.html", {"title": "report"})

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Assets
    success_url = "/images/"
    # fields = ["title", "description"]
    fields = ["name",'category', "description","image_url"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
def images(request):
    # images = Assets.objects.all().first()
    images = Assets.objects.all()
    # print(images)
    return render(request, "main/snippets_templates/static/images.html", {"title": "pay", "images": images})

class ImageUpdateView(LoginRequiredMixin,UpdateView):
    model=Assets
    fields = ['name','image_url','description']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:images') 


# def payment(request,method):
#     (phone_number,email_info,
#     email_dck,cashapp,
#     venmo,stan_account_no,
#     coda_account_no,dck_account_no)=payment_details()
#     path_value,sub_title=path_values(request)
#     subject='PAYMENT'
#     url='email/payment/payment_method.html'
#     message=f'Hi,{request.user.first_name}, an email has been sent \
#             with {sub_title} details for your payment.In the unlikely event\
#             that you have not received it, kindly \
#             check your spam folder.'
#     context={
#                 "title": "PAYMENT DETAILS",
#                 'user': request.user.first_name,
#                 "images":images, 
#                 "message": message,
#         }
#     try:
#         send_email( category=request.user.category, 
#                     to_email=[request.user.email,], 
#                     subject=subject, html_template=url, 
#                     context={
#                             'subtitle': sub_title,
#                             'user': request.user.first_name,
#                             'mpesa_number':phone_number,
#                             'cashapp':cashapp,
#                             'venmo':venmo,
#                             'stan_account_no':stan_account_no,
#                             'coda_account_no':coda_account_no,
#                             'dck_account_no':dck_account_no,
#                             'email':email_info,
#                             'email':email_dck,
#                             }
#                     )
#         return render(request, "main/errors/generalerrors.html",context)
#     except:
#         return render(request, "main/errors/500.html")


# @login_required
# def pay(request):
#     url="https://www.codanalytics.net/static/main/img/service-3.jpg"
#     message=f'Hi,{request.user}, you are yet to sign the contract with us kindly contact us at info@codanalytics.net'
#     link=f'{SITEURL}/finance/new_contract/{request.user}/'
#     images,image_names=image_view(request)
#     try:
#         payment_info = Payment_Information.objects.filter(
#             customer_id=request.user.id
#         ).first()
#         context={
#             "title": "PAYMENT", 
#             "images":images, 
#             "image_name": image_names, 
#             "payments": payment_info,
#             "message": message,
#             "link": link,
#         }
#         return render(request, "finance/payments/pay.html",context)
#     except:
#         # try:
#         #     payment_history=Payment_History.objects.filter(
#         #             Q(customer__username="admin")| 
#         #             Q(customer__username="coda_info") 
#         #             ).latest('id')
#         #     context={
#         #         "title": "PAYMENT", 
#         #         "images":images, 
#         #         "image_name": image_names, 
#         #         "payments": payment_history,
#         #         "message": message,
#         #         "link": link,
#         #     }
#         #     if request.user.category == 4 and request.user.sub_category == 6:
#         #         return render(request, "finance/payments/pay.html",context)
#         #     else:
#         #         return render(request, "finance/payments/pay.html",context)
#         # except :#payment_history.DoesNotExist as den:
#         return render(request, "management/contracts/contract_error.html", context)
        

# def paymentComplete(request):
#     payments = Payment_Information.objects.filter(customer_id=request.user.id).first()
#     # print(payments)
#     customer = request.user
#     body = json.loads(request.body)
#     # print("payment_complete:", body)
#     payment_fees = body["payment_fees"]
#     down_payment = payments.down_payment
#     studend_bonus = payments.student_bonus
#     plan = payments.plan
#     fee_balance = payments.fee_balance
#     payment_mothod = payments.payment_method
#     contract_submitted_date = payments.contract_submitted_date
#     client_signature = payments.client_signature
#     company_rep = payments.company_rep
#     client_date = payments.client_date
#     rep_date = payments.rep_date
#     Payment_History.objects.create(
#         customer=customer,
#         payment_fees=payment_fees,
#         down_payment=down_payment,
#         student_bonus=studend_bonus,
#         plan=plan,
#         fee_balance=fee_balance,
#         payment_method=payment_mothod,
#         contract_submitted_date=contract_submitted_date,
#         client_signature=client_signature,
#         company_rep=company_rep,
#         client_date=client_date,
#         rep_date=rep_date,
#     )

#     return JsonResponse("Payment completed!", safe=False)


def training(request):
    return render(request, "main/training.html", {"title": "training"})


def project(request):
    return render(request, "main/project.html", {"title": "project"})


# -----------------------------Documents---------------------------------
"""
def codadocuments(request):
    codadocuments=Codadoc.objects.all().order_by('-date_uploaded')
    return render(request, 'main/documentation.html', {'codadocuments': codadocuments})


def doc(request):
    if request.method== "POST":
        form=CodadocumentsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main-documents')
    else:
        form=CodadocumentsForm()
    return render(request, 'main/doc.html',{'form':form})
"""

# @shared_task(name="advertisement")
# def advertisement():
    # This function will post the latest Facebook Ad
    # context = Advertisement.objects.all().first()
    # # facebook_context = Advertisement.objects.all().first()
    # apiKey =context.twitter_api_key # '1zPxZNd57aXHZb8WwQFYEvNbv'  
    # apiSecret = context.twitter_api_key_secret # 'UdRcVGDSE9Ntpwz1Rbq3qsGPcYYBCor7Yl6X3wVLR5J6hKczmZ' 
    # accessToken = context.twitter_access_token # '1203036386011570177-rgXHzNM25WeUMnua6U13dS7jQmDgWg' 
    # accessTokenSecret =context.twitter_access_token_secret #'17cKoLwVdiZMnvKCWSxONCWj1A8atW6OvEAWtpqdUeZLF' 

    # 3. Create Oauth client and set authentication and create API object
    # oauth = tweepy.OAuthHandler(apiKey, apiSecret)
    # oauth.set_access_token(accessToken, accessTokenSecret)

    # api = tweepy.API(oauth)

    # 4. upload media
    # urllib.request.urlretrieve(
    # 'https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link',
    # "advertisement.png")
    # urllib.request.urlretrieve(
    # 'https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png',
    # "advertisement.png")
    # image = Image.open("advertisement.png")
    # image_path='https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link'
    # link = urllib.request.urlopen(image_path).read()
    # image = Image.open(r"https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link") 
    # This method will show image in any image viewer 
    # image.show() 
    # media=googledriveurl={{image.image_url}}
    # image=link
    # image='media/profile_pics/Chris.jpg'
    # image='https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link'
    
    
    # media = api.media_upload(image)

    # api.update_status(
    #     status=context.post_description,
    #     # media_ids=[context.tweet_media],
    #     media_ids=[media.media_id]
    # )

#     # facebook_page_id = facebook_context.facebook_page_id
#     # access_token = facebook_context.facebook_access_token
#     # url = "https://graph.facebook.com/{}/photos".format(facebook_page_id)
#     # msg = facebook_context.post_description
#     # image_location = facebook_context.image
#     # payload = {
#     #     "url": image_location,
#     #     "access_token": access_token,
#     #     "message": msg,
#     # }

#     # Send the POST request
#     # requests.post(url, data=payload)


class whatsappCreateView(LoginRequiredMixin, CreateView):
    model = Whatsapp
    success_url = "/whatsapplist/"  
    form_class=WhatsappForm
    # fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class whatsappUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Whatsapp
    form_class=WhatsappForm

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:whatsapp_list")

    def test_func(self):
        # plan = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False

def delete_whatsapp(request,id):
    whatsapp_record = Whatsapp.objects.get(pk=id)
    if request.user.is_superuser:
        whatsapp_record.delete()
    return redirect('main:whatsapp_list')


def whatsapp_apis(request):
    whatsaapitems=Whatsapp.objects.all()
    context={
            "whatsaapitems":whatsaapitems
    }
    return render(request, 'main/snippets_templates/table/whatsapp_apis.html',context)

def runwhatsapp(request):
    whatsaapitems=Whatsapp.objects.all()
    group_id=Whatsapp.objects.values_list('group_id',flat=True).first()
    # image_url=Whatsapp.objects.values_list('image_url',flat=True).first()
    message=Whatsapp.objects.values_list('message',flat=True).first()

    print("Groups====>",group_id)
    # group_id = "120363047226624982@g.us" #group_id #"14174137966-1445706887@g.us" #
    image_name = "image.jpg"
    screen_id=26504
    product_id='333b59c1-c310-43c0-abb5-e5c4f0379e61' #"6985f35e-b282-4316-91ef-83019d3e31c5"
    image ="https://www.codanalytics.net/static/main/img/service-3.jpg"
    # url = "https://api.maytapi.com/api/6985f35e-b282-4316-91ef-83019d3e31c5/26503/sendMessage"
    # url = "https://api.maytapi.com/api/6985f35e-b282-4316-91ef-83019d3e31c5/26503/sendMessage"
    url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"

    # payload = json.dumps({
    #   "to_number": group_id, #"120363047226624982@g.us", #'14174137966-1445706887@g.us', # 
    #   "type": "text",
    #   "message":  message # "this text message send"
    # })

    payload = json.dumps({
        "to_number": group_id,
        "type": "media",
        "message": image, #"this text message send", #image,
        "filename": image_name
    })

    headers = {
        'accept': 'application/json',
        'x-maytapi-key':'cce10961-db15-46e7-b5f1-6d6bf091b686', # 'b914dbd3-e225-48c0-bdbf-cbffa39ce44c',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    message=f'Hi,{request.user}, your messages have been post to your groups'
    context={
        'title':'WHATSAPP',
        'message':message
    }
    return render (request, "main/errors/generalerrors.html",context)
import requests
import os
import time
import http.client
import json
from django.db.models import Min,Max
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from celery import shared_task
from django.shortcuts import redirect, render
from django.contrib import messages
import calendar,string
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from .models import Service,Plan,Assets
from .utils import Meetings,image_view,path_values
from accounts.utils import employees
from codablog.models import Post,Testimonials
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
import http.client
import json
from coda_project.task import TrainingLoanDeduction
# from finance.utils import pay_info
# from django.core.management import call_command
# importing modules
import urllib.request
from PIL import Image
from django.contrib.auth import get_user_model
import random
import string
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

def template_errors(request):
    url = request.path
    contact = 'Please contact admin at info@codanalytics.net'
    title = ['Bad Request', 'Permission Denied', 'Page Not Found', 'System Issue']

    # Map each error code to its corresponding context
    context_dict = {
        400: {'title': title[0], 'error_message': 'Kindly check your URL/link provided', 'contact_message': contact},
        403: {'title': title[1], 'error_message': 'You are not allowed to visit this page', 'contact_message': contact},
        404: {'title': title[2], 'error_message': 'Page not found', 'contact_message': contact},
        500: {'title': title[3], 'error_message': 'There is an issue on our end. Please try again later.', 'contact_message': contact},
    }

    # Get the context based on the error code, or use a default context
    error_code = getattr(url, 'response', None)
    context = context_dict.get(error_code, {'title': 'Error', 'error_message': 'An error has occurred', 'contact_message': contact})

    print(error_code)
    return render(request, 'main/errors/template_error.html', context)


# def template_errors(request):
#     url=request.path
#     # if url.response.code=400
#     contact='Please Contact admin at info@codanalytics.net'
#     title=['Bad Request','Permission Denied','Page Not Found','System Issue']
#     if url.response.code==400:
#         context={
#                     'title':title[0],
#                     'message':'Kindly check your url/link provided',
#                     'message':contact,
#                  }
#     if url.response.code==403:
#         context={
#                     'title':title[1],
#                     'message':'You are not allowed to vist this page',
#                     'message':contact,
#                  }
#     if url.response.code==404:
#         context={
#                     'title':title[2],
#                     'message':'Please contact admin at info@codanalytics.net',
#                     'message':contact,
#                  }
        
#     if url.response.code==500:
#         context={
#                     'title':title[3],
#                     'message':'There is an issue on our end Please Try again later',
#                     'message':contact,
#                  }
#     print(url.response.code)
#     return render(request,'main/errors/generalerrors.html',context)



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

from django.shortcuts import get_object_or_404



def layout(request):
    latest_posts = Testimonials.objects.values('writer').annotate(latest=Max('date_posted')).order_by('-latest')
    testimonials = []
    for post in latest_posts:
        writer = post['writer']
        #querying for the latest post
        user_profile = UserProfile.objects.filter(user=writer,user__is_client=True).first()
        # user_profile = UserProfile.objects.filter(user=writer).first()
        if user_profile:
            latest_post = Testimonials.objects.filter(writer=writer, date_posted=post['latest']).first()
            testimonials.append(latest_post)

    for post in testimonials:
        print("title",post.title)
        # print("image",post.writer.profile.image2.image_url)
        # print("image",post.writer.profile.img_url)
    services = Service.objects.all()
    images, image_names = image_view(request)
    context = {
        "images": images,
        "image_names": image_names,
        "services": services,
        "posts": testimonials,
        "title": "layout",
    }
    return render(request, "main/home_templates/newlayout.html", context)




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


# =====================SERVICE VIEWS=======================================
class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    success_url = "/services/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def services(request):
    services = Service.objects.filter(is_active=True).order_by('serial')
    context = {
        "SITEURL" :settings.SITEURL,
        "services": services
    }
    return render(request, "main/services.html", context)


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields ="__all__"

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:services")

    def test_func(self):
        service = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == service.staff:
            return True
        return False

def delete_service(request,id):
    service = service.objects.get(pk=id)
    if request.user.is_superuser:
        service.delete()
    return redirect('main:services')



def about(request):
    team_members = UserProfile.objects.filter(user__is_employee=True,user__is_active=True,user__is_staff=True)
    sub_title=path_values(request)[-1]
    date_object="01/20/2023"
    start_date = datetime.strptime(date_object, '%m/%d/%Y')
    end_date=start_date + relativedelta(months=3)
    images,image_names=image_view(request)
    staff=[member for member in team_members if member.img_category=='employee']
    img_urls=[member.img_url for member in team_members if member.img_category=='employee']
    context={
        "start_date": start_date,
        "end_date": end_date,
        "title_team": "team",
        # "employee_subcategories": employee_subcategories,
        "active_employees": staff,
        "title_about": "about",
        # "images": images,
        "img_urls": img_urls,
        "title_letter": "letter",
    }
    if sub_title == 'team':
        return render(request, "main/team.html",context)
    elif sub_title == 'letter':
        return render(request, "main/doc_templates/letter.html",context)
    elif sub_title == 'appointment_letter':
        return render(request, "main/doc_templates/appointment_letter.html",context)
    elif sub_title == 'about':
        return render(request, "main/about.html",context)
    

class UserCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    success_url = "/team/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# def profiles(request):
#     sub_title=path_values(request)[-1]
#     images = Assets.objects.values_list('name', flat=True)
#     team_members = UserProfile.objects.filter(user__is_employee=True,user__is_active=True,user__is_staff=True)
#     print(team_members)
#     for team in team_members:
#         profile_image=team.image2
#         profile_image_category=team.img_category 
#         profile_image_image_url=team.img_url

#         print(profile_image,profile_image_category,profile_image_image_url)
#     # for image in images:
#     #     image_name=image
    
#     # if profile_image=="banner_page_v1":
#     #     print("YES")
#     # else:
#     #     print("NO")
#     #     # print(image_name,"==",profile_image)

#     context={
#         "team_members":team_members,
#         "title": "team",
#         "profile_image": profile_image
#         # "image_name": image_name
#     }
#     if sub_title == 'team':
#         return render(request, "main/team.html",context)
#     else:
#         return render(request, "main/profiles.html",context)


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    # fields ="__all__"
    fields=['position','description','image','image2','is_active','laptop_status']
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("management:companyagenda")

    def test_func(self):
        # profile = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
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
    fields = ['category','name','image_url','description']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:images') 


def training(request):
    return render(request, "main/training.html", {"title": "training"})


def project(request):
    return render(request, "main/project.html", {"title": "project"})


def market(request):
    path,sub_title=path_values(request)
    print("path",path,sub_title)
    if sub_title=='trainingad':
        return render(request, "main/snippets_templates/marketing/trainingad.html", {"title": "project"})
    if sub_title=='market':
        return render(request, "main/snippets_templates/marketing/marketing.html", {"title": "project"})


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
    whatsapp_items = Whatsapp.objects.all()
    image_url = None
    # Get a list of all group IDs from the Whatsapp model
    # group_ids = list(whatsapp_items.values_list('group_id', flat=True))
    group_ids = list(whatsapp_items.values_list('group_id', flat=True))
    # group_ids = ["120363047226624982@g.us"]

    # Get the image URL and message from the first item in the Whatsapp model
    if whatsapp_items:
        image_url = whatsapp_items[0].image_url
        message = whatsapp_items[0].message
    else:
        message = "local testing"
    product_id = whatsapp_items[0].product_id
    screen_id = whatsapp_items[0].screen_id
    token = whatsapp_items[0].token
    # product_id = os.environ.get('MYAPI_PRODUCT_ID')
    # screen_id = os.environ.get('MYAPI_SCREEN_ID')
    # token = os.environ.get('MYAPI_TOKEN_ID')

    # print("Group IDs:", group_ids)
    # print("Image URL:", image_url)
    # print("Message:", message)
    print("product_id:", product_id)
    print("screen_id:", screen_id)
    print("token:", token)

    # Loop through all group IDs and send the message to each group
    for group_id in group_ids:
        print("Sending message to group", group_id)

        # Set the message type to "text" or "media" depending on whether an image URL is provided
        conn = http.client.HTTPSConnection("api.maytapi.com")
        if image_url:
            # Set the length of the random string
            length = 10
            # Generate a random string of lowercase letters and digits
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            payload = json.dumps({
                "to_number": group_id,
                "type": "media",
                "message": image_url,
                "filename": random_string
            })
        else:
            payload = json.dumps({
                "to_number": group_id,
                "type": "text",
                "message": message
            })

        headers = {
            'accept': 'application/json',
            'x-maytapi-key': token,
            'Content-Type': 'application/json'
        }
        conn.request("POST", f"/api/{product_id}/{screen_id}/sendMessage", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        # Check if the API request was successful
        # if response.status_code == 200:
        if json.loads(data).get('success') is True:
            print("Message sent successfully!")
            message = f"Hi, {request.user}, your messages have been sent to your groups."
        else:
            # print("Error sending message:", response.text)
            message = data

        # time.sleep(5) # add a delay of 1 second

    # Display a success message on the page
    # message = f"Hi, {request.user}, your messages have been sent to your groups."
    context = {"title": "WHATSAPP", "message": message}
    return render(request, "main/errors/generalerrors.html", context)
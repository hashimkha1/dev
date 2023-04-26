import requests
import json
import datetime
import time
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.db.models import Q
from celery import shared_task
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from .models import Service,Plan,Assets
from .utils import Meetings,path_values,buildmodel
from accounts.utils import employees
from .models import Testimonials
from management.models import Advertisement
from coda_project.task import advertisement
from coda_project import settings
from application.models import UserProfile
from management.utils import task_assignment_random
from management.models import Whatsapp
from main.forms import WhatsappForm,PostForm,ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        CreateView,
        DeleteView,
        ListView,
        DetailView,
        UpdateView,
    )
from accounts.forms import LoginForm
from .forms import *
from accounts.views import CreateProfile
from coda_project.task import TrainingLoanDeduction
import urllib.request
from PIL import Image
from django.contrib.auth import get_user_model
User=get_user_model()





#  ===================================================================================   
def test(request):
    return render(request, "main/test.html", {"title": "test"})

def checkout(request):
    return render(request, "main/checkout.html", {"title": "checkout"})



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
#===============Processing Images from Database==================

def layout(request):
    images= Assets.objects.all()
    image_names=Assets.objects.values_list('name',flat=True)
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

    services = Service.objects.all()
    context = {
        "images": images,
        "image_names": image_names,
        "services": services,
        "posts": testimonials,
        "title": "layout",
    }
    return render(request, "main/home_templates/newlayout.html", context)




# =====================TESTIMONIALS  VIEWS=======================================
@login_required
def newpost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.writer = request.user
            form.save()
            return redirect('main:layout')
    else:
        form = PostForm()
        quest = "write 3 full paragraphs each on how good my data analyst coach was" # pick a question bunch of questions

        response = buildmodel(question=quest)
        context={
            "response" : response,
            "form": form
        }
        # form.instance.description = buildmodel(question=quest)
        print("response",response)
    return render(request, "main/testimonials/newpost.html", context)

class PostListView(ListView):
    model=Testimonials
    template_name='main/testimonials/success.html'
    context_object_name='posts'
    ordering=['-date_posted']

class PostDetailView(DetailView):
    model=Testimonials
    ordering=['-date_posted']


class PostDetailSlugView(DetailView):
    queryset = Testimonials.objects.all()
    template_name = "main/post_detail.html"
 
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailSlugView, self).get_context_data(*args, **kwargs)
        return context
 
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
 
        #instance = get_object_or_404(Post, slug=slug, active=True)
        try:
            instance = Testimonials.objects.get(slug=slug, active=True)
        except Testimonials.DoesNotExist:
            raise Http404("Not found..")
        except Testimonials.MultipleObjectsReturned:
            qs = Testimonials.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Testimonials
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Testimonials
    success_url="/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# =====================DC_KENYA VIEWS=======================================
# =====================DC_KENYA VIEWS=======================================
def dclayout(request):
    # advertisement()
    
    posts=Testimonials.objects.all()
    services=Service.objects.all()

    context={
            "services":services,
            "posts":posts,
            "title": "DCKENYA"
        }
    return render(request, "main/dc48kenya/dc_layout.html",context)


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
    images= Assets.objects.all()
    image_names=Assets.objects.values_list('name',flat=True)
    team_members = UserProfile.objects.filter(user__is_employee=True,user__is_active=True,user__is_staff=True)
    sub_title=path_values(request)[-1]
    date_object="01/20/2023"
    start_date = datetime.strptime(date_object, '%m/%d/%Y')
    end_date=start_date + relativedelta(months=3)
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


# -----------------------------Documents---------------------------------

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


# def runwhatsapp(request):
#     # whatsapp_items = Whatsapp.objects.all()
#     group_ids = Whatsapp.objects.values_list('group_id', flat=True)
#     image_url = Whatsapp.objects.values_list('image_url', flat=True).first()
#     message = Whatsapp.objects.values_list('message', flat=True).first()

#     print("Groups====>", group_ids, image_url, message)

#     image_name = "image.jpg"
#     screen_id = 26504
#     product_id = '333b59c1-c310-43c0-abb5-e5c4f0379e61'
#     image = image_url
#     url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"

#     payload = json.dumps({
#         "type": "media",
#         "message": image,
#         "filename": image_name
#     })


#     headers = {
#         'accept': 'application/json',
#         'x-maytapi-key':'cce10961-db15-46e7-b5f1-6d6bf091b686',
#         'Content-Type': 'application/json'
#     }

#     for group_id in group_ids:
#         payload_data = json.loads(payload)
#         payload_data['to_number'] = group_id
#         payload_data['type'] = 'media' if image else 'text'
#         payload_data['message'] = image if image else message

#         response = requests.request("POST", url, headers=headers, data=json.dumps(payload_data))
#         print(response.text)

#     message = f'Hi, {request.user}, your messages have been posted to your groups.'
#     context = {
#         'title': 'WHATSAPP',
#         'message': message
#     }
#     return render(request, "main/errors/generalerrors.html", context)


def runwhatsapp(request):
    whatsapp_items = Whatsapp.objects.all()

    # Get a list of all group IDs from the Whatsapp model
    group_ids = list(whatsapp_items.values_list('group_id', flat=True))

    # Get the image URL and message from the first item in the Whatsapp model
    image_url = whatsapp_items[0].image_url
    message = whatsapp_items[0].message
    product_id = whatsapp_items[0].product_id
    screen_id = whatsapp_items[0].screen_id
    token = whatsapp_items[0].token

    # print("Group IDs:", group_ids)
    # print("Image URL:", image_url)
    # print("Message:", message)
    # print("product_id:", product_id)
    # print("screen_id:", screen_id)
    # print("token:", token)

    # Loop through all group IDs and send the message to each group
    for group_id in group_ids:
        print("Sending message to group", group_id)

        # Set the message type to "text" or "media" depending on whether an image URL is provided
        if image_url:
            message_type = "media"
            message_content = image_url
            filename = "image.jpg"
        else:
            message_type = "text"
            message_content = message
            filename = None

        # Set up the API request payload and headers
        payload = {
            "to_number": group_id,
            "type": message_type,
            "message": message_content,
            "filename": filename,
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-maytapi-key": token,
        }
        # Send the API request and print the response
        url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        # print(response.status_code)
        # print(response.text)
        # print(url)

        # Check if the API request was successful
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Error sending message:", response.text)

        # time.sleep(5) # add a delay of 1 second

    # Display a success message on the page
    message = f"Hi, {request.user}, your messages have been sent to your groups."
    context = {"title": "WHATSAPP", "message": message}
    return render(request, "main/errors/generalerrors.html", context)


def error400(request):
    return render(request, "main/errors/400.html", {"title": "400Error"})

def error403(request):
    return render(request, "main/errors/403.html", {"title": "403Error"})

def error404(request):
    return render(request, "main/errors/404.html", {"title": "404Error"})
    
def error500(request):
    return render(request, "main/errors/500.html", {"title": "500Error"})

def general_errors(request):
    # return render(request, "main/errors/noresult.html")
    context={'message':'message'}
    return render(request,'main/errors/generalerrors.html',context)

#  ===================================================================================   
def add_availability(request):
    context = {}
    if request.method == "POST":
        form = ClientAvailabilityForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = request.user
            instance.save()
            form = ClientAvailabilityForm()
    else:
        form = ClientAvailabilityForm()
    return render(request, "main/availability/add_availability.html", {"form": form, "context": context})


def my_availability(request):
    context = {}
    dist = {}
    try:
        availability = ClientAvailability.objects.filter(client=request.user).order_by('-id')
        for obj in availability:
            today = datetime.today()
            day_dif = abs(today.weekday()-int(obj.day))
            date = today.replace(day=(today.day+day_dif))
            day = date.strftime("%A")
            print(day)
            print(date)

            dist[obj] = {'date': date, 'day': day}
    except:
        availability = None
    context['obj'] = dist

    return render(request, "main/availability/my_availability.html", {"context": context})


def clints_availability(request):
    context = {}
    availability = None
    dist = {}
    if request.method == "POST":
        form = ClientNameForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            availability = ClientAvailability.objects.filter(client=client).order_by('-id')
            for obj in availability:
                today = datetime.today()
                day_dif = abs(today.weekday() - int(obj.day))
                date = today.replace(day=(today.day + day_dif))
                day = date.strftime("%A")
                dist[obj] = {'date': date, 'day': day}
    else:
        form = ClientNameForm()

    context['obj'] = dist
    return render(request, "main/availability/client_availability.html", {"form": form, "context": context})
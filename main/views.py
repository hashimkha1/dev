import requests
import json
import datetime
import time
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from .models import Service,Plan,Assets
from .utils import Meetings,path_values,buildmodel,team_members,client_categories
from .models import Testimonials
from coda_project import settings
from application.models import UserProfile
from management.utils import task_assignment_random
from management.models import Whatsapp
from main.forms import PostForm,ContactForm
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
from .forms import *
from PIL import Image
from django.contrib.auth import get_user_model
User=get_user_model()





#  ===================================================================================   


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

def data_policy(request):
    return render(request, "main/datapolicy.html", {"title": "Data Policy"})

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
    services = Service.objects.filter(is_active=True).order_by('serial')
    # services = Service.objects.all()
    context = {
        "images": images,
        "image_names": image_names,
        "services": services,
        "posts": testimonials,
        "title": "layout",
    }
    return render(request, "main/home_templates/newlayout.html", context)

# =====================SERVICES  VIEWS=======================================
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
    return render(request, "main/services/show_service.html", context)

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


def display_service(request,*args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        service_shown = Service.objects.all()
    except Service.DoesNotExist:
        return redirect('main:display_service')

    service_category_slug = next((x.slug for x in service_shown if sub_title == x.slug), None)
    service_category_title = next((x.title for x in service_shown if sub_title == x.slug), None)
    service_description = next((x.description for x in service_shown if sub_title == x.slug), None)
    service_id = next((x.id for x in service_shown if sub_title == x.slug), None)

    service_categories = ServiceCategory.objects.filter(service=service_id)

    for cat in service_categories:
        print("cat=====>",cat)

    print(service_category_slug,service_category_title,service_id)

    context = {}  # Initialize context with an empty dictionary
    context = {
        'service_categories': service_categories,
        "title": service_category_title,
        "service_desc": service_description,
        "slug":service_category_slug
    }
    return render(request, "main/services/show_service.html", context)

# def display_service(request,*args, **kwargs):
#     path_list, sub_title, pre_sub_title = path_values(request)
#     data_analysis = Service.objects.get(slug='data_analysis')
#     investing = Service.objects.get(slug='investing')
#     data_analysis_categories = ServiceCategory.objects.filter(service=data_analysis.id)
#     investing_categories = ServiceCategory.objects.filter(service=investing.id)
    
#     context = {}  # Initialize context with an empty dictionary
#     print()
#     if sub_title == data_analysis.slug:
#         context = {
#             'services': data_analysis_categories,
#             "title": data_analysis.title,
#             "service_desc": data_analysis.description,
#             "slug":data_analysis.slug
#         }
#     elif sub_title == investing.slug:
#         context = {
#             'services': investing_categories,
#             "title": investing.title,
#             "service_desc": investing.description,
#         }
#     return render(request, "main/services/show_service.html", context)


def service_plans(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        if pre_sub_title:
            service_shown = Service.objects.get(slug=pre_sub_title)
        else:
            return redirect('main:display_service')
    except Service.DoesNotExist:
        return redirect('main:display_service')
    context = {}  # Initialize context with an empty dictionary

    service_categories = ServiceCategory.objects.filter(service=service_shown.id)
    category_slug = next((x.slug for x in service_categories if sub_title == x.slug), None)
    category_name = next((x.name for x in service_categories if sub_title == x.slug), None)
    category_id = next((x.id for x in service_categories if sub_title == x.slug), None)
    plans = Pricing.objects.filter(category=category_id)

    context = {
        "SITEURL": settings.SITEURL,
        "title": category_name,
        "category_slug": category_slug,
        "services": plans
    }
    return render(request, "main/services/service_plan.html", context)

def service_plans(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        if pre_sub_title:
            service_shown = Service.objects.get(slug=pre_sub_title)
        else:
            return redirect('main:services')
    except Service.DoesNotExist:
        return redirect('main:services')

    service_categories = ServiceCategory.objects.filter(service=service_shown.id)
    category_slug = next((x.slug for x in service_categories if sub_title == x.slug), None)
    category_name = next((x.name for x in service_categories if sub_title == x.slug), None)
    category_id = next((x.id for x in service_categories if sub_title == x.slug), None)
    plans = Pricing.objects.filter(category=category_id)

    context = {
        "SITEURL": settings.SITEURL,
        "title": category_name,
        "subcatslug":category_slug,
        "services": plans
    }
    return render(request, "main/services/service_plan.html", context)


# def job_support(request):
#     job_support = ServiceCategory.objects.get(name__iexact='Job Support')
#     plans = Pricing.objects.filter(category=job_support.id)
    
#     context={
#         "SITEURL" :settings.SITEURL,
#         "title":job_support.name,
#         # "service_desc":job_support.description,
#         'services': plans
#     }
#     # return render(request, "main/services/job_support.html", context)
#     return render(request, "main/services/full_course.html", context)


# def full_course(request):
#     full_course = ServiceCategory.objects.get(name__iexact='Full Course')
#     plans = Pricing.objects.filter(category=full_course.id)
#     # return render(request, "main/services/job_support.html", {'services': plans})
#     context={
#         "SITEURL" :settings.SITEURL,
#         "title":full_course.name,
#         # "service_desc":job_support.description,
#         'services': plans
#     }
#     return render(request, "main/services/full_course.html", context)


@login_required
def job_market(request):
    return render(request, "data/training/job_market.html")

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
        print("HERE")
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

#========================Internal Team & Clients==============================
def team(request):
    path_list, sub_title, pre_sub_title = path_values(request)
    team_members_staff = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__sub_category=1).order_by("user__date_joined")
    team_members_agents = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__sub_category=3).order_by("user__date_joined")
    team_members_trainees = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__category=2, user__sub_category=4).order_by("user__date_joined")
    clients_job_seekers = UserProfile.objects.filter(user__is_client=True, user__is_active=True).exclude(user__sub_category=4).order_by("user__date_joined")
    clients_job_support = UserProfile.objects.filter(user__is_client=True, user__sub_category=4, user__is_active=True).order_by("user__date_joined")

    if sub_title == 'team_profiles':
        team_categories = {
        'Lead Team': list(team_members_staff),
        'Support Team': list(team_members_agents),
        'Trainee Team': list(team_members_trainees),
        }
        user_group=team_members
        heading="THE BEST TEAM IN ANALYTICS"
    if sub_title == 'client_profiles':
        team_categories = {
        'Job Seekers': list(clients_job_seekers),
        'Job Support': list(clients_job_support),
        }
        user_group=client_categories
        heading="EXPERTS FOR DATA ANALYTICS/SCIENCE"

    context = {
        "team_categories": team_categories,
        "team_members": user_group,
        "title":heading
    }
    return render(request, "main/team_profiles.html", context)


#========================Internal documents==============================  
def letters(request):
    path_list,sub_title,pre_sub_title=path_values(request)
    date_object="01/20/2023"
    start_date = datetime.strptime(date_object, '%m/%d/%Y')
    end_date=start_date + relativedelta(months=3)
    context={
        "start_date": start_date,
        "end_date": end_date,
        "title_letter": "letter",
    }

    if sub_title == 'letter':
        return render(request, "main/doc_templates/letter.html",context)
    if sub_title == 'appointment_letter':
        return render(request, "main/doc_templates/appointment_letter.html",context)
    

def about(request):
    images= Assets.objects.all()
    image_names=Assets.objects.values_list('name',flat=True)
    team_members = UserProfile.objects.filter(user__is_staff=True,user__is_active=True)
    path_list,sub_title,pre_sub_title=path_values(request)
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
    success_url = "/team_profiles/"
    fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    # fields ="__all__"
    fields=['position','description','image','image2','is_active','laptop_status']
    def form_valid(self, form):
        # form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:team_profiles")

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
                                            # Q(sub_category=3),
                                            Q(is_admin=True),
                                            Q(is_active=True),
                                            Q(is_staff=True),
                        ).order_by("-date_joined")
    employees=[employee.first_name for employee in emp_obj ]
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
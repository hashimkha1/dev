import webbrowser
import datetime, json
import random
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.shortcuts import redirect, render,get_object_or_404
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
import openai
from django.db.models import Sum
from data.models import ClientAssessment
from investing.models import InvestmentContent
from .models import Service,Plan,Assets,Testimonials
from .utils import (Automation, General, Meetings,path_values,buildmodel,team_members,future_talents,board_members, url_mapping,
                    client_categories,service_instances,service_plan_instances,reviews,packages,courses,
                    generate_database_response,generate_chatbot_response,upload_image_to_drive, langchainModelForAnswer)
from coda_project import settings
from application.models import UserProfile
from management.utils import task_assignment_random
from management.models import TaskHistory
from accounts.models import Team_Members
from main.forms import PostForm,ContactForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        CreateView,
        DeleteView,
        ListView,
        DetailView,
        UpdateView,)

from .forms import *
from django.http import JsonResponse
from django.apps import apps
# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from django.db.models import F, FloatField, Case, When, Value, Subquery, OuterRef, Q
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
from management.models import Requirement, Training
from data.models import ClientAssessment
from getdata.models import Editable
from investing.views import get_or_create_investment_content

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

def get_testimonials():
    count_to_class = {
        2: "col-md-6",
        3: "col-md-4",
        4: "col-md-3"
    }
    latest_posts = Testimonials.objects.values('writer').annotate(latest=Max('date_posted')).order_by('-latest')
    testimonials = []
    for post in latest_posts:
        writer = post['writer']
        user_profile = UserProfile.objects.filter(user=writer, user__is_client=True).first()
        if user_profile:
            latest_post = Testimonials.objects.filter(writer=writer, date_posted=post['latest']).first()
            testimonials.append(latest_post)

    number_of_testimonials = len(testimonials)
    selected_class = count_to_class.get(number_of_testimonials, "default-class")

    return testimonials, selected_class


def layout(request):
    testimonials, selected_class = get_testimonials()

    services = Service.objects.filter(is_active=True).order_by('serial')
    context = {
        "services": services,
        "posts": testimonials,
        "title": "layout",
        "selected_class": selected_class,
    }
    return render(request, "main/home_templates/newlayout.html", context)

def fetch_model_table_names(request):
    app_name = request.GET.get('category', None)  # Replace with the actual app name
    app_models = apps.get_app_config(app_name).get_models()
    # Get the actual model table names based on the application
    # table_names = [model.__name__ for model in app_models]
    table_names = [{'value': model.__name__, 'display_text': model._meta.verbose_name.replace('_', ' ').capitalize()} for model in app_models]
    return JsonResponse({'model_table_names': table_names})


# =====================TESTIMONIALS  VIEWS=======================================
# @login_required
# def search(request):
#     instructions = [
#         {"topic": "Review", "description": "Select Your User Category."},
#         {"topic": "Sample", "description": "Select Topic Category"},
#         {"topic": "copy", "description": "Enter topic-related question"},
#         {"topic": "Submit", "description": "Click on Submit Review!"},
#     ]
#     values = ["management", "investing", "main", "getdata", "data", "projectmanagement"]

#     if request.method == "POST":
#         form = SearchForm(request.POST, request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data
#             instance = form.save(commit=False)
#             instance.searched_by = request.user
#             category = form.instance.category
#             table = form.instance.topic
#             # print('table============',table)
#             question = form.instance.question
#             app = category
#             result, = generate_database_response(user_message=question, app=app,table=table)
#             if result:
#                 # This one is simple hu
#                 # llm = OpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
#                 chat_model = ChatOpenAI(openai_api_key='OPENAI_API_KEY')
#                 messages = [HumanMessage(content=str(result))]
#                 # response_llm = llm.predict_messages(messages)
#                 chat_model_result = chat_model.predict_messages(messages)
#                 # response1 = response_llm.content.split(':', 1)[-1].strip()
#                 response = chat_model_result.content
#             else:
#                 response = None

#             context = {
#                 "values": values,
#                 "instructions": instructions,
#                 "response": response,
#                 "form": form
#             }

#         return render(request, "main/snippets_templates/search.html", context)
#     else:
#         form = SearchForm()
#         context = {
#             "values": values,
#             "instructions": instructions,
#             "form": form
#         }
#         return render(request, "main/snippets_templates/search.html", context)

@login_required
def search(request):

    instructions = [
        {"topic": "Review", "description": "Select Your User Category."},
        {"topic": "Sample", "description": "Select Topic Category"},
        {"topic": "copy", "description": "Enter topic-related question"},
        {"topic": "Submit", "description": "Click on Submit Review!"},
    ]
    values = ["management", "investing", "main", "getdata", "data", "projectmanagement"]

    if request.method == "POST":
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.instance
            instance.searched_by = request.user
            question = instance.question + f"and for more context, try to refer {instance.topic} table in {instance.category} category first."
            response = langchainModelForAnswer(question)

            instance.save()
        else:
            response = 'form is invalid'
        
        context = {
            "values": values,
            "instructions": instructions,
            "response": response,
            "form": form
        }
        return render(request, "main/snippets_templates/search.html", context)
    else:
        form = SearchForm()
        context = {
            "values": values,
            "instructions": instructions,
            "form": form
        }
        return render(request, "main/snippets_templates/search.html", context)

def get_respos(request):
    user_message = request.GET.get('userMessage', '')  # Get the user's message from the request
    general_use = request.GET.get('generalUse', False)
    # import pdb; pdb.set_trace()
    if not user_message:
        return JsonResponse({'response': 'Invalid user message'})
    try:
        if not general_use:
            database_response = generate_database_response(user_message)
            if database_response:
                # chat_model = ChatOpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
                llm = OpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
                messages = [HumanMessage(content=str(database_response))]
                response_llm = llm.predict_messages(messages)
                # chat_model_result = chat_model.predict_messages(messages)
                return JsonResponse({'response': response_llm.content})
            
        chatbot_response = generate_chatbot_response(user_message)
        if chatbot_response:
            return JsonResponse({'response': chatbot_response})
        else:
            contact_model = DSU.objects.filter(challenge=user_message).first()
            if not contact_model:
                form = ContactForm(request.POST, request.FILES)
                dsu_instance = form.save(commit=False)
                dsu_instance.trained_by=request.user
                dsu_instance.task='NA',
                dsu_instance.plan='NA',
                dsu_instance.challenge = user_message
                dsu_instance.save()
                return JsonResponse({'response': "Oops! It seems I haven't learned that one yet, but don't worry. Our team will get back to you shortly with the information you need. Thanks for your patience!"})
            else:
                return JsonResponse({'response': str(contact_model.task)})
         
    except Exception as e:
        # Handle exceptions and return an appropriate JSON response
        return JsonResponse({'error': str(e)})


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
    
class PriceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pricing
    fields ="__all__"

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("main:services")

    def test_func(self):
        # service = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

def delete_service(request,id):
    service = service.objects.get(pk=id)
    if request.user.is_superuser:
        service.delete()
    return redirect('main:services')


def display_service(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        service_shown = Service.objects.all()
    except Service.DoesNotExist:
        return redirect('main:display_service')

    (service_category_slug, service_category_title, service_description,service_sub_titles, service_id) = service_instances(service_shown, sub_title)
    service_categories = ServiceCategory.objects.filter(service=service_id)
    try:
        asset = Assets.objects.get(name=service_category_title)
        asset_image_url = asset.service_image.url
    except Assets.DoesNotExist:
        asset_image_url = None
    investment_content = InvestmentContent.objects.first()

    description = investment_content.description if investment_content else "No description available"

    testimonials, selected_class = get_testimonials()

    # Calculate the number of students and other users
    students_count = CustomerUser.objects.filter(category=CustomerUser.Category.Student).count()
    teachers_count = CustomerUser.objects.filter(category=CustomerUser.Category.Coda_Staff_Member).count()
    # Calculate the total number of courses
    total_courses_count = ServiceCategory.objects.filter(service=service_id).count()
  
    category_name = 'website Development'  
    projects = Pricing.objects.filter(category__name=category_name, is_active=True)

    context = {
        'service_categories': service_categories,
        "title": service_category_title,
        "service_desc": service_description,
        'content': description,
        "General":General,
        "projects": projects,
        "Automation":Automation,
        "sub_titles": service_sub_titles,
        "posts": testimonials,
        "selected_class": selected_class,
        "slug": service_category_slug,
        "asset_image_url": asset_image_url,
        "students_count": students_count,
        "teachers_count": teachers_count,
        "total_courses_count": total_courses_count,
    }
    return render(request, "main/services/show_services.html", context)




def service_plans(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        if pre_sub_title == 'bigdata':
            service_shown = ServiceCategory.objects.get(slug=sub_title).service

        elif pre_sub_title:
            service_shown = Service.objects.get(slug=pre_sub_title)
            # print("service_shown====>",service_shown)

        elif sub_title.lower() in ["job-support","interview","full-course"]:
            # service_shown = Data Analysis
            service_shown = Service.objects.get(slug="data_analysis")
            # print("service_shown====>",service_shown)
        else:
            return redirect('main:layout')
        
    except Service.DoesNotExist:
        return redirect('main:display_service', slug ='data_analysis')
    except Exception:
        return redirect('main:layout')
    service_categories = ServiceCategory.objects.filter(service=service_shown.id)
    (category_slug,category_name,category_id)=service_plan_instances(service_categories,sub_title)
    plans = Pricing.objects.filter(category=category_id)

    context = {}
    context = {
        "SITEURL": settings.SITEURL,
        "title": category_name,
        "packages": packages,
        "category_slug": category_slug,
        "courses": courses,
        "services_plans": plans
    }
    return render(request, "main/services/service_plan.html", context)

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
        topics = ['Project Manager', 'Business Analysis', 'Data Analyst']

        # Randomly select a title from the list
        selected_title = random.choice(topics)
        user_message = f"write a full paragraph on how good/great coaches/trainers of {selected_title} in CODA were?" # pick a question bunch of questions
        # result = buildmodel(question=quest)
        result = generate_chatbot_response(user_message)

        if result is None:
            selected_review = random.choice(reviews)
            selected_description = selected_review["description"]
            response=selected_description
        else:
            response=result
        context={
            "response" : response,
            "form": form
        }
    return render(request, "main/testimonials/newpost.html", context)

class PostListView(ListView):
    model = Testimonials
    template_name = 'main/testimonials/reviews.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2  # This will ensure only 3 posts are retrieved

    def get_queryset(self):
        return super().get_queryset()[:2]
    
class PostDetailView(DetailView):
    model=Testimonials
    template_name='main/testimonials/post_detail.html'
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
    fields=['writer','title','content']

    def form_valid(self,form):
        # form.instance.writer=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("main:success")
    
    def test_func(self):
        post = self.get_object()
        if self.request.user.is_superuser or self.request.user == post.writer:
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
    
@login_required
def plans(request):
    day_name = date.today().strftime("%A")
    plans = Plan.objects.filter(is_active=True)
    plan_categories_list = Plan.objects.values_list(
                    'category', flat=True).distinct()
    plan_categories=sorted(plan_categories_list)
    for plan in plans:
        delivery_date=plan.created_at +  timedelta(days=plan.duration*30)
    context = {
        "plans": plans,
        "plan_categories": plan_categories,
        "delivery_date": delivery_date,
        "day_name": day_name,
        "message": "You are not a super user",

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


@login_required
def open_urls(request, url_type):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        # Try to use Chrome
        chrome_browser = webbrowser.get("chrome")
        browser = chrome_browser
    except webbrowser.Error:
        # Fallback to the default browser
        browser = webbrowser

    # Get the URLs for the given sub_title
    urls = url_mapping.get(sub_title, [])

    # Open each URL in the default web browser
    for url in urls:
        browser.open(url, new=1)
        # webbrowser.open(url)
    
    return render(request,"main/errors/generalerrors.html")

@login_required
def plan_urls(request):
    day_name = date.today().strftime("%A")
    open_urls= Plan.objects.filter(category="Work",is_active=True)
    plan_categories_list = Plan.objects.values_list(
                    'category', flat=True).distinct()
    plan_categories=sorted(plan_categories_list)
    for plan in open_urls:
        delivery_date=plan.created_at +  timedelta(days=plan.duration*30)
    context = {
        "plans": open_urls,
        "plan_categories": plan_categories,
        "delivery_date": delivery_date,
        "day_name": day_name,
    }
    if request.user.is_superuser:
        return render(request, "main/open_urls.html", context)
    else:
        return render(request, "main/errors/404.html", context)




#========================Internal Team & Clients==============================

# def team(request):
#     count_to_class = {
#         2: "col-md-6",
#         3: "col-md-4",
#         4: "col-md-3"
#     }
    
#     path_list, sub_title, pre_sub_title = path_values(request)
#     team_members_staff = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__sub_category=1).order_by("user__date_joined")
#     team_members_agents = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__sub_category=2).order_by("user__date_joined")
#     team_members_senior_trainees = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__category=2, user__sub_category=5).order_by("user__date_joined")
#     team_members_junior_trainees = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__category=2, user__sub_category=4).order_by("user__date_joined")
#     clients_job_seekers = UserProfile.objects.filter(user__is_client=True, user__is_active=True).exclude(user__sub_category=4).order_by("user__date_joined")
#     clients_job_support = UserProfile.objects.filter(user__is_client=True, user__sub_category=4, user__is_active=True).order_by("user__date_joined")
#     number_of_staff = len(team_members_staff)-1
#     # team_members_count = len(team_members_agents)-1
#     # print(team_members_count)
#     # number_of_staff = len(team_members_staff)-1
#     selected_class = count_to_class.get(number_of_staff, "default-class")
#     if sub_title == 'team_profiles':
#         team_categories = {
#         'Lead Team': list(team_members_staff),
#         'Support Team': list(team_members_agents),
#         'Senior Trainee Team': list(team_members_senior_trainees),
#         'Junior Trainee Team': list(team_members_junior_trainees),
#         }
#         user_group=team_members
#         heading="THE BEST TEAM IN ANALYTICS AND WEB DEVELOPMENT"
#     if sub_title == 'client_profiles':
#         team_categories = {
#         'Job Seekers': list(clients_job_seekers),
#         'Job Support': list(clients_job_support),
#         }
#         user_group=client_categories
#         heading="EXPERTS FOR DATA ANALYTICS/SCIENCE"

#     context = {
#         "team_categories": team_categories,
#         "team_members": user_group,
#         "title":heading,
#         "selected_class":selected_class
#     }
#     return render(request, "main/team_profiles.html", context)
    
openai.api_key = os.environ.get('OPENAI_API_KEY')
class SQSum(Subquery):
    output_field = models.IntegerField()
    template = "(SELECT sum(point) from (%(subquery)s) _sum)"


def generate_openai_description(user_profile):
    try:
        client_assessment = ClientAssessment.objects.filter(email=user_profile.user.email).first()
    except ClientAssessment.DoesNotExist:
        return "No ClientAssessment found for the user."
    first_name = client_assessment.first_name

    total_points =client_assessment.totalpoints
    experience =client_assessment.it_exp
    it_skills = [
        ('Non-IT Experience', client_assessment.non_it_exp),
        ('IT Experience', client_assessment.it_exp),
        ('Project Charter', client_assessment.projectcharter),
        ('Requirements Analysis', client_assessment.requirementsAnalysis),
        ('Reporting', client_assessment.reporting),
        ('ETL', client_assessment.etl),
        ('Database', client_assessment.database),
        ('Testing', client_assessment.testing),
        ('Deployment', client_assessment.deployment),
        ('Frontend', client_assessment.frontend),
        ('Backend',client_assessment.backend),
        # Add more IT skills as needed
    ]
    # Sort IT skills by rating in descending order
    sorted_it_skills = sorted(it_skills, key=lambda x: x[1], reverse=True)

    # Take the top two IT skills
    top_it_skills = [skill[0] for skill in sorted_it_skills[:2]]

    user_message = f"Generate a description for {first_name}, a professional with {experience} years of experience in {', '.join(top_it_skills)}."
    response=generate_chatbot_response(user_message)
    return response.strip()

def team(request,title):
    path_list, sub_title, pre_sub_title = path_values(request)
    if sub_title != 'client_profiles':

        #for aggregate sum of point in subquery
        def get_sqsum(field):
            class SQSum(Subquery):
                output_field = models.IntegerField()
                template = f"(SELECT sum({field}) from (%(subquery)s) _sum)"
            return SQSum
        
        #from task history model    
        employee_taskhistory_subquery = get_sqsum('point')(TaskHistory.objects.filter(employee_id__profile=OuterRef('pk')).values('point'))
        
        #from requirement model(counting duration-task hour as point for staff)
        employee_requiremet_subquery = get_sqsum('duration')(Requirement.objects.filter(assigned_to__profile=OuterRef('pk')).values('duration'))
        
        #from Training model
        employee_training_subquery = get_sqsum('level_point')(Training.objects.filter(presenter__profile=OuterRef('pk')).annotate(
            level_point=Case(
                When(level=1, then=F('level') * 5.0),
                When(level=2, then=F('level') * 10.0),
                When(level=3, then=F('level') * 15.0),
                When(level=4, then=F('level') * 20.0),
                When(level=5, then=F('level') * 25.0),
                default=F('level'),  # Default case, if level doesn't match any condition
                output_field=FloatField()
            )
        ).values('level_point'))
        
        #from clientassesment model(takeing latest totalpoints for that user)
        employee_clientassesment = ClientAssessment.objects.filter(email=OuterRef('user__email')).order_by('-rating_date')[:1]
        
        all_member = UserProfile.objects.filter(user__is_active=True, user__is_staff=True, user__category=2).annotate(
            
            taskhistory_points=Coalesce(employee_taskhistory_subquery, Value(0)),
            requirement_points=Coalesce(employee_requiremet_subquery, Value(0)),
            training_points=Coalesce(employee_training_subquery, Value(0)),
            clientassesment_points=Coalesce(employee_clientassesment.values('totalpoints'), Value(0)),
            total_points=F('taskhistory_points') + F('requirement_points') + F('training_points') + F('clientassesment_points')
        
        ).order_by("user__date_joined")

        all_staff_member = all_member.exclude(Q(user__sub_category=2) |Q(user__sub_category=6)|Q(user__username='c_maghas'))
        all_staff_contractor = all_member.filter(user__sub_category=2)
        
        # all_staff_member.values_list('user__username','user__email', 'taskhistory_points', 'requirement_points', 'training_points', 'clientassesment_points', 'total_points')
        
        team_member_value_json = Editable.objects.filter(name='team_profile_value_json')

        if team_member_value_json.exists():

            team_member_value_json = team_member_value_json.get().value
        
        else:
            team_member_value_json = {
                "lead_team":2000,
                "support_team":1000,
                "delta":500,
                "percentage": 10
            }

        staff_team = ["lead_team", "senior_analysts", "junior_analysts", "senior_trainee", "junior_trainee", "elementry"]
        
        threshold_dict = {} 
        previous_threshold = 0
        
        for team in staff_team:
            
            if team == 'lead_team':
                threshold_dict[team] = (team_member_value_json['lead_team']) 
            else:
                if previous_threshold - team_member_value_json['delta'] > 0:
                    threshold_dict[team] = previous_threshold - team_member_value_json['delta']
                else:
                    threshold_dict[team] = previous_threshold - (previous_threshold*team_member_value_json['percentage']/100)

            previous_threshold = threshold_dict[team]

        elite_team_member = UserProfile.objects.filter(user__is_superuser=True, user__username='c_maghas')
        
        lead_team = list(filter(lambda v: v.total_points > threshold_dict['lead_team'], all_staff_member))
        senior_analysts = list(filter(lambda v: v.total_points <= threshold_dict['lead_team'] and v.total_points > threshold_dict['senior_analysts'], all_staff_member))
        junior_analysts = list(filter(lambda v: v.total_points <= threshold_dict['senior_analysts'] and v.total_points > threshold_dict['junior_analysts'], all_staff_member))
        senior_trainee = list(filter(lambda v: v.total_points <= threshold_dict['junior_analysts'] and v.total_points > threshold_dict['senior_trainee'], all_staff_member))
        junior_trainee = list(filter(lambda v: v.total_points <= threshold_dict['senior_trainee'] and v.total_points > threshold_dict['junior_trainee'], all_staff_member))
        elementry = list(filter(lambda v: v.total_points <= threshold_dict['junior_trainee'], all_staff_member))

        support_team = list(filter(lambda v: v.total_points > team_member_value_json['support_team'], all_staff_contractor))

    # number_of_staff = len(lead_team)-1

    # selected_class = count_to_class.get(number_of_staff, "default-class")
    if sub_title == 'team_profiles':
        team_categories = {
        'Elite Team': list(elite_team_member),
        'Lead Team': lead_team,
        'Support Team': list(support_team),
        # 'Senior Analysts': senior_analysts,
        }
        user_group = team_members
        heading = "THE BEST TEAM IN ANALYTICS AND WEB DEVELOPMENT"

        # Generate descriptions for team members if not present
        for category, members in team_categories.items():
            for member in members:
                try:
                    user_profile = member.user.profile 
                except UserProfile.DoesNotExist:
                    user_profile = UserProfile.objects.create(user=member.user)

                if not user_profile.description:
                    total_points = ClientAssessment.objects.filter(
                        email=member.user.email
                    ).aggregate(Sum('totalpoints'))['totalpoints__sum']
                    try:
                        user_profile.description = generate_openai_description(user_profile)
                    except:
                        user_profile.description = 'null'
                    user_profile.save()
    
    if sub_title == 'client_profiles':

        clients_job_seekers = UserProfile.objects.filter(user__is_client=True, user__is_active=True).exclude(user__sub_category=4).order_by("user__date_joined")
        clients_job_support = UserProfile.objects.filter(user__is_client=True, user__sub_category=4, user__is_active=True).order_by("user__date_joined")
    
        team_categories = {
        'Job Seekers': list(clients_job_seekers),
        'Job Support': list(clients_job_support),
        }
        user_group=client_categories
        heading="EXPERTS FOR DATA ANALYTICS/SCIENCE"
    
    if sub_title == 'future_talents':
        team_categories = {
            'Junior Analysts': junior_analysts,
            # 'Senior Trainee Team': senior_trainee,
            'Junior Trainee Team': junior_trainee,
            'Elementary': elementry
        }
        user_group=future_talents
        heading="MINDS OF TOMORROW: LEADING DATA ANALYTICS AND WEB DEVELOPMENT"

    if sub_title == 'board':
        BOG_members = UserProfile.objects.filter(user__is_staff=True, user__is_active=True,user__sub_category=6).order_by("user__date_joined")
        team_categories = {
            'Board Members': list(BOG_members),
        }
        user_group=board_members
        heading="THE BOG"
    
    context = {
        "team_categories": team_categories,
        "team_members": user_group,
        "title":heading,
        # "selected_class":selected_class
    }
    return render(request, "main/team_profiles.html", context)


# def team(request):
#     path_list, sub_title, pre_sub_title = path_values(request)
#     if sub_title != 'client_profiles':

#         #for aggregate sum of point in subquery
#         def get_sqsum(field):
#             class SQSum(Subquery):
#                 output_field = models.IntegerField()
#                 template = f"(SELECT sum({field}) from (%(subquery)s) _sum)"
#             return SQSum
        
#         #from task history model    
#         employee_taskhistory_subquery = get_sqsum('point')(TaskHistory.objects.filter(employee_id__profile=OuterRef('pk')).values('point'))
        
#         #from requirement model(counting duration-task hour as point for staff)
#         employee_requiremet_subquery = get_sqsum('duration')(Requirement.objects.filter(assigned_to__profile=OuterRef('pk')).values('duration'))
        
#         #from Training model
#         employee_training_subquery = get_sqsum('level_point')(Training.objects.filter(presenter__profile=OuterRef('pk')).annotate(
#             level_point=Case(
#                 When(level=1, then=F('level') * 5.0),
#                 When(level=2, then=F('level') * 10.0),
#                 When(level=3, then=F('level') * 15.0),
#                 When(level=4, then=F('level') * 20.0),
#                 When(level=5, then=F('level') * 25.0),
#                 default=F('level'),  # Default case, if level doesn't match any condition
#                 output_field=FloatField()
#             )
#         ).values('level_point'))
        
#         #from clientassesment model(takeing latest totalpoints for that user)
#         employee_clientassesment = ClientAssessment.objects.filter(email=OuterRef('user__email')).order_by('-rating_date')[:1]
        
#         all_member = UserProfile.objects.filter(user__is_active=True, user__is_staff=True, user__category=2).annotate(
            
#             taskhistory_points=Coalesce(employee_taskhistory_subquery, Value(0)),
#             requirement_points=Coalesce(employee_requiremet_subquery, Value(0)),
#             training_points=Coalesce(employee_training_subquery, Value(0)),
#             clientassesment_points=Coalesce(employee_clientassesment.values('totalpoints'), Value(0)),
#             total_points=F('taskhistory_points') + F('requirement_points') + F('training_points') + F('clientassesment_points')
        
#         ).order_by("user__date_joined")

#         all_staff_member = all_member.exclude(Q(user__sub_category=2) | Q(user__username='c_maghas'))
#         all_staff_contractor = all_member.filter(user__sub_category=2)
        
#         # all_staff_member.values_list('user__username','user__email', 'taskhistory_points', 'requirement_points', 'training_points', 'clientassesment_points', 'total_points')
        
#         team_member_value_json = Editable.objects.filter(name='team_profile_value_json')

#         if team_member_value_json.exists():

#             team_member_value_json = team_member_value_json.get().value
        
#         else:
#             team_member_value_json = {
#                 "lead_team":2000,
#                 "support_team":1000,
#                 "delta":500,
#                 "percentage": 10
#             }

#         staff_team = ["lead_team", "senior_analysts", "junior_analysts", "senior_trainee", "junior_trainee", "elementry"]
        
#         threshold_dict = {} 
#         previous_threshold = 0
        
#         for team in staff_team:
            
#             if team == 'lead_team':
#                 threshold_dict[team] = (team_member_value_json['lead_team']) 
#             else:
#                 if previous_threshold - team_member_value_json['delta'] > 0:
#                     threshold_dict[team] = previous_threshold - team_member_value_json['delta']
#                 else:
#                     threshold_dict[team] = previous_threshold - (previous_threshold*team_member_value_json['percentage']/100)

#             previous_threshold = threshold_dict[team]

#         elite_team_member = UserProfile.objects.filter(user__is_superuser=True, user__username='c_maghas')
        
#         lead_team = list(filter(lambda v: v.total_points > threshold_dict['lead_team'], all_staff_member))
#         senior_analysts = list(filter(lambda v: v.total_points <= threshold_dict['lead_team'] and v.total_points > threshold_dict['senior_analysts'], all_staff_member))
#         junior_analysts = list(filter(lambda v: v.total_points <= threshold_dict['senior_analysts'] and v.total_points > threshold_dict['junior_analysts'], all_staff_member))
#         senior_trainee = list(filter(lambda v: v.total_points <= threshold_dict['junior_analysts'] and v.total_points > threshold_dict['senior_trainee'], all_staff_member))
#         junior_trainee = list(filter(lambda v: v.total_points <= threshold_dict['senior_trainee'] and v.total_points > threshold_dict['junior_trainee'], all_staff_member))
#         elementry = list(filter(lambda v: v.total_points <= threshold_dict['junior_trainee'], all_staff_member))

#         support_team = list(filter(lambda v: v.total_points > team_member_value_json['support_team'], all_staff_contractor))

#     # number_of_staff = len(lead_team)-1

#     # selected_class = count_to_class.get(number_of_staff, "default-class")
#     if sub_title == 'team_profiles':
#         team_categories = {
#         'Elite Team': list(elite_team_member),
#         'Lead Team': lead_team,
#         'Support Team': list(support_team),
#         'Senior Analysts': senior_analysts,
#         }
#         # user_group = team_members
        
#         user_group=Team_Members.objects.filter(category='analytics_team')
#         heading = "THE BEST TEAM IN ANALYTICS AND WEB DEVELOPMENT"

#         # Generate descriptions for team members if not present
#         for category, members in team_categories.items():
#             for member in members:
#                 try:
#                     user_profile = member.user.profile 
#                 except UserProfile.DoesNotExist:
#                     user_profile = UserProfile.objects.create(user=member.user)

#                 if not user_profile.description:
#                     total_points = ClientAssessment.objects.filter(
#                         email=member.user.email
#                     ).aggregate(Sum('totalpoints'))['totalpoints__sum']
#                     try:
#                         user_profile.description = generate_openai_description(user_profile)
#                     except:
#                         user_profile.description = 'null'
#                     user_profile.save()
    
#     if sub_title == 'client_profiles':

#         clients_job_seekers = UserProfile.objects.filter(user__is_client=True, user__is_active=True).exclude(user__sub_category=4).order_by("user__date_joined")
#         clients_job_support = UserProfile.objects.filter(user__is_client=True, user__sub_category=4, user__is_active=True).order_by("user__date_joined")
    
#         team_categories = {
#         'Job Seekers': list(clients_job_seekers),
#         'Job Support': list(clients_job_support),
#         }
#         # user_group=client_categories
#         user_group=Team_Members.objects.filter(category='clients')
#         print(user_group)
#         heading="EXPERTS FOR DATA ANALYTICS/SCIENCE"
    
#     if sub_title == 'future_talents':
#         team_categories = {
#             'Junior Analysts': junior_analysts,
#             'Senior Trainee Team': senior_trainee,
#             'Junior Trainee Team': junior_trainee,
#             'Elementary': elementry
#         }
#         # user_group=future_talents
#         user_group=Team_Members.objects.filter(category='future_talent')
#         print(user_group)
#         heading="MINDS OF TOMORROW: LEADING DATA ANALYTICS AND WEB DEVELOPMENT"

#     if sub_title == 'board':
#         team_categories = {
#             'Junior Analysts': junior_analysts,
#             'Senior Trainee Team': senior_trainee,
#             'Junior Trainee Team': junior_trainee,
#             'Elementary': elementry
#         }
#         # user_group=future_talents
#         user_group=Team_Members.objects.filter(category='board')
#         print(user_group)
#         heading="THE BOG"
    
#     context = {
#         "team_categories": team_categories,
#         "team_members": user_group,
#         "title":heading,
#         # "selected_class":selected_class
#     }
#     return render(request, "main/team_profiles.html", context)


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
        instance = form.save()
        form.instance.username = self.request.user
        # Replace 'folder_id' with the ID of the folder where you want to save the image.
        if form.cleaned_data.get('image') is not None and form.cleaned_data.get('image') is not False:
            image_name = form.cleaned_data.get('image').name
            folder_id =os.environ.get('DRIVER_FOLDER_ID')
            image_path = instance.image.path
            image_id = upload_image_to_drive(image_path, folder_id,image_name)
            assets_instance = Assets.objects.create(image_url=image_id)
            instance.image2 = assets_instance
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

def interview(request):
    return redirect('data:train')

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
    return render(request, "main/snippets_templates/static/images.html", {"title": "pay", "images": images})

class ImageUpdateView(LoginRequiredMixin,UpdateView):
    model=Assets
    fields = ['category','name','image_url','description',"is_active","is_featured",]
     
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


def FrequentlyAskedQuestion(request):
    CAT_CHOICES = [
        ("all", "all"),
        ("accounts", "Registration"),
        ("application", "Application"),
        ("finance", "Financial Information"),
        ("management", "Employees Activities"),
        ("data", "Data Analysis"),
        ("getdata", "Automation"),
        ("investing", "Investments"),
        ("main", "General Information"),
        ("projectmanagement", "Field Projects"),
    ]
    questions = Search.objects.all().distinct('question')

    if request.method == 'POST':
        raw_data = request.body.decode('utf-8')

        if raw_data:
            
            payload = json.loads(raw_data)
            question = payload.get('question', None)
            category = payload.get('category', None)
            topic = payload.get('topic', None)

            if question:
                question += f"and for more context, try to refer {topic} table in {category} category first."
                print(question)
                # Parse the JSON data
                response = langchainModelForAnswer(question)
                print(response)

                return JsonResponse({"answer": response})
    else:

        category = request.GET.get('category')
        if category and category != "all":
            questions = questions.filter(category=category)
     
        context = {
            "questions": questions,
            "categories": CAT_CHOICES
        }
        return render(request, "main/home_templates/help.html", context)
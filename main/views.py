import webbrowser
import datetime
import random
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.shortcuts import redirect, render,get_object_or_404
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from .models import Service,Plan,Assets
from .utils import (Meetings,path_values,buildmodel,team_members,url_mapping,
                    client_categories,service_instances,service_plan_instances,reviews,packages,courses,
                    generate_database_response,generate_chatbot_response,upload_image_to_drive
)
from .models import Testimonials
from getdata.models import Logs
from coda_project import settings
from application.models import UserProfile
from management.utils import task_assignment_random
from finance.models import Payment_Information
from main.forms import PostForm,ContactForm

from django.contrib.auth.decorators import login_required
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
from django.http import JsonResponse
from django.apps import apps
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

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
    count_to_class = {
        2: "col-md-6",
        3: "col-md-4",
        4: "col-md-3"
    }
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

    number_of_testimonials = len(testimonials)
    selected_class = count_to_class.get(number_of_testimonials, "default-class")

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
            data = form.cleaned_data
            instance = form.save(commit=False)
            instance.searched_by = request.user
            category = form.instance.category
            table = form.instance.topic
            # print('table============',table)
            question = form.instance.question
            app = category
            result, = generate_database_response(user_message=question, app=app,table=table)
            if result:
                # This one is simple hu
                # llm = OpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
                chat_model = ChatOpenAI(openai_api_key='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')
                messages = [HumanMessage(content=str(result))]
                # response_llm = llm.predict_messages(messages)
                chat_model_result = chat_model.predict_messages(messages)
                # response1 = response_llm.content.split(':', 1)[-1].strip()
                response = chat_model_result.content
            else:
                response = None

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
    
    if not user_message:
        return JsonResponse({'response': 'Invalid user message'})
    try:
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


def display_service(request,*args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        service_shown = Service.objects.all()
    except Service.DoesNotExist:
        return redirect('main:display_service')
    (service_category_slug,service_category_title,service_description,service_id)=service_instances(service_shown,sub_title)
    service_categories = ServiceCategory.objects.filter(service=service_id)
    if service_category_slug=='investing':
        context = {
            'service_categories': service_categories,
            "title": service_category_title,
            "service_desc": service_description,
            "slug":service_category_slug
       }
        return render(request, "main/home_templates/investing_home.html", context)
    context = {}  # Initialize context with an empty dictionary
    context = {
        'service_categories': service_categories,
        "title": service_category_title,
        "service_desc": service_description,
        "slug":service_category_slug
    }
    return render(request, "main/services/show_service.html", context)



def service_plans(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    # print("pre_sub_title==========>",pre_sub_title)
    # try:
    #     payment_details = Payment_Information.objects.get(customer_id_id=request.user.id)
    # except:
    #     payment_details=[]
    try:
        if pre_sub_title:
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
        "services": plans
    }
    # print(request.user.category)
    # if payment_details and request.user.category==3:
    #     return render(request, "data/interview/interview_progress/start_interview.html",context)
    # else:
    return render(request, "main/services/service_plan.html", context)


# def full_course(request, *args, **kwargs):
#     path_list, sub_title, pre_sub_title = path_values(request)
#     # print("pre_sub_title==========>",pre_sub_title)
#     try:
#         service_shown = Service.objects.get(slug="data_analysis")
#     except Service.DoesNotExist:
#         return redirect('main:display_service', slug ='data_analysis')
#     service_categories = ServiceCategory.objects.filter(service=service_shown.id)
#     (category_slug,category_name,category_id)=service_plan_instances(service_categories,sub_title)
#     plans = Pricing.objects.filter(category=category_id)

#     context = {}
#     context = {
#         "SITEURL": settings.SITEURL,
#         "title": category_name,
#         "packages": packages,
#         "category_slug": category_slug,
#         "courses": courses,
#         "services": plans
#     }
#     # print(request.user.category)
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
        topics = ['Tableau', 'SQL', 'Business Analyst', 'Alteryx', 'Power BI', 'Scrum Master']

        # Randomly select a title from the list
        selected_title = random.choice(topics)
        quest = f"write a full paragraph on how good my {selected_title} coach was" # pick a question bunch of questions
        result = buildmodel(question=quest)

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

def team(request):
    count_to_class = {
        2: "col-md-6",
        3: "col-md-4",
        4: "col-md-3"
    }
    
    path_list, sub_title, pre_sub_title = path_values(request)
    team_members_staff = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__sub_category=1).order_by("user__date_joined")
    team_members_agents = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__sub_category=2).order_by("user__date_joined")
    team_members_senior_trainees = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__category=2, user__sub_category=5).order_by("user__date_joined")
    team_members_junior_trainees = UserProfile.objects.filter(user__is_staff=True, user__is_active=True, user__category=2, user__sub_category=4).order_by("user__date_joined")
    clients_job_seekers = UserProfile.objects.filter(user__is_client=True, user__is_active=True).exclude(user__sub_category=4).order_by("user__date_joined")
    clients_job_support = UserProfile.objects.filter(user__is_client=True, user__sub_category=4, user__is_active=True).order_by("user__date_joined")
    number_of_staff = len(team_members_staff)-1
    # team_members_count = len(team_members_agents)-1
    # print(team_members_count)
    # number_of_staff = len(team_members_staff)-1
    selected_class = count_to_class.get(number_of_staff, "default-class")
    if sub_title == 'team_profiles':
        team_categories = {
        'Lead Team': list(team_members_staff),
        'Support Team': list(team_members_agents),
        'Senior Trainee Team': list(team_members_senior_trainees),
        'Junior Trainee Team': list(team_members_junior_trainees),
        }
        user_group=team_members
        heading="THE BEST TEAM IN ANALYTICS AND WEB DEVELOPMENT"
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
        "title":heading,
        "selected_class":selected_class
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
    fields=['position','description','image','google_image_id','image2','is_active','laptop_status']
    def form_valid(self, form):
        instance = form.save()
        form.instance.username = self.request.user
        # Replace 'folder_id' with the ID of the folder where you want to save the image.
        if form.cleaned_data.get('image') is not None:
            image_name = form.cleaned_data.get('image').name
            folder_id ="15DFj4PQIqRFgM1T9x18Dq2rzmK32YLQ_" # os.environ.get('DRIVER_FOLDER_ID') #'1qzO8GAa5jGRgFYsamGEmnrI_bHbJ6Zre'
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
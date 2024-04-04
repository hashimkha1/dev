import webbrowser
import datetime
import random
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.shortcuts import redirect, render,get_object_or_404
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta

from .utils import (Meetings,path_values,buildmodel,team_members,future_talents, url_mapping,
                    client_categories,service_instances,service_plan_instances,reviews,packages,courses,
                    generate_database_response,generate_chatbot_response,upload_image_to_drive
)
from .models import CompanyAsset
#from getdata.models import Logs
from coda_project import settings
#from application.models import UserProfile
# from management.utils import task_assignment_random
# from management.models import TaskHistory
# from finance.models import Payment_Information
#from main.forms import PostForm,ContactForm

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
from django.db.models import F, FloatField, Case, When, Value, Subquery, OuterRef, Q
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
# from management.models import Requirement, Training
# from data.models import ClientAssessment
# from getdata.models import Editable

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
    # count_to_class = {
    #     2: "col-md-6",
    #     3: "col-md-4",
    #     4: "col-md-3"
    # }
    # latest_posts = Testimonials.objects.values('writer').annotate(latest=Max('date_posted')).order_by('-latest')
    # testimonials = []
    # for post in latest_posts:
    #     writer = post['writer']
    #     #querying for the latest post
    #     user_profile = UserProfile.objects.filter(user=writer,user__is_client=True).first()
    #     # user_profile = UserProfile.objects.filter(user=writer).first()
    #     if user_profile:
    #         latest_post = Testimonials.objects.filter(writer=writer, date_posted=post['latest']).first()
    #         testimonials.append(latest_post)

    # number_of_testimonials = len(testimonials)
    # selected_class = count_to_class.get(number_of_testimonials, "default-class")

    # services = Service.objects.filter(is_active=True).order_by('serial')
    context = {
       # "services": services,
        #"posts": testimonials,
        "title": "layout",
        #"selected_class": selected_class,
    }
    return render(request, "main/home_templates/newlayout.html", context)



def fetch_model_table_names(request):
    app_name = request.GET.get('category', None)  # Replace with the actual app name
    app_models = apps.get_app_config(app_name).get_models()
    # Get the actual model table names based on the application
    # table_names = [model.__name__ for model in app_models]
    table_names = [{'value': model.__name__, 'display_text': model._meta.verbose_name.replace('_', ' ').capitalize()} for model in app_models]
    return JsonResponse({'model_table_names': table_names})


# # =====================TESTIMONIALS  VIEWS=======================================
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

def coda_assets_list(request):
    assets = CompanyAsset.objects.all()
    return render(request, "main\departments\codassetslist.html", {"assets":assets})
 

def shoppinglist(request):
    assets = CompanyAsset.objects.all()
    return render(request, "main\departments\codassetslist.html", {"assets":assets})

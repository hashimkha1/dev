import webbrowser
import datetime
import random
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.db.models import Q
from django.shortcuts import redirect, render,get_object_or_404
from datetime import datetime,date,timedelta
# from dateutil.relativedelta import relativedelta

#from .utils import (generate_chatbot_response,handle_openai_api_exception,analyze_website_for_wcag_compliance )
from .models import websitewcag
from .forms import wcagForm
#from getdata.models import Logs
# from coda_project import settings
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
import json
from django.http import JsonResponse
from django.apps import apps
# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage
import os
from django.db.models import F, FloatField, Case, When, Value, Subquery, OuterRef, Q
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
# from management.models import Requirement, Training
# from data.models import ClientAssessment
# from getdata.models import Editable

def websitewcag_list(request):
    wcaglists=websitewcag.objects.all().order_by("updated_at")
    print("wcaglists=====>",wcaglists)
    
    return render(request, "application/wcaglist.html",{"wcaglists":wcaglists})

def websitewcagcreate_view(request):
    if request.method == 'POST':
        form =wcagForm(request.POST)
        if form.is_valid():
            form.save            
            return redirect("application:wcaglist")
    else:
        form = wcagForm()
        print("form ====>",form) 
    return render(request,"application/wcagcreate.html", {'form': form})      

    
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

# def websitewcagcreate_view(request):
#     if request.method == 'POST':
#         form =wcagForm(request.POST)
#         if form.is_valid():
#             form.save            
#             return redirect("application:wcaglist")
#     else:
#         form = wcagForm()
#         print("form ====>",form) 
#     return render(request,"application/wcagcreate.html", {'form': form}) 


class Accessibility:
    def __init__(self, wcag_data):
        self.is_compliant = wcag_data.get('is_compliant', False)
        self.errors = wcag_data.get('errors', [])
        self.warnings = wcag_data.get('warnings', [])
        self.improvements = wcag_data.get('improvements', [])

    @property
    def compliance_level(self):
        # Simplified to just 'pass' or 'fail'
        return "Pass" if self.is_compliant else "Fail"

    def summary(self):
        return {
            'compliance_level': self.compliance_level,
            'number_of_errors': len(self.errors),
            'number_of_warnings': len(self.warnings),
            'recommended_improvements': self.improvements
        }

def websitewcagcreate_view(request):
    if request.method == 'POST':
        form = wcagForm(request.POST, request.FILES)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            page_name = form.cleaned_data['page_name']
            uploaded_file_content = request.FILES['uploaded_file'].read()

            # Check if there is an existing record for the same website URL and page name
            query =wcagForm.objects.filter(website_url__contains=website_url, page_name__contains=page_name)
            if query.exists():
                query_instance = query.first()
                responses = query_instance.improvements
            else:
                # Perform analysis if no existing record found
                responses = analyze_website_for_wcag_compliance(uploaded_file_content)

            try:
                # Try to parse the JSON response
                final_json_response = json.loads(responses.replace('json', '').strip('''''').strip('\n'))
                accessibility_instance = Accessibility(final_json_response)
                context = {
                    "form": wcagForm(),
                    "website_url": website_url,
                    "suggestions": responses,
                    "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
                    "page_name": page_name,
                    "improved_coda": final_json_response.get('improved_coda'),  # Using get() to avoid KeyError
                    "problem_list": final_json_response.get('list_of_problem')  # Using get() to avoid KeyError
                }
                # Save form data to the model
                instance = form.save(commit=False)
                instance.improvements = responses
                instance.save()
            except Exception as e:  # Catching all exceptions
                suggestions = handle_openai_api_exception(responses)
                context = {
                    "form": wcagForm(),
                    "website_url": website_url,
                    "suggestions": suggestions,  # Using 'suggestions' instead of 'responses'
                    "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
                    "improved_code": None,
                    "page_name": page_name,
                    "problem_list": []  # Empty list for problem_list
                }
            return redirect('application:wcaglist')
    else:
        form = wcagForm()
        context = {
            "form": form,
            "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
        }
    return render(request, 'application\openaicreate.html', context)

    
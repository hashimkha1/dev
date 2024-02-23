import math
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import WCAG_TAB_Form
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
from .models import WCAG_TAB

def WCAG_TAB_list(request):
    wcaglist = WCAG_TAB.objects.all()
    return render(request,"application/applications/wcagtablist.html",{'wcaglist':wcaglist})

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

def WCAGTABcreate_view(request):
    if request.method == 'POST':
        form = WCAG_TAB_Form(request.POST, request.FILES)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            page_name = form.cleaned_data['page_name']
            uploaded_file_content = request.FILES['uploaded_file'].read()

            # Check if there is an existing record for the same website URL and page name
            query = WCAG_TAB.objects.filter(website_url__contains=website_url, page_name__contains=page_name)
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
                    "form": WCAG_TAB_Form(),
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
                    "form": WCAG_TAB_Form(),
                    "website_url": website_url,
                    "suggestions": suggestions,  # Using 'suggestions' instead of 'responses'
                    "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
                    "improved_code": None,
                    "page_name": page_name,
                    "problem_list": []  # Empty list for problem_list
                }
            return redirect('application:wcaglist')
    else:
        form = WCAG_TAB_Form()
        context = {
            "form": form,
            "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
        }
    return render(request, 'application/applications/wcagtabcreateOPENAI.html', context)

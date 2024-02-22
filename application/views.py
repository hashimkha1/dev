from django.db.models import Q
from django.utils.text import capfirst
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import (
        CreateView,
        DeleteView,
        ListView,
        DetailView,
        UpdateView,
    )
from.models import codawebsite
from .forms import wcagForm

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model


def codawebsite_list_view(request):
    wcaglists=codawebsite.objects.all().order_by("updated_at")
    
    return render(request,"application/wcaglist.html",{"wcaglists":wcaglists})

# def codawebsitecreate_view(request):
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

def codawebsitecreate_view(request):
    if request.method == 'POST':
        form = wcagFormForm(request.POST, request.FILES)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            page_name = form.cleaned_data['page_name']
            uploaded_file_content = request.FILES['uploaded_file'].read()

            # Check if there is an existing record for the same website URL and page name
            query = codawebsite.objects.filter(website_url__contains=website_url, page_name__contains=page_name)
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
            return redirect('application:openailist')
    else:
        form = wcagForm()
        context = {
            "form": form,
            "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
        }
    return render(request, 'application/openaicreate.html', context)

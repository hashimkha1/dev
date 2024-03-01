import math
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from accounts.models import Transaction,Payment_History,Payment_Information
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
from.models import Balancesheet_category,Balancesheet_entry,BalanceSheet_Summary,WCAGCODA
import logging
from. forms import wcagForm



def Balancesheet_category_list(request):
    categories=Balancesheet_category.objects.all()
    print('category=========================>',categories)
    return render(request,'application/training/balancesheetlist.html',{'categories':categories})

logger = logging.getLogger(__name__)

def openai_balancesheet(request):
    # Fetch financial data using the previously defined function
    assets, liabilities, equity = fetch_and_process_financial_data(request)

    # Logic to use the assets, liabilities, and equity data
    # This part depends on how you want to utilize this data in your application
    # ...

def balancesheet_list(request):
    try:
        balance_sheet = BalanceSheet_Summary.objects.last()  
        if balance_sheet:
            current_assets = balance_sheet.entries.filter(category__category_type='Assets')
            current_liabilities =  balance_sheet.entries.filter(category__category_type='Liability')
            equity = balance_sheet.entries.filter(category__category_type='Equity')
            total_assets = current_assets.aggregate(sum('amount'))['amount'] or 0
            total_liabilities = current_liabilities.aggregate(sum('amount'))['amount'] or 0
            total_equity = equity.aggregate(sum('amount'))['amount'] or 0
            total_liabilities_and_equity = total_liabilities + total_equity

            context = {
                'company_name':'CODA',
                'balance_sheet':balance_sheet,
                'current_assets':current_assets,
                'current_liabilities':current_liabilities,
                'equity':equity,
                'total_assets': total_assets,
                'total_liabilities_and_equity': total_liabilities_and_equity,
                'total_liabilities': total_liabilities,
                'total_equity': total_equity
            }
        else: 
            context = {'error_message':'No balance sheet data available.'} 
    except Exception as e:
        logger.erro(f"error fetching balance sheet data: {e}")  
        context = {'error_message': 'An error occured while fetching balance_sheet data'} 

    return render(request,'application/training/balancelist.html',context)  

def wcag_list_view(request):
    wcaglists=WCAGCODA.objects.all().order_by("updated_at")
    
    return render(request, "application\wcaglist.html",{"wcaglists":wcaglists})    

# def wcag_create_view(request):
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

def wcag_create_view(request):
    context = {}
    if request.method == 'POST':
        form = wcagForm(request.POST, request.FILES)
        if form.is_valid():
            website_url = form.cleaned_data['website_url']
            page_name = form.cleaned_data['page_name']
            uploaded_file_content = request.FILES['uploaded_file'].read()

            # Check if there is an existing record for the same website URL and page name
            query = WCAGCODA.objects.filter(website_url__contains=website_url, page_name__contains=page_name)
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
            return redirect('application:API list')
    else:
        form = wcagForm()
        context = {
            "form": form,
            "accessibility":  Accessibility({}).summary(),  # Assuming Accessibility is defined somewhere
        }
    return render(request, 'application/API create.html', context)


             
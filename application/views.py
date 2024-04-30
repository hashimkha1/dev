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
from.models import Balancesheet_category,Balancesheet_entry,BalanceSheet_Summary,InvestmentStrat,Application_user
import logging
from django.urls import reverse,reverse_lazy
from .forms import investForm



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


def investList(request):
    investment_strats = InvestmentStrat.objects.all()
    return render(request, "application/ListView.html", {"investment_strats":investment_strats})

class List(ListView): 
      model = InvestmentStrat
  
      template_name = 'application/ListView.html'


class investCreat(CreateView): 
      model = InvestmentStrat
      form_class = investForm
      template_name = 'application/Creat.html'
      success_url = reverse_lazy('application:lt')
      
      def form_valid(self,form):
            return super().form_valid(form)

  
class investUp(UpdateView):
    model = InvestmentStrat
    form_class = investForm  # Assuming you have a form xForm for xuser
    template_name = 'application/updateview.html'
    success_url = reverse_lazy('application:lt')  # URL to redirect after updating


class investDel(DeleteView):
    model = InvestmentStrat
    template_name = 'application/deleteview.html'
    success_url = reverse_lazy('application:lt')  # URL to redirect after deleting


class investDet(DetailView):
    model = InvestmentStrat
    template_name = 'application/investmentstrat_detail.html'
    context_object_name = 'investment_strats'

def Application_user_list(request):
    categories = Application_user.objects.all()
    return render(request, 'application/application_list.html', {'categories': categories})



             
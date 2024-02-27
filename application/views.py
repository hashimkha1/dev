from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.http import QueryDict, Http404,JsonResponse
from requests import request
from datetime import datetime,date
from decimal import *
from django.urls import reverse,reverse_lazy
from django.views.generic import (
	CreateView,
	ListView,
	UpdateView,
	DetailView,
	DeleteView,
)
import json
#from accounts.models import CustomerUser
from .models import (		
        Balance_Sheet_Entry,BalanceSheetSummary
	)

# def Balance_sheet_list(request):
#     categories = Balance_sheetCategory.objects.all()
#     print ('categories========>, categories')
#     return render (request,"application/balancelist.html",{'categories':categories})

def balancesheet(request):
    try:
        balance_sheet = BalanceSheetSummary.objects.last()
        if balance_sheet:
            # Fetch entries for assets, liabilities, and equity
            current_assets = balance_sheet.entries.filter(category__category_type='Asset')
            current_liabilities = balance_sheet.entries.filter(category__category_type='Liability')
            equity = balance_sheet.entries.filter(category__category_type='Equity')

            # Calculate totals
            total_assets = current_assets.aggregate(Sum('amount'))['amount__sum'] or 0
            total_liabilities = current_liabilities.aggregate(Sum('amount'))['amount__sum'] or 0
            total_equity = equity.aggregate(Sum('amount'))['amount__sum'] or 0
            total_liabilities_and_equity=total_liabilities+total_equity
            context = {
                'company_name': 'CODA',
                'balance_sheet': balance_sheet,
                'current_assets': current_assets,
                'current_liabilities': current_liabilities,
                'equity': equity,
                'total_liabilities_and_equity': total_liabilities_and_equity,
                'total_assets': total_assets,
                'total_liabilities': total_liabilities,
                'total_equity': total_equity
            }
        else:
            context = {'error_message': 'No balance sheet data available.'}
    except Exception as e:
        print(f"Error: {e}")
        context = {'error_message': 'An error occurred while fetching balance sheet data.'}

    return render(request, "application/balancesheet.html", context)

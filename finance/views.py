import datetime
import json
import ast
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect,render
from requests import request
from accounts.forms import UserForm
from accounts.models import CustomerUser
from .models import Payment_Information,Payment_History,Default_Payment_Fees
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render
from django.db.models import Count
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from management.utils import email_template
# from .forms import (
#     # TransactionForm,
#     OutflowForm,
#     InflowForm,
#     PolicyForm,
#     ManagementForm,
#     RequirementForm,
#     EvidenceForm,
# )
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from data.models import DSU

from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import Tracker

# User=settings.AUTH_USER_MODEL
User = get_user_model()



# Create your views here.


#================================STUDENT AND JOB SUPPORT CONTRACT FORM SUBMISSION================================

def contract_form_submission(request):
	try:
		if request.method == "POST":
			user_student_data = request.POST.get('usr_data')
			student_dict_data = QueryDict(user_student_data)
			username = student_dict_data.get('username')
			customer=CustomerUser.objects.filter(username=username)
			if customer:
				return redirect('data:bitraining')
			else:
				form=UserForm(student_dict_data)
				print("form --->",form)
				if form.cleaned_data.get('category') == 1:
					form.instance.is_applicant = True
				elif form.cleaned_data.get('category') == 2:
					form.instance.is_employee = True 
				elif form.cleaned_data.get('category') == 3:
					form.instance.is_client = True 
				else:
					form.instance.is_admin = True 
				form.save()
				customer=CustomerUser.objects.get(username=username)
				payment_fees = int(request.POST.get('duration'))*1000
				down_payment = int(request.POST.get('down_payment'))
				student_bonus_amount = request.POST.get('bonus')
				fee_balance = payment_fees - down_payment
				if request.POST.get('student_contract'):
					fee_balance = payment_fees - (down_payment+int(student_bonus_amount))
				plan = request.POST.get('duration')
				payment_method = request.POST.get('payment_type')
				client_signature = request.POST.get('client_sign')
				company_rep = request.POST.get('rep_name')
				client_date = request.POST.get('client_date')
				rep_date = request.POST.get('rep_date')
				payment_data=Payment_Information(payment_fees=int(payment_fees),
					down_payment=down_payment,
					student_bonus = student_bonus_amount,
					fee_balance=int(fee_balance),
					plan=plan,
					payment_method=payment_method,
					client_signature=client_signature,
					company_rep=company_rep,
					client_date=client_date,
					rep_date=rep_date,
					customer_id_id=int(customer.id)
					)
				payment_data.save()
				payment_history_data=Payment_History(payment_fees=int(payment_fees),
					down_payment=down_payment,
					student_bonus = student_bonus_amount,
					fee_balance=int(fee_balance),
					plan=plan,
					payment_method=payment_method,
					client_signature=client_signature,
					company_rep=company_rep,
					client_date=client_date,
					rep_date=rep_date,
					customer_id=int(customer.id)
					)
				payment_history_data.save()
				messages.success(request, f'Account created for {username}!')
				return redirect('data:bitraining')
	except Exception as e:
		print("Student Form Creation Error ==>",print(e))

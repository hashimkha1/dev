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
from accounts.models import CustomerUser
from .models import (
		LoanUsers, Payment_Information,Payment_History,
		Default_Payment_Fees,TrainingLoan,
		Inflow,Transaction,PayslipConfig,Supplier,Food,FoodHistory,
		DC48_Inflow,Field_Expense,Budget,
        BalanceSheetCategory,BalanceSheetEntry,BalanceSheetSummary
	)
from .forms import (LoanForm,TransactionForm,InflowForm,
					DepartmentFilterForm,FoodHistoryForm,BudgetForm)

from mail.custom_email import send_email
from coda_project.settings import SITEURL,payment_details
from main.utils import path_values,countdown_in_month,dates_functionality
from main.filters import FoodFilter
from main.models import Service,ServiceCategory,Pricing,Company
from investing.models import Investments,Investment_rates,Investor_Information
from investing.utils import get_user_investment
from management.utils import paytime,loan_computation,paymentconfigurations
from management.models import Requirement
from django.views import View
from .utils import *
from .mpesa_integration import *


User = get_user_model()

# payment details
phone_number,email_info,cashapp,venmo,account_no=payment_details(request)


#Time details
(remaining_days, remaining_seconds, remaining_minutes, remaining_hours) = countdown_in_month()
#Exchange Rate details
usd_to_kes = get_exchange_rate('USD', 'KES')
rate = round(Decimal(usd_to_kes), 2)

def finance_report(request):
    return render(request, "finance/reports/finance.html", {"title": "Finance"})


@login_required
def add_budget_item(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            instance=form.save(commit=False)
            print(request.user)
            instance.budget_lead=request.user
            instance.save()
            return redirect("finance:budget")
    else:
        form = BudgetForm()
    return render(request, "finance/budgets/newbudget.html", {"form": form})

def budget(request):
    budget_obj=Budget.objects.all()
    ytd_duration,current_year,first_date=dates_functionality()
    webhour, delta = PayslipConfig.objects.values_list("web_pay_hour", "web_delta").first()
    total_amt = sum(transact.ksh_amount for transact in budget_obj)
    total_usd_amt =float(total_amt)/float(rate)
    # print("Amounts",total_outflows,ytd_outflows,total_field_ouflow_usd,total_web_ouflow,total_field_ouflow_usd)
    data = [
        {"title": "Amount(Ksh)", "value": total_amt},
        {"title": "Amount(usd)", "value": total_usd_amt},
	]

    context = {
        "budget_obj": budget_obj,
        "data": data,
        "webhour": webhour,
        "delta": delta,
        "remaining_days": remaining_days,
        "remaining_seconds ": int(remaining_seconds % 60),
        "remaining_minutes ": int(remaining_minutes % 60),
        "remaining_hours": int(remaining_hours % 24),
    }
    return render(request, "finance/budgets/budget.html", context)


class BudgetUpdateView(UpdateView):
	model = Budget
	success_url = "/finance/budget/"
	template_name="main/snippets_templates/generalform.html"
	fields ="__all__"

	def form_valid(self, form):
		if self.request.user.is_superuser or self.request.user:
			return super().form_valid(form)
		else:
			return render(request,"main/snippets_templates/generalform.html")

	def test_func(self):
		# task = self.get_object()
		if self.request.user.is_superuser:
			return True
		if self.request.user:
		    return True



def investment_report(request):
    return render(request, "finance/reports/investment_report.html", {"title": "Investment"})

#================================STUDENT AND JOB SUPPORT CONTRACT FORM SUBMISSION================================
def contract_data_submission(request):
	(today,*_)=paytime()
	try:
		if request.method == "POST":
			user_student_data = request.POST.get('usr_data')
			contract_charge = request.POST.get('contract_charge')
			contract_duration = request.POST.get('contract_duration')
			contract_period = request.POST.get('contract_period')
			student_dict_data = QueryDict(user_student_data)
			username = student_dict_data.get('username')
			try:
				customer=CustomerUser.objects.get(username=username)
				ss= customer.id
			except:
				customer= request.user
			payment_fees = float(contract_charge)
			down_payment = int(payment_fees*0.33)
			student_bonus_amount = 0
			fee_balance = payment_fees - down_payment
			plan = int(contract_duration)
			payment_method = request.POST.get('payment_type')
			client_signature =username
			company_rep = "coda"
			client_date = today
			rep_date = today
			print("data",customer,
					payment_fees,
					down_payment,
					student_bonus_amount,
					fee_balance,
					plan,
					payment_method,
					client_signature,
					company_rep,
					client_date,
					rep_date,)
			try:
				# payment = Payment_Information.objects.get(customer_id_id=customer.id)
				payment = Payment_Information.objects.filter(
            			customer_id=customer.id
        			).first()
				
			except:
				payment = None
			if payment:
				payment_data=Payment_Information.objects.filter(customer_id_id=int(customer.id)).update(payment_fees=int(payment_fees),
					down_payment=down_payment,
					student_bonus = student_bonus_amount,
					fee_balance=int(fee_balance),
					plan=plan,
					payment_method=payment_method,
					client_signature=client_signature,
					company_rep=company_rep,
					client_date=client_date,
					rep_date=rep_date)
			else:
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
			new_payment_added = Payment_Information.objects.filter(customer_id_id=customer.id).first()

			if new_payment_added:
				# messages.success(request, f'Added New Contract For the {username}!')
				return redirect('management:companyagenda')
			else:
				# messages.success(request, f'Account created for {username}!')
				if request.user.category == 3  or request.user.is_superuser: 
					return redirect('main:job_support')
				if request.user.category == 4 or request.user.is_superuser: 
					return redirect('main:full_course')
				else:
					return redirect('management:companyagenda')
			
	except Exception as e:
		# print("Student Form Creation Error ==>",print(e))
		message=f'Hi,{request.user}, there is an issue on our end kindly contact us directly at info@codanalytics.net'
		context={
                  "title": "CONTRACT", 
                  "message": message,
                }
		return render(request, "main/errors/generalerrors.html", context)
	

def contract_investment_submission(request):
	(today,*_)=paytime()
	try:
		if request.method == "POST":
			user_investor_data = request.POST.get('usr_data')
			investment_contract = request.POST.get('investment_contract')
			total_amount = float(request.POST.get('total_amount'))
			protected_capital = float(request.POST.get('protected_capital'))
			amount_invested = float(request.POST.get('amount_invested'))
			contract_duration = request.POST.get('contract_duration')
			number_positions = int(request.POST.get('number_positions'))
			bi_weekly_returns = float(request.POST.get('bi_weekly_returns'))
			beneficiary_name = request.POST.get('beneficiary_name', None)
			beneficiary_relation = request.POST.get('beneficiary_relation', None)
			investor_dict_data = QueryDict(user_investor_data)
			username = investor_dict_data.get('username')
			try:
				investor=CustomerUser.objects.get(username=username)
				ss= investor.id
			except:
				investor= request.user
			payment_method = request.POST.get('payment_type')
			client_signature =username
			company_rep = "coda"

			investor_data=Investor_Information(
				total_amount=int(total_amount),
				protected_capital=int(protected_capital),
				amount_invested=amount_invested,
				duration=int(contract_duration),
				positions=int(number_positions),
				bi_weekly_returns=int(bi_weekly_returns),
				payment_method=payment_method,
				client_signature=client_signature,
				company_rep=company_rep,
				investor_id=int(investor.id),
				beneficiary_relation=beneficiary_relation,
				beneficiary_name=beneficiary_name
				)
			investor_data.save()
			payment_data=Payment_Information(
				payment_fees=int(total_amount),
				fee_balance=int(total_amount),
				down_payment=int(total_amount),
                payment_method=payment_method,
                client_signature=client_signature,
                company_rep=company_rep,
                client_date=datetime.today(),
                rep_date=datetime.today(),
                customer_id_id=int(request.user.id),
				plan=999
                )
			payment_data.save()
			# new_payment_added = Investor_Information.objects.get(investor_id=investor.id)
			# print("new_payment====>",new_payment_added)
			# if new_payment_added:
			# messages.success(request, f'Added New Contract For the {username}!')
			# return redirect('management:companyagenda')
			return redirect('finance:pay')
	except Exception as e:
		message=f'Hi,{request.user}, there is an issue on our end kindly contact us directly at info@codanalytics.net'
		context={
                  "title": "CONTRACT", 
                  "message": message,
                }
		return render(request, "main/errors/generalerrors.html", context)

@login_required
def mycontract(request, *args, **kwargs):
	username = kwargs.get('username')
	client_data = CustomerUser.objects.get(username=username)

	if client_data.category == 5:
		try:
			investor_details = Investor_Information.objects.filter(investor_id=client_data.id).order_by('-contract_date').first()
			print(Investor_Information.objects.filter(investor_id=client_data.id).values_list('beneficiary_name','contract_date'))
			if investor_details:
				contract_date = investor_details.contract_date.strftime("%d %B, %Y")
				context = {
                    'client_data': client_data,
                    'contract_date': contract_date,
                    'investor_data': investor_details,
                }
				return render(request, 'management/contracts/my_investor_contract.html', context)
			else:
				return redirect('investing:investments')	

		except Investor_Information.DoesNotExist:
			return redirect('investing:investments')
	else:
		try:
			payment_details = Payment_Information.objects.filter(customer_id_id=client_data.id).first()
			contract_date = payment_details.contract_submitted_date.strftime("%d %B, %Y")
			context = {
				'job_support_data': client_data,
				'contract_date': contract_date,
				'payment_data': payment_details,
			}
			if client_data.category == 3 or client_data.category == 4:
				return render(request, 'management/contracts/my_supportcontract_form.html', context)
			else:
				raise Http404("Login/Wrong Page: Are You a Client?")
		
		except Payment_Information.DoesNotExist:
			if client_data.category == 3:
				return redirect('main:job_support')
			elif client_data.category == 4:
				return redirect('main:service_plans',slug="full-course")
			else:
				return redirect('main:bi_services')


@login_required
def new_option_contract(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    username = kwargs.get('username')
    client_data = CustomerUser.objects.get(username=username)
    user = get_object_or_404(CustomerUser, username=username)
    today = date.today()
    plan_title = request.POST.get('service_title').lower() if request.method == 'POST' and request.POST.get('service_title') else None
    
    # plan = contract_charge = contract_duration = contract_period = None

    investments = Investments.objects.filter(client=user)
    latest_investment_rates = Investment_rates.objects.order_by('-created_date').first()
    
    (total_amount,protected_capital,amount_invested,
     bi_weekly_returns,number_positions,minimum_duration
     )=get_user_investment(investments,latest_investment_rates)
    print("minimum_duration======>",minimum_duration)
    context = {
        'client_data': client_data,
        'total_amount': total_amount,
        'protected_capital': protected_capital,
        'amount_invested': amount_invested,
        'bi_weekly_returns': bi_weekly_returns,
        'contract_duration': minimum_duration,
        'number_positions': number_positions,
        'contract_date': today.strftime("%d %B, %Y")
    }
    return render(request, 'management/contracts/client_investment_contract.html', context)

@login_required
def new_contract(request, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    # print("subtile--->",pre_sub_title)
    username = kwargs.get('username')
    client_data = CustomerUser.objects.get(username=username)
    today = date.today()
    plan_title = request.POST.get('service_title').lower() if request.method == 'POST' and request.POST.get('service_title') else None
    plan = contract_charge = contract_duration = contract_period = None
    try:
        if pre_sub_title:
            service_category_instance = ServiceCategory.objects.get(slug=pre_sub_title)
        else:
            return redirect('main:display_service')
    except ServiceCategory.DoesNotExist:
        return redirect('main:display_service')
    
    # Access the service_instance properties
    service_instance = Service.objects.filter(servicecategory__name=service_category_instance.name).first()
    if service_instance:
        service_title = service_instance.title
        service_title_uppercase = service_title.upper()
        service_description = service_instance.description
    else:
        print("No service found for the given pricing title.")
	
    plan = Pricing.objects.filter(category=service_category_instance.id, title__iexact=plan_title).first()
    if plan:
        contract_charge = plan.price
        contract_duration = plan.duration
        contract_period = plan.contract_length
        plan_id = plan.id
    context = {
        'service_title': service_title,
        'service_title_uppercase': service_title_uppercase,
        'client_data': client_data,
        'contract_data': plan,
        'contract_charge': contract_charge,
        'contract_duration': contract_duration,
        'contract_period': contract_period,
        'plan_id': plan_id,
        'contract_date': today.strftime("%d %B, %Y")
    }
    # if service_title_uppercase == 'INVESTING':
    #     return render(request, 'management/contracts/client_investment_contract.html', context)
    # 	return render(request, 'management/contracts/client_contract.html', context)
    # else:
    return render(request, 'management/contracts/client_contract.html', context)



# ==================PAYMENT CONFIGURATIONS VIEWS=======================
class PaymentConfigCreateView(LoginRequiredMixin, CreateView):
	model = PayslipConfig
	success_url = "/finance/paymentconfigs/"
	fields = "__all__"

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class PaymentConfigListView(ListView):
	model = PayslipConfig
	template_name = "finance/payments/paymentconfigs.html"
	context_object_name = "payconfigs"


class PaymentConfigUpdateView(UpdateView):
	model = PayslipConfig
	success_url = "/finance/paymentconfigs/"
	
	fields = "__all__"

	def form_valid(self, form):
		# form.instance.author=self.request.user
		if self.request.user.is_superuser:
			return super().form_valid(form)
		else:
			# return redirect("management:tasks")
			return render(request,"management/contracts/supportcontract_form.html")

	def test_func(self):
		# task = self.get_object()
		if self.request.user.is_superuser:
			return True
		# elif self.request.user == task.employee:
		#     return True
		return False


# ==================PAYMENTVIEWS=======================
class PaymentCreateView(LoginRequiredMixin, CreateView):
	model = Default_Payment_Fees
	success_url = "/finance/contract_form"
	fields = [
				"job_down_payment_per_month",
				"job_plan_hours_per_month",
				"student_down_payment_per_month",
				"student_bonus_payment_per_month",
	]
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

def payments(request):
	payment_history=Payment_History.objects.all()
	Payment_Info=Payment_Information.objects.all()
	# payment_history=Payment_History.objects.filter(customer__is_client=True)
	# Payment_Info=Payment_Information.objects.filter(customer_id__is_client=True)
	context={
		"title":"Payments",
		"payment_history":payment_history,
		"Payment_Info":Payment_Info
	}
	return render(request,"finance/payments/payments.html",context)


def payment(request,method):
    path_list,sub_title,pre_sub_title=path_values(request)
    subject='PAYMENT'
    url='email/payment/payment_method.html'
    message=f'Hi,{request.user.first_name}, an email has been sent \
            with {sub_title} details for your payment.In the unlikely event\
            that you have not received it, kindly \
            check your spam folder.'
    error_message=f'Hi,{request.user.first_name}, there seems to be an issue on our end.kindly contact us directly for payment details.'
    context={
                'subtitle': sub_title,
                'user': request.user.first_name,
                'mpesa_number':phone_number,
                'cashapp':cashapp,
                'venmo':venmo,
                'account_no':account_no,
                'email':email_info,
                'message':message,
                'error_message':error_message,
                'contact_message':'info@codanalytics.net',
            }
    try:
        send_email( category=request.user.category, 
                    to_email=[request.user.email,], 
                    subject=subject, html_template=url, 
		    		context=context
                    )
        return render(request, "email/payment/payment_method.html",context)
    except:
        return render(request, "email/payment/payment_method.html",context)
    

# def send_invoice(request):
#     service='Training and Job Support'
#     url="email/payment/invoice.html"

#     ###############################
#     # due payment userlist
#     ###############################
#     user_payment_information = Payment_Information.objects.filter(fee_balance__gt=0).distinct('customer_id')
#     for customer_payment_information in user_payment_information:
#         if PayslipConfig.objects.filter(user__username=customer_payment_information.customer_id.username).exists():
#             payslip_config = PayslipConfig.objects.get(user__username=customer_payment_information.customer_id.username)
#         else:
#             payslip_config = PayslipConfig.objects.create(
#                 user = customer_payment_information.customer_id,
#                 loan_amount = customer_payment_information.payment_fees,
#                 loan_repayment_percentage = 0,
#                 installment_amount = customer_payment_information.down_payment,
#             )

#         organization = Company.objects.filter(user__username=customer_payment_information.customer_id.username)
#         client=CustomerUser.objects.get(username=customer_payment_information.customer_id.username)
#         client_email=client.email
#         today = datetime.now()
#         date=datetime(today.year, today.month, 1)
#         # debt_amount=payslip_config.loan_amount
#         # repayment_percentage=payslip_config.loan_repayment_percentage
#         # repayment_amount = debt_amount * repayment_percentage if repayment_percentage >0.0 else 1000
#         # balance_amount=debt_amount-repayment_amount
#         debt_amount=customer_payment_information.fee_balance
#         repayment_amount=payslip_config.installment_amount
#         balance_amount=debt_amount-repayment_amount

#         context={
#                     'service': service,
#                     'date': date,
#                     'first_name': client.first_name,
#                     'last_name': client.last_name,
#                     'organization': organization.first().name if organization.exists() else 'CODA',
#                     'address':client.address,
#                     'city':client.city,
#                     'state':client.state,
#                     'country':client.country,
#                     'zipcode':client.zipcode,
#                     'account_no':account_no,
#                     'user_email':client.email,
#                     'debt_amount':debt_amount,
#                     'repayment_amount':repayment_amount,
#                     'balance_amount':balance_amount,
#                     'email':email_info,
#                     'message':"message",
#                     'error_message':"error_message",
#                     'contact_message':'info@codanalytics.net',
#                 }
#         try:
#             send_email( category=request.user.category, 
#                         to_email=[client_email],#[request.user.email,], 
#                         subject=service, html_template=url, 
#                         context=context
#                         )
#             # return render(request, "email/payment/invoice.html",context)
#         except:
#               pass
#     return render(request, "email/payment/invoice.html",context)


def send_invoice(request):
    service='Training and Job Support'
    url="email/payment/invoice.html"

    ###############################
    # due payment userlist
    ###############################
    user_payment_information = Payment_History.objects.filter(fee_balance__gt=0).distinct('customer_id')
    
    successful_user_list = []
    
    for customer_payment_information in user_payment_information:
        if PayslipConfig.objects.filter(user__username=customer_payment_information.customer.username).exists():
            payslip_config = PayslipConfig.objects.get(user__username=customer_payment_information.customer.username)
            # print("payslip_config====>",payslip_config)
        else:
            payslip_config = PayslipConfig.objects.create(
                user = customer_payment_information.customer,
                loan_amount = customer_payment_information.payment_fees,
                loan_repayment_percentage = 0,
                rp_starting_period= customer_payment_information.contract_submitted_date.strftime("%Y-%m-%d"),
                installment_amount = customer_payment_information.down_payment,
                installment_date = datetime.now().date()
            )

        if payslip_config.installment_date and payslip_config.installment_date.day == datetime.today().date().day:
            organization = Company.objects.filter(user__username=customer_payment_information.customer.username)
            client=customer_payment_information.customer
            client_email=client.email
            today = datetime.now()
            date=datetime(today.year, today.month, 1)
            debt_amount=customer_payment_information.fee_balance
            repayment_amount=payslip_config.installment_amount
            balance_amount=debt_amount-repayment_amount if debt_amount-repayment_amount > 0 else debt_amount

            context={
                        'service': service,
                        'date': date,
                        'first_name': client.first_name,
                        'last_name': client.last_name,
                        'organization': organization.first().name if organization.exists() else f"{client.first_name} {client.last_name}",
                        'address':client.address if client.address is not None else '',
                        'city':client.city if client.city is not None else '',
                        'state':client.state if client.state is not None else '',
                        'country':client.country if client.country is not None else '',
                        'zipcode':client.zipcode if client.zipcode is not None else '',
                        'account_no':account_no,
                        'user_email':client.email,
                        'debt_amount':debt_amount,
                        'repayment_amount':repayment_amount,
                        'balance_amount':balance_amount,
                        'email':email_info,
                        'message':"sucess",
                        'error_message':"error_message",
                        'contact_message':'info@codanalytics.net',
                    }
            try:
                send_email( category=request.user.category, 
                            to_email=[client_email],#[request.user.email,], 
                            subject=service, html_template=url, 
                            context=context
                            )                
                successful_user_list.append(context)
                # return render(request, "email/payment/invoice.html",context)
            except:
                pass

    return render(request, "finance/payments/sendinvoice.html",{'customer_payment_information': successful_user_list})
    

@login_required
def pay(request, *args, **kwargs):
    contract_url = reverse('finance:newcontract', args=[request.user.username])
    payment_info = None
    # try:
    #     payment_info = Payment_Information.objects.get(customer_id=request.user.id)
    # except Payment_Information.DoesNotExist:
    if request.method == 'POST' and request.POST.get('fees'):
        total_fee = float(request.POST.get('fees'))
        
        if not request.POST.get('is_direct', False):
            downpayment = total_fee * 0.30
        else:
            downpayment = total_fee
        fee_balance = total_fee - downpayment
        payment_info = Payment_Information.objects.create(
            customer_id=request.user,
            payment_fees=total_fee,
            down_payment=downpayment,
            student_bonus=0,
            plan=request.POST.get('service_category_id', 999), # added service_category id
			subplan=request.POST.get('subplan_id', None),
			pricing_plan=request.POST.get('pricing_serial', None),
            fee_balance=fee_balance,
            payment_method='mpesa',
            contract_submitted_date=date.today(),
            client_signature="client",
            company_rep="coda",
            client_date=date.today(),
            rep_date=date.today(),
        )
    else:
        try:
	        
            payment_info = Payment_Information.objects.filter(customer_id=request.user.id).order_by('-contract_submitted_date').first()
        except:
            # Redirect for specific user categories or to contract signing view
            if request.user.category == 5:
                return redirect('main:layout')
            else:
                # Need modification to take the user to interested page.
                return redirect('main:layout')

    # Calculate PayPal charges
    paypal_charges = calculate_paypal_charges(payment_info.down_payment) if payment_info else 0

    context = {
        "title": "PAYMENT",
        'payments': payment_info,
        'paypal_charges': paypal_charges,
        "message": f"Hi {request.user}, you are yet to sign the contract with us. Kindly contact us at info@codanalytics.net.",
        "link": contract_url,
    }

    return render(request, "finance/payments/pay.html", context)


def paymentComplete(request):
    payments = Payment_Information.objects.filter(customer_id=request.user.id).first()
    customer = request.user
    body = json.loads(request.body)
    payment_fees = body["payment_fees"]
    down_payment = payments.down_payment
    studend_bonus = payments.student_bonus
    plan = payments.plan
    subplan = payments.subplan
    pricing_plan = payments.pricing_plan
    fee_balance = payments.fee_balance
    payment_mothod = payments.payment_method
    contract_submitted_date = payments.contract_submitted_date
    client_signature = payments.client_signature
    company_rep = payments.company_rep
    client_date = payments.client_date
    rep_date = payments.rep_date
    Payment_History.objects.create(
        customer=customer,
        payment_fees=payment_fees,
        down_payment=down_payment,
        student_bonus=studend_bonus,
        plan=plan,
		subplan=subplan,
		pricing_plan=pricing_plan,
        fee_balance=fee_balance,
        payment_method=payment_mothod,
        contract_submitted_date=contract_submitted_date,
        client_signature=client_signature,
        company_rep=company_rep,
        client_date=client_date,
        rep_date=rep_date,
    )
    try:
        if PayslipConfig.objects.filter(user__username=request.user.username).exists():
            payslip_config = PayslipConfig.objects.get(user__username=request.user.username)
            payslip_config.loan_amount = payment_fees
            payslip_config.installment_amount = down_payment
            payslip_config.save()

        else:
            payslip_config = PayslipConfig.objects.create(
                user = request.user.customer_id,
                loan_amount = payment_fees,
                loan_repayment_percentage = 0,
                installment_amount = down_payment,
            )
    except:
        pass
	
    return JsonResponse("Payment completed!", safe=False)

class DefaultPaymentListView(ListView):
	model = Default_Payment_Fees
	template_name = "finance/payments/defaultpayments.html"
	context_object_name = "defaultpayments"

class DefaultPaymentUpdateView(UpdateView):
	model = Default_Payment_Fees
	success_url = "/finance/payments"
	
	fields = [
				"job_down_payment_per_month",
				"job_plan_hours_per_month",
				"student_down_payment_per_month",
				"student_bonus_payment_per_month",
				"loan_amount",
	]
	# fields=['user','activity_name','description','point']
	def form_valid(self, form):
		# form.instance.author=self.request.user
		if self.request.user.is_superuser:
			return super().form_valid(form)
		else:
			# return redirect("management:tasks")
			return render(request,"management/contracts/supportcontract_form.html")

	def test_func(self):
		task = self.get_object()
		if self.request.user.is_superuser:
			return True
		# elif self.request.user == task.employee:
		#     return True
		return False

# For payment purposes
# from django.shortcuts import render, get_object_or_404, redirect
# from django.forms.models import modelform_factory

# def update_table(request, table_id, model_class):
#     table = get_object_or_404(model_class, id=table_id)
#     FormClass = modelform_factory(model_class, exclude=['id'])  # Exclude 'id' field if it's an auto-generated primary key
#     if request.method == 'POST':
#         form = FormClass(request.POST, instance=table)
#         if form.is_valid():
#             form.save()
#             return redirect('finance:pay')  # Redirect to the appropriate URL
#     else:
#         form = FormClass(instance=table)
#     return render(request, 'main/snippets_templates/generalform.html', {'form': form})

class PaymentInformationUpdateView(UpdateView):
	model = Payment_Information
	success_url = "/finance/pay/"
	template_name="main/snippets_templates/generalform.html"
	
	fields ="__all__"
	# fields=['customer_id','down_payment']
	def form_valid(self, form):
		# form.instance.author=self.request.user
		# if self.request.user.is_superuser or self.request.user:
		if self.request.user is not None:
			return super().form_valid(form)
		else:
			# return redirect("management:tasks")
			return render(request,"main/snippets_templates/generalform.html")

	def test_func(self):
		task = self.get_object()
		# if self.request.user.is_superuser:
		# 	return True
		# elif self.request.user == task.employee:
		if self.request.user:
		    return True


# ----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------
@login_required
def transact(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            instance=form.save(commit=False)
            instance.sender=request.user
            instance.save()
            return redirect("/finance/transaction/")
    else:
        form = TransactionForm()
    return render(request, "finance/payments/transact.html", {"form": form})

@login_required
def add_budget_item(request):
    if request.method == "POST":
        form = BudgetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            instance=form.save(commit=False)
            print(request.user)
            instance.budget_lead=request.user
            instance.save()
            return redirect("/finance/budget/")
    else:
        form = BudgetForm()
    return render(request, "finance/budgets/newbudget.html", {"form": form})

class TransactionListView(ListView):
	model = Transaction
	template_name = "finance/payments/transaction.html"
	context_object_name = "transactions"
	# ordering=['-transaction_date']

def filteroutflowsbydepartment(request):
    all_outflows = Transaction.objects.all().order_by('-id')
    if request.method == "POST":
        form = DepartmentFilterForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['name']
            # print("department=====>",department)
            filtered_outflows = Transaction.objects.filter(department__name=department).order_by('-id')
            count_filtered_outflows = Transaction.objects.filter(department__name=department).count()
            # print("filtered_outflows=====>",count_filtered_outflows)
	    
            outflows=filtered_outflows
        return outflows,form
    else:
        form = DepartmentFilterForm()
        outflows=all_outflows
        return outflows,form


def outflows(request):
    outflows,form=filteroutflowsbydepartment(request)
    # print("values========>",outflows,form)
    ytd_duration,current_year,first_date=dates_functionality()
    webhour, delta = PayslipConfig.objects.values_list("web_pay_hour", "web_delta").first()
    #operations totals
    operations_obj = outflows
    ytd_transactions = operations_obj.filter(activity_date__year=current_year)
    ytd_op_outflow = sum(transact.amount*transact.qty for transact in ytd_transactions)
    total_op_outflows = sum(transact.amount*transact.qty for transact in operations_obj)
    total_op_outflows_usd =float(total_op_outflows)/float(rate)
    ytd_op_outflow_usd=float(ytd_op_outflow)/float(rate)
    
    # website_totals
    web_obj = Requirement.objects.all()
    web_obj_done = Requirement.objects.filter(is_reviewed=False)
    ytd_requirements = Requirement.objects.filter(created_at__year=current_year,is_reviewed=False)
    ytd_web_ouflow = sum(req.duration * delta * webhour for req in ytd_requirements)
    total_web_ouflow = sum(req.duration * delta * webhour for req in web_obj_done)
    total_web_duration=(x.duration * delta for x in web_obj_done)
    
    # field_totals
    field_obj = Field_Expense.objects.all()
    ytd_field_obj = Field_Expense.objects.filter(date__year=current_year)
    ytd_field_ouflow = sum(transact.transactions_amt for transact in ytd_field_obj)
    total_field_ouflow = sum(transact.transactions_amt for transact in field_obj)
    total_field_ouflow_usd =float(total_field_ouflow)/float(rate)
    ytd_field_ouflow_usd=float(ytd_field_ouflow)/float(rate)

    total_outflows = float(total_op_outflows_usd) + float(total_web_ouflow) + float(total_field_ouflow_usd)
    ytd_outflows = float(ytd_op_outflow_usd) + float(ytd_web_ouflow) + float(ytd_field_ouflow_usd)
    
    # print("Amounts",total_outflows,ytd_outflows,total_field_ouflow_usd,total_web_ouflow,total_field_ouflow_usd)
    
    avg_daily_expenditure=ytd_outflows/ytd_duration
    avg_hourly_expenditure=avg_daily_expenditure/12
    avg_minute_expenditure=avg_hourly_expenditure/60
    avg_second_expenditure=avg_minute_expenditure/60
    avg_monthly_expenditure=avg_daily_expenditure*30
    avg_quarterly_expenditure=avg_monthly_expenditure*3
    
    data = [
        {"title": "Operations", "value": total_op_outflows_usd},
        {"title": "Web Development", "value": total_web_ouflow},
        {"title": "Makutano Office", "value": total_field_ouflow_usd},
        {"title": "Year_To_Date", "value": ytd_outflows},
        {"title": "Quarterly", "value": avg_quarterly_expenditure},
        {"title": "Monthly", "value": avg_monthly_expenditure},
        {"title": "Daily", "value": avg_daily_expenditure},
        {"title": "Hourly", "value": avg_hourly_expenditure},
	]

    outflow_context = {
        "transactions": operations_obj,
        "web_transactions": web_obj,
        "field_transactions": field_obj,
        "total_amt": total_outflows,
        "data": data,
        # "balance": balance,
        "webhour": webhour,
        "delta": delta,
        "remaining_days": remaining_days,
        "remaining_seconds ": int(remaining_seconds % 60),
        "remaining_minutes ": int(remaining_minutes % 60),
        "remaining_hours": int(remaining_hours % 24),
        "form": form,
    }
    return render(request,"finance/payments/transaction.html",outflow_context)



@method_decorator(login_required, name="dispatch")
class TransanctionDetailView(DetailView):
	template_name = "finance/payments/transaction_detail.html"
	model = Transaction
	ordering = ["-transaction_date"]


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Transaction
	# success_url="/finance/transaction"
	fields = [
		"sender",
		"receiver",
		"phone",
		"department",
		"category",
		"type",
		"payment_method",
		"qty",
		"amount",
		"transaction_cost",
		"description",
		"receipt_link",
	]
	form = TransactionForm()

	def form_valid(self, form):
		form.instance.username = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse("finance:transaction-list")

	def test_func(self):
		inflow = self.get_object()
		if self.request.user == inflow.sender:
			return True
		elif self.request.user.is_admin or self.request.user.is_superuser:
			return True
		return False

@method_decorator(login_required, name="dispatch")
class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Transaction
	success_url = "/finance/transaction"

	def test_func(self):
		transaction = self.get_object()
		if self.request.user == transaction.sender:
			return True
		elif self.request.user.is_superuser or self.request.user.is_admin:
			return True
		return False
		
# ----------------------CASH INFLOW CLASS-BASED VIEWS--------------------------------
def inflow(request):
	if request.method == "POST":
		form = InflowForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.sender = request.user
			form.save()
			return redirect("/finance/inflows/")
	else:
		form = InflowForm()
	return render(
		request, "finance/company_finances/inflow_entry.html", {"form": form}
	)

@method_decorator(login_required, name="dispatch")
class InflowDetailView(DetailView):
	template_name = "finance/cash_inflow/inflow_detail.html"
	model = Inflow
	ordering = ["-transaction_date"]


def inflows(request):
	inflows = Inflow.objects.all().order_by("-transaction_date")
	total = Inflow.objects.all().aggregate(Total_Cashinflows=Sum("amount"))
	revenue = total.get("Total_Cashinflows")
	context = {"inflows": inflows, "revenue": revenue}
	return render(request, "finance/cash_inflow/inflows.html", context)


@method_decorator(login_required, name="dispatch")
class UserInflowListView(ListView):
	model = Inflow
	template_name = "finance/cash_inflow/user_inflow.html"
	context_object_name = "inflows"
	ordering = ["-transaction_date"]

@method_decorator(login_required, name="dispatch")
class InflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Inflow
	success_url = "/finance/inflow"
	fields = [
		"sender",
		"receiver",
		"phone",
		"category",
		"task",
		"method",
		"period",
		"qty",
		"amount",
		"transaction_cost",
		"description",
	]

	def form_valid(self, form):
		form.instance.sender = self.request.user
		return super().form_valid(form)

	def test_func(self):
		inflow = self.get_object()
		if self.request.user == inflow.sender:
			return True
		return False

@method_decorator(login_required, name="dispatch")
class InflowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Inflow
	success_url = "/finance/inflow"

	def test_func(self):
		inflow = self.get_object()
		# if self.request.user == inflow.sender:
		if self.request.user.is_superuser:
			return True
		return False


# ============LOAN VIEWS========================
class LoanCreateView(LoginRequiredMixin, CreateView):
	model = PayslipConfig
	success_url = "/finance/loans"
	fields = "__all__"
	form = LoanForm()

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

def admin_loan_data_modified(form, username, user_data):
	previous_balance_amount = user_data.order_by('-id')[0].balance_amount
	try:
		employee = CustomerUser.objects.get(username=username)
	except:
		employee=None
	data = form.cleaned_data
	if previous_balance_amount != data['balance_amount']:
		loan_data = TrainingLoan(
			user=employee,
			category="Debit",
			amount=data['amount'],
			# created_at,
			# updated_at=2022-10-10,
			# is_active,
			training_loan_amount=data['training_loan_amount'],
			total_earnings_amount=data['total_earnings_amount'],
			# deduction_date,
			deduction_amount=data['deduction_amount'],
			balance_amount=data['balance_amount'],
		)
		loan_data.save()
		return loan_data
	return None

class LoanUpdateView(UpdateView):
	model = TrainingLoan
	success_url = "/finance/loans"
	fields="__all__"

	def form_valid(self, form):
		# form.instance.user=self.request.user
		if self.request.user.is_superuser:
			user_data = TrainingLoan.objects.filter(id=self.kwargs['pk'], is_active=True)
			username=user_data.order_by('-id')[0].user.username
			admin_loan_data_modified(form=form, username=username, user_data=user_data)
			return redirect("finance:trainingloans")
		else:
			return redirect("finance:trainingloans")
			# return render(request,"management/contracts/supportcontract_form.html")

	def test_func(self):
		# task = self.get_object()
		if self.request.user.is_superuser:
			return True
		# elif self.request.user == task.employee:
		#     return True
		return False

class LoanListView(ListView):
	model = TrainingLoan
	template_name = "finance/payments/loans.html"
	context_object_name = "payments"
	ordering = ['created_at']

class userLoanListView(ListView):
	model = LoanUsers
	template_name = "finance/payments/loanpage.html"
	context_object_name = "loans"


# ==================================TESTING FOOD VIEWS==========================
@method_decorator(login_required, name="dispatch")
class FoodCreateView(LoginRequiredMixin, CreateView):
    model = Food
    success_url = "/finance/food"
    fields = "__all__"

    def form_valid(self, form):
        if self.request.user:
            return super().form_valid(form)

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    success_url = "/finance/food"
    fields = "__all__"

    def form_valid(self, form):
        if self.request.user:
            return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class SupplierUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Supplier
    success_url = "/finance/food"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    fields = "__all__"

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        Supplier = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == Supplier.added_by:
            return True
        return redirect("finance:supplies")


@method_decorator(login_required, name="dispatch")
class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    success_url = "/finance/food"
    fields = "__all__"

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        Food = self.get_object()
        if self.request.user.is_superuser:
            return True
        # elif self.request.user == Food.added_by:
        elif self.request.user:
            return True
        return redirect("finance:supplies")


class SupplierListView(ListView):
    model = Supplier
    template_name = "finance/payments/food.html"
	
    context_object_name = "suppliers"
    ordering = ["-created_at"]
    

def foodlist(request):
    supplies = Food.objects.all().order_by("-id")
    food_filters=FoodFilter(request.GET,queryset=supplies)

    total_amt = 0
    for supply in supplies:
        total_amt = total_amt + supply.total_amount

    total_add_amount = 0
    for supply in supplies:
        total_add_amount = total_add_amount + supply.additional_amount

    context={
        "total_add_amount": total_add_amount,
        "total_amt": total_amt,
        "supplies": supplies,
        "food_filters": food_filters
    }
    return render(request,"finance/payments/food.html",context)

def food_history_view(request):    
    date_today = timezone.now()
    current_year = date_today.year
    current_month = date_today.month
    query = Q()

    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    selected_office_location = request.GET.get('office_location')

    if selected_month and selected_month.isdigit():
        query &= Q(history_date__month=selected_month)
    if selected_year and selected_year.isdigit():
        query &= Q(history_date__year=selected_year)
    if selected_office_location:
        query &= Q(office_location=selected_office_location)

    food_histories = FoodHistory.objects.filter(query).order_by('-history_date')
    total_amount = FoodHistory.objects.filter(query).aggregate(
        total=Sum(F('unit_amt') * F('qty'))
    )['total'] or 0

    unique_office_locations = Food.objects.order_by('office_location').values_list('office_location', flat=True).distinct()
    years = list(range(current_year - 5, current_year + 1))
    months = [(i, timezone.datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    context = {
        'food_histories': food_histories,
        'unique_office_locations': unique_office_locations,
        'months': months,
        'years': years,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'total_amount': total_amount,
    }

    return render(request, 'finance/payments/foodhistory.html', context)


def food_history_update(request,pk):
    food_histories= get_object_or_404(FoodHistory,pk=pk)
    if request.method == 'POST':                 
        form = FoodHistoryForm(request.POST,instance=food_histories)
        if form.is_valid():
            form.save() 
            return redirect('finance:foodhistory')            
    else:
        form = FoodHistoryForm(instance=food_histories)
    return render(request,"finance/payments/foodhistory_update.html",{'form':form,'food_histories':food_histories}) 

# =========================DC 48 KENYA===================================
@method_decorator(login_required, name="dispatch")
class DC48InflowCreateView(LoginRequiredMixin, CreateView):
    model = DC48_Inflow
    success_url = "/finance/listinflow"
    template_name="finance/payments/inflow_form.html"
    # fields =("receiver",
    #         "phone",
    #         "category",
    #         "task",
    #         "method",
    #         "period",
    #         "qty",
    #         "amount",
    #         "transaction_cost",
    #         "description",
	#    )
    fields ="__all__"
    exclude='transaction_date'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class DC48InflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DC48_Inflow
    template_name="finance/payments/inflow_form.html"
    success_url = "/finance/listinflow"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    # fields =("receiver",
    #         "phone",
    #         "category",
    #         "task",
    #         "method",
    #         "period",
    #         "qty",
    #         "amount",
    #         "transaction_cost",
    #         "description",
	#    )
    fields ="__all__"
    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        # DC48_Inflow = self.get_object()
        if self.request.user.is_superuser or self.request.user:
            return True
        return redirect("data:training-list")

@method_decorator(login_required, name="dispatch")
class DC48InflowDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DC48_Inflow
    success_url = "/finance/listinflow/"
    template_name="finance/payments/inflow_confirm_delete.html"
    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False
    
@login_required
def clientinflows(request, user=None, *args, **kwargs):
	try:
		client = get_object_or_404(User, username=kwargs.get("username"))
		transactions = DC48_Inflow.objects.filter(sender=client, is_active=True)
		total_members = transactions.count()
		paid_members = transactions.filter(has_paid=True).count()
		total_amt = 0
		total_paid = 0
		for transact in transactions:
			print("clients_category",transact.clients_category)
			total_amt += transact.total_payment
			if transact.has_paid:
				total_paid += transact.total_paid
		
		pledged = total_amt - total_paid
		amount_ksh = total_amt * rate  # Initialize amount_ksh outside the if block
		context = {
			"message":"Kindly contact adminstrator info@codanalytics.net",
			"transactions": transactions,
			"total_count": total_members,
			"paid_count": paid_members,
			"total_amt": total_amt,
			"amount_ksh": amount_ksh,
			"total_paid": total_paid,
			"pledged": pledged,
			"rate": rate,
			"remaining_days": remaining_days,
			"remaining_seconds ": int(remaining_seconds % 60),
			"remaining_minutes ": int(remaining_minutes % 60),
			"remaining_hours": int(remaining_hours % 24),
		}
		return render(request, "finance/payments/dcinflows.html", context)
	except:
		return render(request, "main/errors/template_error.html",context)
    
@login_required
def dcinflows(request):
    (remaining_days, remaining_seconds, remaining_minutes, remaining_hours) = countdown_in_month()
    usd_to_kes = get_exchange_rate('USD', 'KES')
    rate = round(Decimal(usd_to_kes), 2)
    
    if request.user.sub_category == 7 or request.user.is_superuser:
        transactions = DC48_Inflow.objects.filter(clients_category="DYC")
        total_members = transactions.filter(clients_category="DYC").count()
        paid_members = transactions.filter(clients_category="DYC", has_paid=True).count()
        total_amt = 0
        total_paid = 0
    else:
        transactions = DC48_Inflow.objects.filter(clients_category="DC48KENYA")
        total_members = transactions.filter(clients_category="DC48KENYA").count()
        paid_members = transactions.filter(clients_category="DC48KENYA", has_paid=True).count()
        total_amt = 0
        total_paid = 0
        
    amount_ksh = 0  # Assign a default value of 0
    receipt_url = ''
    for transact in transactions:
        # print("receipturl",transact.receipturl)
        total_amt += transact.total_payment
        if transact.has_paid:
            total_paid += transact.total_paid
        if transact.receipturl:
            receipt_url=transact.receipturl
        else:
            return redirect('main:404error')
    
    pledged = total_amt - total_paid
    amount_ksh = total_amt * rate  # Initialize amount_ksh outside the if block
    
    context = {
        "transactions": transactions,
        "total_count": total_members,
        "paid_count": paid_members,
        "total_amt": total_amt,
        "amount_ksh": amount_ksh,
        "total_paid": total_paid,
        "pledged": pledged,
        "rate": rate,
        "remaining_days": remaining_days,
        "remaining_seconds ": int(remaining_seconds % 60),
        "remaining_minutes ": int(remaining_minutes % 60),
        "remaining_hours": int(remaining_hours % 24),
        "receipt_url": receipt_url,
    }
    return render(request, "finance/payments/dcinflows.html", context)




# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

def MpesaPaymentView(request):
    context = {}

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        user_email = request.user.email  # Replace with the actual path to the user's email
        print('user_email: ', user_email)
        otp = generate_and_send_otp(user_email)
        print('otp: ', otp)

        request.session['phone_number'] = phone_number
        
        request.session['payment_otp'] = otp
        return redirect('finance:otp_confirmation')
    else:
        payment_info = Payment_Information.objects.filter(customer_id=request.user.id).first()
        downpayment = payment_info.down_payment
        paypal_charges = calculate_paypal_charges(downpayment)
        request.session['amount'] = downpayment
        
        reference = f"MPESA-{request.session.get('phone_number')}-{request.session.get('amount')}"
        request.session['reference'] = reference
        context = {"payment": payment_info, 'paypal_charges': paypal_charges,} 
        return render(request, 'finance/payments/mpesa_payment.html', context)

# views.py
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('payment_otp')
        phone_number = request.session.get('phone_number')
        amount = request.session.get('amount')
        reference = request.session.get('reference')
        # print("Phone Number:", phone_number)
        # print("Amount:", amount)
        # print("reference:", reference)
        

        # Debugging: Print entered and stored OTP to console
        # print("Entered OTP:", entered_otp)
        # print("Stored OTP:", stored_otp)

        if entered_otp == stored_otp:
            print("_______correct")
            # If OTP is verified, proceed with payment initiation
            payment_data = []
            if not payment_data:
                print("____________________paymrnt_data", payment_data)
                response = initiate_payment(phone_number, amount, reference)
                print(response, "______________Response")
                if ("ResponseCode" in response) and (response['ResponseCode'] == "0"):
                    payment_info = Payment_Information.objects.get(customer_id=request.user.id)
                    Payment_History.objects.create(
                        customer=request.user,
                        payment_fees=payment_info.payment_fees,
                        down_payment=payment_info.down_payment,
                        student_bonus=payment_info.student_bonus,
                        plan=payment_info.plan,
                        fee_balance=payment_info.fee_balance,
                        payment_method="M-pesa",
                        contract_submitted_date=payment_info.contract_submitted_date,
                        client_signature=payment_info.client_signature,
                        company_rep=payment_info.company_rep,
                        client_date=payment_info.client_date,
                        rep_date=payment_info.rep_date,
                    )
                if response.get('ResponseCode') == '0':
                    messages.success(request, 'Payment initiated successfully.')
                    return redirect('finance:payment_success')  # Redirect to success page
                else:
                    messages.error(request, 'Failed to initiate payment.')
                    return redirect('finance:payment_failed')  # Redirect to failed page
            else:
                messages.error(request, 'Payment data not found. Please try again.')
                return redirect('finance:payment_failed')  # Redirect to failed page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('finance:payment_failed')  # Redirect to failed page

    return render(request, 'finance/payments/otp_confirmation.html')

def payment_success(request):
    return render(request, 'finance/payments/success.html')

def payment_failed(request):
    return render(request, 'finance/payments/failed.html')


def get_existing_data():
    existing_assets = BalanceSheetCategory.objects.filter(category_type='Asset')
    existing_long_term_assets = BalanceSheetCategory.objects.filter(category_type='Long-term Asset')
    existing_liabilities = BalanceSheetCategory.objects.filter(category_type='Liability')
    existing_long_term_liabilities = BalanceSheetCategory.objects.filter(category_type='Long-term Liability')

    total_current_assets = existing_assets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_long_term_assets = existing_long_term_assets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_current_liabilities = existing_liabilities.aggregate(Sum('amount'))['amount__sum'] or 0
    total_long_term_liabilities = existing_long_term_liabilities.aggregate(Sum('amount'))['amount__sum'] or 0

    return (
        existing_assets.exists() and existing_long_term_assets.exists() and
        existing_liabilities.exists() and existing_long_term_liabilities.exists(),
        existing_assets, existing_long_term_assets, existing_liabilities, existing_long_term_liabilities,
        total_current_assets, total_long_term_assets, total_current_liabilities, total_long_term_liabilities
    )

def openai_balancesheet(request):
    context = {}  # Initialize context variable

    try:
        (
            data_exists,
            existing_assets, existing_long_term_assets, existing_liabilities, existing_long_term_liabilities,
            total_current_assets, total_long_term_assets, total_current_liabilities, total_long_term_liabilities
        ) = get_existing_data()

        # Check if data already exists in the model
        if data_exists:
            # Use existing data
            print("Using existing data")
            context = {
                'company_name': 'CODA',
                'assets': existing_assets,
                'long_term_assets': existing_long_term_assets,
                'liabilities': existing_liabilities,
                'long_term_liabilities': existing_long_term_liabilities,
                'total_current_assets': total_current_assets,
                'total_long_term_assets': total_long_term_assets,
                'total_current_liabilities': total_current_liabilities,
                'total_long_term_liabilities': total_long_term_liabilities,
                'total_assets': total_current_assets + total_long_term_assets,
                'total_liabilities': total_current_liabilities + total_long_term_liabilities,
            }
        else:
            try:
                response = fetch_and_process_financial_data(request)

                # Use the newly generated data
                context = {
                    'assets': response['assets'],
                    'long_term_assets': response['long_term_assets'],
                    'liabilities': response['liabilities'],
                    'long_term_liabilities': response['long_term_liabilities']
                }

            except json.JSONDecodeError as e:
                # Handle JSON parsing error
                print(f"Error processing OpenAI response: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")

    # Calculate total revenues
	# Get existing revenue and expenses data
    (
        data_exist,
		existing_revenue,existing_expenses,total_revenue, total_expenses,net_income

    ) = get_existing_revenue_expenses_data()

    if  data_exist:
        context.update({
            'existing_revenue_data': existing_revenue,
            'existing_expenses_data': existing_expenses,
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
			"net_income": net_income,
        })
    else:
        response = calculate_revenue_and_expenses(request)
        data = response.json() if hasattr(response, 'json') else json.loads(response.content.decode('utf-8'))

        context.update({
            'total_revenue': data.get('total_revenue', 0),
            'total_expenses': data.get('total_expenses', 0),
            'net_income': data.get('net_income', 0),
            'revenue_breakdown': data.get('revenue_breakdown', {}),
            'expense_breakdown': data.get('expense_breakdown', {}),
        })
# Render the template with the 'assets' variable
    return render(request, "finance/reports/openai.html", context)




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

    return render(request, "finance/reports/balancesheet.html", context)





from unicodedata import category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum
from django.http import QueryDict, Http404, JsonResponse
from requests import request
from datetime import datetime,date
from django.views.generic import (
	CreateView,
	ListView,
	UpdateView,
	DetailView,
	DeleteView,
)
from accounts.forms import UserForm
from accounts.models import CustomerUser
from .models import (
		LoanUsers, Payment_Information,Payment_History,
		Default_Payment_Fees,TrainingLoan,
		Inflow,Transaction,PayslipConfig
	)
from .forms import LoanForm,TransactionForm,InflowForm
# User=settings.AUTH_USER_MODEL
from management.utils import paymentconfigurations
from management.views import loan_update_save
from management.utils import loan_computation

from management.views import pay

User = get_user_model()

# Create your views here.

def finance(request):
    return render(request, "finance/reports/finance.html", {"title": "Finance"})

#================================STUDENT AND JOB SUPPORT CONTRACT FORM SUBMISSION================================
def contract_form_submission(request):
	try:
		if request.method == "POST":
			user_student_data = request.POST.get('usr_data')
			student_dict_data = QueryDict(user_student_data)
			username = student_dict_data.get('username')
			try:
				customer=CustomerUser.objects.get(username=username)
				ss= customer.id
				payment = Payment_Information.objects.get(customer_id_id=customer.id)
			except:
				customer = None
				payment = None
			if not payment:
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
				if form.is_valid():
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
			if payment:
				messages.success(request, f'Added New Contract For the {username}!')
				return redirect('accounts:user-list', username=request.user)
			else:
				messages.success(request, f'Account created for {username}!')
				return redirect('data:bitraining')
	except Exception as e:
		print("Student Form Creation Error ==>",print(e))

def mycontract(request, *args, **kwargs):
	username = kwargs.get('username')
	client_data=CustomerUser.objects.get(username=username)
	check_default_fee = Default_Payment_Fees.objects.all()
	if check_default_fee:
		default_fee = Default_Payment_Fees.objects.get(id=1)
	else:
		default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
				job_plan_hours_per_month=40,
				student_down_payment_per_month=500,
				student_bonus_payment_per_month=100)
		default_payment_fees.save()
		default_fee = Default_Payment_Fees.objects.get(id=1)
		
	if Payment_Information.objects.filter(customer_id_id=client_data.id).exists():
		payemnt_details = Payment_Information.objects.get(customer_id_id=client_data.id)
		contract_date = payemnt_details.contract_submitted_date.strftime("%d %B, %Y")
		if client_data.category == 3 and client_data.sub_category == 1:
			plan_dict = {"1":40,"2":80,"3":120}
			selected_plan = plan_dict[str(payemnt_details.plan)]
			job_support_hours = selected_plan - 30
			return render(request, 'my_supportcontract_form.html',{'job_support_data': client_data,'contract_date':contract_date,'payment_data':payemnt_details,"selected_plan":selected_plan,"job_support_hours":job_support_hours})
		if client_data.category == 3 and client_data.sub_category == 2:
			return render(request, 'my_trainingcontract_form.html',{'student_data': client_data,'contract_date':contract_date,'payment_data':payemnt_details})
		else:
			# return render(request, 'templates\errors\403.html')
			raise Http404("Login/Wrong Page: Are You a Client?")
	else:
		return render(request, 'contract_error.html',{'username':username})
		
@login_required
def newcontract(request, *args, **kwargs):
	username = kwargs.get('username')
	client_data=CustomerUser.objects.get(username=username)
	check_default_fee = Default_Payment_Fees.objects.all()
	if check_default_fee:
		default_fee = Default_Payment_Fees.objects.get(id=1)
	else:
		default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
				job_plan_hours_per_month=40,
				student_down_payment_per_month=500,
				student_bonus_payment_per_month=100)
		default_payment_fees.save()
		default_fee = Default_Payment_Fees.objects.get(id=1)
	today = date.today()
	contract_date = today.strftime("%d %B, %Y")

	if client_data.category == 3 and client_data.sub_category == 1:
		return render(request, 'management/doc_templates/supportcontract_form.html',{'job_support_data': client_data,'contract_date':contract_date,'default_fee':default_fee})
	if client_data.category == 3 and client_data.sub_category == 2:
		return render(request, 'management/doc_templates/trainingcontract_form.html',{'student_data': client_data,'contract_date':contract_date,'default_fee':default_fee})
	else:
		# return render(request, 'templates\errors\403.html')
		raise Http404("Login/Wrong Page: Are You a Client?")

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
			return render(request,"management/doc_templates/supportcontract_form.html")

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

class PaymentListView(ListView):
	model = Payment_History
	template_name = "finance/payments/payments.html"
	context_object_name = "payments"

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
			return render(request,"management/doc_templates/supportcontract_form.html")

	def test_func(self):
		task = self.get_object()
		if self.request.user.is_superuser:
			return True
		# elif self.request.user == task.employee:
		#     return True
		return False


# ----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------
@login_required
def transact(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            # try:
            #     points,mxpoint = Task.objects.values_list(
			# 		"point","mxpoint"
			# 		).filter(
			# 			Q(activity_name__contains="Cashflow") | Q(activity_name__contains="cashflow"),
			# 			employee__username=form.instance.sender
			# 		)[
			# 			0
			# 		]
            #     points = points+1
            #     if points >= mxpoint:
            #         mxpoint += 5
            #     Task.objects.filter(
			# 			Q(activity_name__contains="Cashflow") | Q(activity_name__contains="cashflow"),
			# 			employee__username=form.instance.sender
			# 		).update(point=points, mxpoint=mxpoint)
            # except:
            form.save()
                # instance=form.save(commit=False)
                # instance.sender=request.user
                # instance.save()
            return redirect("/finance/transaction/")
    else:
        form = TransactionForm()
    return render(request, "finance/payments/transact.html", {"form": form})


class TransactionListView(ListView):
	model = Transaction
	template_name = "finance/payments/transaction.html"
	context_object_name = "transactions"
	# ordering=['-transaction_date']


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
	# total_duration=Tracker.objects.all().aggregate(Sum('duration'))
	# total_communication=Rated.objects.all().aggregate(Sum('communication'))
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
# def loan(request):
# 	if request.method == "POST":
# 		form = LoanForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('finance:trainingloans')
# 	else:
# 		form=LoanForm()
# 	return render(request, "finance/payments/payment_form.html", {"form":form})
	
class LoanCreateView(LoginRequiredMixin, CreateView):
	model = PayslipConfig
	success_url = "/finance/loans"
	fields = "__all__"
	form = LoanForm()

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class LoanUpdateView(UpdateView):
	model = TrainingLoan
	success_url = "/finance/loans"
	fields="__all__"

	def form_valid(self, form):
		# form.instance.user=self.request.user
		if self.request.user.is_superuser:
			user_data = TrainingLoan.objects.filter(id=self.kwargs['pk'], is_active=True)
			username=user_data.order_by('-id')[0].user.username
			pay(self.request, **{"username":username})
			# # user_data = TrainingLoan.objects.filter(user=employee, is_active=True)
			# loantable = TrainingLoan
			# print(employee, "EEEEEE")
			# payslip_config = paymentconfigurations(PayslipConfig, employee)
			# print("AAAAAAAAAA", payslip_config)
			# total_pay = form.cleaned_data['total_earnings_amount']
			# a=loan_update_save(loantable, user_data, employee, total_pay, payslip_config)
			# print(7777777, a)
			return super().form_valid(form)
		else:
			return redirect("finance:trainingloans")
			# return render(request,"management/doc_templates/supportcontract_form.html")

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

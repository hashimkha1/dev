from unicodedata import category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum
from django.http import QueryDict, Http404,JsonResponse
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
		Inflow,Transaction,PayslipConfig,Supplier,Food,
		DC48_Inflow
	)
from .forms import LoanForm,TransactionForm,InflowForm
# User=settings.AUTH_USER_MODEL
from management.utils import paymentconfigurations
from management.views import loan_update_save
from management.utils import loan_computation
from main.filters import FoodFilter
from .utils import check_default_fee

from management.views import pay

User = get_user_model()

# Create your views here.


def finance_report(request):
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
				payment = Payment_Information.objects.filter(
            			customer_id=request.user.id
        			).first()
				# payment = Payment_Information.objects.get(customer_id_id=customer.id)
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
		message=f'Hi,{request.user}, there is an issue on our end kindly contact us directly at info@codanalytics.net'
		context={
                  "title": "CONTRACT", 
                  "message": message,
                }
		return render(request, "main/errors/generalerrors.html", context)

def mycontract(request, *args, **kwargs):
	username = kwargs.get('username')
	client_data=CustomerUser.objects.get(username=username)
	check_default_fee = Default_Payment_Fees.objects.all()
	if check_default_fee:
		# default_fee = Default_Payment_Fees.objects.get(id=1)
		default_fee = Default_Payment_Fees.objects.filter(id=1).first()
		print(default_fee)
		# default_fee = Default_Payment_Fees.objects.filter().first()
	else:
		default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
				job_plan_hours_per_month=40,
				student_down_payment_per_month=500,
				student_bonus_payment_per_month=100)
		default_payment_fees.save()
		default_fee = Default_Payment_Fees.objects.all().first()
		print(default_fee)
		
	if Payment_Information.objects.filter(customer_id_id=client_data.id).exists():
		payemnt_details = Payment_Information.objects.get(customer_id_id=client_data.id).first()
		contract_date = payemnt_details.contract_submitted_date.strftime("%d %B, %Y")
		if client_data.category == 3 and client_data.sub_category == 1:
			plan_dict = {"1":40,"2":80,"3":120}
			selected_plan = plan_dict[str(payemnt_details.plan)]
			job_support_hours = selected_plan - 30
			context={
					'job_support_data': client_data,
					'contract_date':contract_date,
					'payment_data':payemnt_details,
					"selected_plan":selected_plan,
					"job_support_hours":job_support_hours
				}
			return render(request, 'management/contracts/my_supportcontract_form.html',context)
		if client_data.category == 3 and client_data.sub_category == 2:
			context={
				'student_data': client_data,
				'contract_date':contract_date,
				'payment_data':payemnt_details
			}
			return render(request, 'management/contracts/my_trainingcontract_form.html',context)
		else:
			raise Http404("Login/Wrong Page: Are You a Client?")
	else:
		context={"title": "CONTRACT", 
				'username':username}
		return render(request, 'management/contracts/contract_error.html',context)
		
@login_required
def newcontract(request, *args, **kwargs):
	username = kwargs.get('username')
	#Gets client/user information from the custom user table
	client_data=CustomerUser.objects.get(username=username)
	print('CLIENTS DATA',client_data)
	# check_default_fee = Default_Payment_Fees.objects.all().first()
	# if check_default_fee:
	# 	default_fee = Default_Payment_Fees.objects.get(id=1)
	# else:
	# 	default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
	# 			job_plan_hours_per_month=40,
	# 			student_down_payment_per_month=500,
	# 			student_bonus_payment_per_month=100)
	# 	default_payment_fees.save()
	# 	default_fee = Default_Payment_Fees.objects.get(id=1)

	#Gets any payment default values from the Default table
	check_default_fee = Default_Payment_Fees.objects.all()
	print(check_default_fee)
	if check_default_fee:
		default_fee = Default_Payment_Fees.objects.filter().first()
		print(default_fee)
	else:
		default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
				job_plan_hours_per_month=40,
				student_down_payment_per_month=500,
				student_bonus_payment_per_month=100)
		default_payment_fees.save()
		default_fee = Default_Payment_Fees.objects.get(id=default_payment_fees.id)
		print('new default:',default_fee)
	# 	default_fee=check_default_fee(Default_Payment_Fees,username)
	today = date.today()
	contract_date = today.strftime("%d %B, %Y")
	context={
			'job_support_data': client_data,
			'student_data': client_data,
			'contract_date':contract_date,
			'default_fee':default_fee
			}
	if client_data.category == 3 and client_data.sub_category == 1 or request.user.is_superuser:
		return render(request, 'management/contracts/supportcontract_form.html',context)
	if client_data.category == 3 and client_data.sub_category == 2 or request.user.is_superuser:
		return render(request, 'management/contracts/trainingcontract_form.html',context)
	else:
		message=f'Hi {request.user},this page is only available for clients,kindly contact adminstrator'
		context={"title": "CONTRACT", 
				"message": message}
		return render(request, "management/contracts/contract_error.html", context)

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
	context={
		"title":"Payments",
		"payment_history":payment_history,
		"Payment_Info":Payment_Info
	}
	return render(request,"finance/payments/payments.html",context)

# class PaymentListView(ListView):
# 	model = Payment_History
# 	template_name = "finance/payments/payments.html"
# 	context_object_name = "payments"


# class PaymentInformationListView(UpdateView):
# 	model = Payment_Information
# 	success_url = "/pay/"
# 	template_name="main/snippets_templates/generalform.html"

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
class PaymentInformationUpdateView(UpdateView):
	model = Payment_Information
	success_url = "/pay/"
	template_name="main/snippets_templates/generalform.html"
	
	# fields ="__all__"
	fields=['customer_id','down_payment']
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
    

# class FoodListView(ListView):
#     model = Food
#     foodfilter=FoodFilter
#     template_name = "finance/payments/food.html"
#     context_object_name = "supplies,foodfilter"
#     ordering = ["-created_at"]

    # def get_context_data(self,*args, **kwargs):
    #     context = super(FoodListView, self).get_context_data(*args,**kwargs)
    #     context['foodfilter'] = Food.objects.all()
    #     return context


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

# =========================DC 48 KENYA===================================



@method_decorator(login_required, name="dispatch")
class DC48InflowCreateView(LoginRequiredMixin, CreateView):
    model = DC48_Inflow
    success_url = "/finance/listinflow"
    template_name="finance/payments/inflow_form.html"
    fields ="__all__"
    exclude='transaction_date'
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DC48InflowListview(LoginRequiredMixin,ListView):
    queryset = DC48_Inflow.objects.all()
    print(queryset)
    transactions=queryset
    template_name="finance/payments/dcinflows.html"
    context_object_name = "transactions"
    # fields ="__all__"
    fields=['category','method','period','sender','receiver'
			'description','phone','qty','amount']

@method_decorator(login_required, name="dispatch")
class DC48InflowUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DC48_Inflow
    template_name="finance/payments/inflow_form.html"
    success_url = "/finance/listinflow"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
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
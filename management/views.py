import calendar
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import (TransactionForm,OutflowForm,InflowForm,PolicyForm,ManagementForm)
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from .models import Transaction,Inflow,Outflow,Policy,Task,Tag#,TaskInfos
from data.models import DSU

from django.conf import settings
from django.contrib.auth import get_user_model

#User=settings.AUTH_USER_MODEL
User = get_user_model()

def home(request):
    return render(request, 'main/home_templates/management_home.html',{'title': 'home'})

def thank(request):
    return render(request, 'management/daf/thank.html')

#==============================PLACE HOLDER MODELS=======================================

#Summary information for tasks


tasksummary=[
{
   
	'Target':'1',
	'Description':'Total Amount Assigned',
},
{
	'Target':'2',
	'Description':' progress	',
},
{
	'Target':'3',
	'Description':'Keep making progress	',
},
]

#----------------------REPORTS--------------------------------

def finance(request):
    return render(request, 'management/company_finances/finance.html',{'title': 'finance'})

def hr(request):
    return render(request, 'management/company_finances/hr.html',{'title': 'hr'})

#----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------

def transact(request):
    if request.method== "POST":
        form=TransactionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/management/transaction/')
    else:
        form=TransactionForm()
    return render(request, 'management/company_finances/transact.html',{'form':form})

'''
def transaction(request):
    transactions=Transaction.objects.all().order_by('-transaction_date')
    return render(request, 'management/company_finances/transaction.html', {'transactions': transactions})
'''

class TransactionListView(ListView):
    model=Transaction
    template_name='management/company_finances/transaction.html'
    context_object_name='transactions'
    #ordering=['-transaction_date']

@method_decorator(login_required, name='dispatch')
class OutflowDetailView(DetailView):
    template_name='management/outflow_detail.html'
    model=Transaction
    ordering=['-transaction_date']

class TransactionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Transaction
    #success_url="/management/transaction"
    fields = ['sender','receiver','phone','department', 'category','type','payment_method','qty','amount','transaction_cost','description','receipt_link']
    form=TransactionForm()

    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('management:transaction-list') 
''' 

    def test_func(self):
        expense = self.get_object()
        if self.request.user == expense.author:
            return True
        return False
'''
#----------------------CASH OUTFLOW CLASS-BASED VIEWS--------------------------------

def outflow_entry(request):
    if request.method== "POST":
        form=OutflowForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.employee=request.user
            form.save()
            return redirect('/management/outflows/')
    else:
        form=OutflowForm()
    return render(request, 'management/company_finances/outflow_entry.html',{'form':form})
'''
@method_decorator(login_required, name='dispatch')
class OutflowCreateView(LoginRequiredMixin, CreateView):
    model=Outflow
    success_url="/management/outflows"
    fields = ['sender','receiver','phone','department', 'category','type','payment_method','qty','amount','transaction_cost','description']
    def form_valid(self,form):
        form.instance.employee=self.request.user
        return super().form_valid(form) 

@method_decorator(login_required, name='dispatch')
class OutflowListView(ListView):
    model=Outflow
    template_name='management/cash_outflow/outflows.html'
    context_object_name='outflows'
    ordering=['-activity_date']
''' 
def outflowlist(request):
    outflows=Outflow.objects.all().order_by('-activity_date')
    #total_duration=Tracker.objects.all().aggregate(Sum('duration'))
    #total_communication=Rated.objects.all().aggregate(Sum('communication'))
    total=Outflow.objects.all().aggregate(Total_Cashoutflows=Sum('amount'))
    expenses=total.get('Total_Cashoutflows')
    context = {
                'outflows': outflows,
                'expenses':expenses
              }
    return render(request, 'management/cash_outflow/outflows.html', context)
                                                                                                                                        
@method_decorator(login_required, name='dispatch')
class OutflowDetailView(DetailView):
    template_name='management/cash_outflow/outflow_detail.html'
    model=Outflow
    ordering=['-activity_date']

@method_decorator(login_required, name='dispatch')
class OutflowUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Outflow
    success_url='/management/outflows'
    fields =['sender','receiver','phone','department', 'category','type','payment_method','qty','amount','transaction_cost','description']
    def form_valid(self,form):
        form.instance.employee=self.request.user
        return super().form_valid(form)

    def test_func(self):
        outflow = self.get_object()
        if self.request.user == outflow.employee:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class OutflowDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Outflow
    success_url='/management/outflows'

    def test_func(self):
        outflow = self.get_object()
        if self.request.user == outflow.employee:
            return True
        return False
#----------------------CASH INFLOW CLASS-BASED VIEWS--------------------------------
'''
@method_decorator(login_required, name='dispatch')
class InflowCreateView(LoginRequiredMixin, CreateView):
    model=Inflow
    success_url="/management/user_inflow"
    fields = ['receiver','phone','department', 'category','task','method','period','qty','amount','transaction_cost','description','receipt_link']
    
    def form_valid(self,form):
        form.instance.sender=self.request.user
        return super().form_valid(form) 
'''

def inflow(request):
    if request.method== "POST":
        form=InflowForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.sender=request.user
            form.save()
            return redirect('/management/inflows/')
    else:
        form=InflowForm()
    return render(request, 'management/company_finances/inflow_entry.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class InflowDetailView(DetailView):
    template_name='management/cash_inflow/inflow_detail.html'
    model=Inflow
    ordering=['-transaction_date']

'''
@method_decorator(login_required, name='dispatch')
class InflowListView(ListView):
    model=Inflow
    template_name='management/cash_inflow/inflow.html'
    context_object_name='inflows'
    ordering=['-transaction_date']
    

'''
def inflows(request):
    inflows=Inflow.objects.all().order_by('-transaction_date')
    #total_duration=Tracker.objects.all().aggregate(Sum('duration'))
    #total_communication=Rated.objects.all().aggregate(Sum('communication'))
    total=Inflow.objects.all().aggregate(Total_Cashinflows=Sum('amount'))
    revenue=total.get('Total_Cashinflows')
    context = {
                'inflows': inflows,
                'revenue':revenue
              }
    return render(request, 'management/cash_inflow/inflows.html', context)

@method_decorator(login_required, name='dispatch')
class UserInflowListView(ListView):
    model=Inflow
    template_name='management/cash_inflow/user_inflow.html'
    context_object_name='inflows'
    ordering=['-transaction_date']
''' 
    def get_queryset(self):
        user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
        return Inflow.objects.filter(author=user).order_by('-transaction_date')
'''

@method_decorator(login_required, name='dispatch')
class InflowUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Inflow
    success_url='/management/inflow'
    fields=['sender','receiver','phone', 'category','task','method','period','qty','amount','transaction_cost','description']

    def form_valid(self,form):
        form.instance.sender=self.request.user
        return super().form_valid(form)

    def test_func(self):
        inflow = self.get_object()
        if self.request.user == inflow.sender:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class InflowDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Inflow
    success_url='/management/inflow'

    def test_func(self):
        inflow = self.get_object()
        #if self.request.user == inflow.sender:
        if self.request.user.is_superuser:
            return True
        return False

#----------------------MANAGEMENT POLICIES& OTHER VIEWS--------------------------------
def policy(request):
    if request.method== "POST":
        form=PolicyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:policies')
    else:
        form=PolicyForm()
    return render(request, 'management/hr/policy.html',{'form':form})


def policies(request):
    reporting_date = date.today()
    day_name=date.today().strftime("%A")
    uploads=Policy.objects.all().order_by('upload_date')
    context = {
        'uploads': uploads,
        'reporting_date': reporting_date,
        'day_name':day_name
    }
    return render(request, 'management/hr/policies.html',context)

def benefits(request):
    reporting_date = date.today()
    day_name=date.today().strftime("%A")
    uploads=Policy.objects.all().order_by('upload_date')
    context = {
        'uploads': uploads,
        'reporting_date': reporting_date,
        'day_name':day_name
    }
    return render(request, 'management/hr/benefits.html',context)

#===================================ACTIVITY CLASS-BASED VIEWS=========================================

#======================TAG=======================
class TagCreateView(LoginRequiredMixin, CreateView):
    model=Tag
    success_url="/management/newcategory"
    fields=['title','description']

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)  

#======================TASKS=======================
def task(request, slug=None, *args, **kwargs):
    # qs=Info.objects.filter(id=pk)
    # if qs.exists and qs.count()==1:
    #     instance=qs.first()
    # else:
    #     raise Http404("User does not exist")
    instance=Task.objects.get_by_slug(slug)
    if instance is None:
        raise Http404("Task does not exist")

    context = {
                'object':instance
              }
    return render(request, 'management/daf/task.html', context)
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model=Task
    success_url="/management/newtask"
    fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)  

class TaskListView(ListView):
  queryset=Task.objects.all()
  template_name='management/daf/tasklist.html'


''' 


  def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['tasksummary'] = tasksummary
        return context

  def interview(self):
    context = {
        'tasksummary': tasksummary
    }
    return context

class UserListView(ListView):
  queryset=Task.objects.all()
  template_name='management/daf/usertasks.html'

  def get_total(self):
      Amount=Task.objects.aggregate(Your_Total_Amount=Sum('pay'))  
      Total=Amount.get('Your_Total_Amount')
      return Total """
'''
def usertask(request, user=None, *args, **kwargs):
    #tasks=Task.objects.all().order_by('-submission')
    #user= get_object_or_404(CustomerUser, username=self.kwargs.get('username'))
    #Amount=Task.objects.all().aggregate(Your_Total_GoalAmount=Sum('mxearning'))
    #total_duration=Task.objects.all().aggregate(Sum('duration'))
    #mxearning=Task.objects.filter().aggregate(Your_Total_AssignedAmt=Sum('mxearning'))  
    #paybalance=round(bal,2)
    #balance=paybalance.quantize(Decimal('0.01'))
    #salary = [task.pay for pay in Task.objects.all().values()]
    computer_maintenance=500
    food_accomodation=1000
    deadline_date=date(date.today().year, date.today().month, calendar.monthrange(date.today().year, date.today().month)[-1])
    delta=deadline_date-date.today()
    time_remaining=delta.days
    current_user = request.user
    employee = get_object_or_404(User, username=kwargs.get('username'))
    tasks=Task.objects.all().filter(employee=employee)
    #tasks = Task.objects.filter(user__username=request.user)
    num_tasks = tasks.count()
    points=tasks.aggregate(Your_Total_Points=Sum('point')) 
    mxpoints=tasks.aggregate(Your_Total_MaxPoints=Sum('mxpoint')) 
    earning=tasks.aggregate(Your_Total_Pay=Sum('mxearning'))
    mxearning=tasks.aggregate(Your_Total_AssignedAmt=Sum('mxearning'))
    Points=points.get('Your_Total_Points')
    MaxPoints=mxpoints.get('Your_Total_MaxPoints')
    pay=earning.get('Your_Total_Pay')
    GoalAmount=mxearning.get('Your_Total_AssignedAmt')
    pay=earning.get('Your_Total_Pay')
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay
    try:
        paybalance=Decimal(GoalAmount)-Decimal(total_pay)
    except (TypeError, AttributeError):
        paybalance=0
    
    loan=Decimal(total_pay)*Decimal('0.2')

    try:
        net=total_pay-computer_maintenance-food_accomodation-loan
    except (TypeError, AttributeError):
        net=total_pay-computer_maintenance-food_accomodation
    try:
        pointsbalance=Decimal(MaxPoints)-Decimal(Points)
    except (TypeError, AttributeError):
        pointsbalance=0

    context= {
                'tasksummary':tasksummary,
                'num_tasks':num_tasks,
                'tasks': tasks,
                'Points':Points,
                'MaxPoints':MaxPoints,
                'pay':pay,
                'GoalAmount':GoalAmount,
                'paybalance':paybalance,
                'pointsbalance':pointsbalance,
                'time_remaining':time_remaining,
                'total_pay':total_pay,
                'loan':loan,
                'net':net
              }

    if request.user == employee:
        return render(request, 'management/daf/usertasks.html', context)
    elif request.user.is_superuser:
        return render(request, 'management/daf/usertasks.html', context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")

def payslip(request, user=None, *args, **kwargs):
    deadline_date=date(date.today().year, date.today().month, calendar.monthrange(date.today().year, date.today().month)[-1])
    today=date(date.today().year, date.today().month , date.today().day)
    year=date.today().year
    month=date.today().month
    day=date.today().day

    employee = get_object_or_404(User, username=kwargs.get('username'))
    tasks=Task.objects.all().filter(employee=employee)
    mxearning=tasks.aggregate(Your_Total_AssignedAmt=Sum('mxearning'))
    GoalAmount=mxearning.get('Your_Total_AssignedAmt')
    points=tasks.aggregate(Your_Total_Points=Sum('point'))
    total_pay = 0
    for task in tasks:
        total_pay = total_pay + task.get_pay

    # Deductions
    loan=Decimal(total_pay)*Decimal('0.2')
    computer_maintenance=500
    food_accomodation=1000
    health=500
    laptop_saving=1000
    total_deduction=Decimal(loan)+Decimal(computer_maintenance)+Decimal(food_accomodation)+Decimal(health)+Decimal(laptop_saving)

    # Bonus
    Lap_Bonus=500
    if points.get('Your_Total_Points')==None:
        pointsearning=0
    else:
        pointsearning=points.get('Your_Total_Points')
    
    Night_Bonus=Decimal(total_pay)*Decimal('0.02')
    if month in (12,1) and day in (24,25,26,31,1,2):
        holidaypay=3000.00
    else:
        holidaypay=0.00
    EOM=0
    EOQ=0
    EOY=0
    yearly=12000
    total_bonus=Decimal(pointsearning)+Decimal(holidaypay)+Decimal(EOM)+Decimal(EOQ)+Decimal(EOY)+Night_Bonus
    # Net Pay
    try:
        net=total_pay-total_bonus-total_deduction
    except (TypeError, AttributeError):
        net=total_pay
        
    context= {
                #deductions
                'laptop_saving':laptop_saving,
                'computer_maintenance':computer_maintenance,
                'food_accomodation':food_accomodation,
                'health':health,
                'loan':loan,
                'total_deduction':total_deduction,
                #bonus
                'Night_Bonus':Night_Bonus,
                'pointsearning':pointsearning,
                'holidaypay':holidaypay,
                'yearly':yearly,
                #General
                'tasks':tasks,
                'deadline_date':deadline_date,
                'today':today,
                'total_pay':total_pay,
                'net':net
              }

    if request.user == employee:
        #return render(request, 'management/daf/paystub.html', context)
        return render(request, 'management/daf/payslip.html', context)
    elif request.user.is_superuser:
        #return render(request, 'management/daf/paystub.html', context)
        return render(request, 'management/daf/payslip.html', context)
    else:
        raise Http404("Login/Wrong Page: Contact Admin Please!")
    
class TaskDetailView(DetailView):
    queryset=Task.objects.all()
    template_name='management/daf/task_detail.html'
    #ordering = ['-datePosted']

    def get_context_data(self, *args,**kwargs):
        context=super(TaskDetailView,self).get_context_data(*args,**kwargs)
        # print(context)
        return context
    
    def get_queryset(self, *args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')
        return Task.objects.filter(pk=pk)


class UserTaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'management/daf/employee_tasks.html'

    #paginate_by = 5
    def get_queryset(self):
        #request=self.request
        #user=self.kwargs.get('user')
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        #tasks=Task.objects.all().filter(employee=user)
        
        return Task.objects.all().filter(employee=user)


"""     def get_queryset(self):
        request=self.request
        user=self.kwargs.get('user')
        #user = get_object_or_404(User, username=self.kwargs.get('user'))
        #tasks=Task.objects.all().filter(user= user).order_by('-submission')
        tasks = Task.objects.filter(user__username=request.user)
        return tasks """


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Task
    success_url="/management/tasks"
    fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    #fields=['user','activity_name','description','point']
    def form_valid(self,form):
        #form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return redirect('management:tasks')

    def test_func(self):
        task = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==task.employee:
            return True
        return False

@method_decorator(login_required, name='dispatch')
      
class UsertaskUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Task
    success_url="/management/thank"
    #fields=['group','category','user','activity_name','description','slug','point','mxpoint','mxearning']
    fields=['employee','activity_name','description','point']
    def form_valid(self,form):
        #form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==task.employee:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Task
    success_url="/accounts/tasklist"

    def test_func(self):
        #timer = self.get_object()
        #if self.request.user == timer.author:
        #if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False

#=============================EMPLOYEE ASSESSMENTS========================================
@login_required
def assess(request):
    if request.method== "POST":
        form=ManagementForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:assessment')
    else:
        form=ManagementForm()
    return render(request, 'management/hr/assess_form.html',{'form':form})

class AssessListView(ListView):
  queryset=DSU.objects.filter(type='Staff').order_by('-created_at')
  #queryset=DSU.objects.all()
  template_name='management/hr/assessment.html'
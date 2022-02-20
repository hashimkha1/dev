import calendar
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import (TransactionForm,OutflowForm,InflowForm,PolicyForm)
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from .models import Transaction,Inflow,Outflow,Policy


def home(request):
    return render(request, 'main/home_templates/management_home.html',{'title': 'home'})

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
    #reporting_date = date.today() + timedelta(days=7)
    uploads=Policy.objects.all().order_by('upload_date')
    context = {
        'uploads': uploads,
       # 'reporting_date': reporting_date
    }
    return render(request, 'management/hr/policies.html',context)
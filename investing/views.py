from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from .utils import compute_pay
from .models import Investments
from .forms import InvestmentForm
from django.contrib.auth import get_user_model
from accounts.models import CustomerUser

User=get_user_model
# Create your views here.
def home(request):
    return render(request, 'main/home_templates/investing_home.html', {'title': 'home'})

def coveredcalls(request):
    return render(request, 'investing/covered_call.html', {'title': 'covered Calls'})

def training(request):
    return render(request, 'investing/training.html', {'title': 'training'})

@login_required
def newinvestment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # config.user = request.user
            instance.save()
            return redirect('investing:investments') 
    else:
        form = InvestmentForm()
    return render(request, 'main/snippets_templates/generalform.html', {'form': form})


def investments(request):
    investments=Investments.objects.all()
    latest_investment = Investments.objects.latest('investment_date')
    total_amt=0
    for amt  in investments:
        total_amt=total_amt+amt.amount
        print(total_amt)
    amount_invested=float(total_amt)*float(0.33)
    amount = float(total_amt)
    returns=compute_pay(amount)
    print(amount,amount_invested,returns)
    context={
        "investments":investments,
        "latest_investment":latest_investment,
        "amount":amount,
        "amount_invested":amount_invested,
         'title': 'training',
         'returns': returns
    }
    return render(request, 'investing/clients_investments.html',context)

def user_investments(request, username=None, *args, **kwargs):
    user = get_object_or_404(CustomerUser, username=username)
    print("username=====>", user)
    investments = Investments.objects.filter(client=user)
    latest_investment = investments.latest('investment_date')
    amount = float(latest_investment.amount)
    returns = compute_pay(amount)
    print(amount, returns)
    context = {
        "investments": investments,
        "latest_investment": latest_investment,
        "title": "training",
        "returns": returns
    }
    return render(request, 'investing/clients_investments.html', context)


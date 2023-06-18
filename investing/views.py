from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.db.models import F
from .utils import compute_pay
from .models import Investments
from .forms import InvestmentForm

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
    amount = float(latest_investment.amount)
    returns=compute_pay(amount)
    print(amount,returns)
    return render(request, 'investing/training.html', {'title': 'training'})

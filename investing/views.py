from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, UpdateView

from .utils import compute_pay
from .forms import (
    CoveredCallsForm,
    ShortPutForm,
    CreadSpreadForm,
    InvestmentForm
)
from .models import (
    stockmarket,
    ShortPut,
    covered_calls,
    cread_spread,
    cryptomarket,
    Investments
)
from accounts.models import CustomerUser
from getdata.utils import (
    main_covered_calls,
    main_cread_spread,
    main_shortput,
    compute_stock_values
)
from main.utils import path_values





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


def options_play_shortput(request):
    # Call the main_shortput function to retrieve the data
    message = 'we are done processing your request'
    data = main_shortput(request)
    # Loop through the data and insert it into the database
    created_count = 0
    for row in data:
        symbol = row[0]
        action = row[1]
        expiry = row[2]
        days_to_expiry = row[3]
        strike_price = row[4]
        mid_price = row[5]
        bid_price = row[6]
        ask_price = row[7]
        implied_volatility_rank = row[8]
        earnings_date = row[9]
        stock_price = row[11]
        raw_return = row[12]
        annualized_return = row[13]
        distance_to_strike = row[14]

        obj, created = ShortPut.objects.get_or_create(
            Symbol=symbol,
            Action=action,
            Expiry=expiry,
            Days_To_Expiry=days_to_expiry,
            Strike_Price=strike_price,
            defaults={
                'Mid_Price': mid_price,
                'Bid_Price': bid_price,
                'Ask_Price': ask_price,
                'Implied_Volatility_Rank': implied_volatility_rank,
                'Earnings_Date': earnings_date,
                'Stock_Price': stock_price,
                'Raw_Return': raw_return,
                'Annualized_Return': annualized_return,
                'Distance_To_Strike': distance_to_strike
            }
        )
        if created:
            created_count += 1
    # return render (request, "main/snippets_templates/output_snippets/option_data.html", context)
    return redirect ('getdata:shortputdata')


def optiondata(request):
    path_value, sub_title = path_values(request)
    if sub_title == 'covered_calls':
        title = 'COVERED CALLS'
        stockdata = covered_calls.objects.all().filter(is_featured=True)
    elif sub_title == 'shortputdata':
        title = 'SHORT PUT'
        stockdata = ShortPut.objects.all().filter(is_featured=True)
    else:
        title = 'CREDIT SPREAD'
        stockdata = cread_spread.objects.all().filter(is_featured=True)
    context = { 
        "data": stockdata,
        "subtitle": sub_title,
        'title': title,
    }
    return render(request, "main/snippets_templates/output_snippets/option_data.html", context)


class OptionList(ListView):
    model=stockmarket
    template_name="getdata/options.html"
    context_object_name = "stocks"

# class OptionUpdateView(UpdateView):
#     success_url = "/getdata/shortputdata"
#     fields = "__all__"
#     template_name="main/snippets_templates/generalform.html"
#     def dispatch(self, request, *args, **kwargs):
#         self.path_value, self.sub_title = path_values(request)
#         return super().dispatch(request, *args, **kwargs)

#     def test_func(self):
#         return self.request.user.is_superuser

#     def get_form_class(self):
#         if self.sub_title == 'covered_calls':
#             return CoveredCallsForm
#         elif self.sub_title == 'shortputdata':
#             return ShortPutForm
#         else:
#             return CreadSpreadForm

#     def get_object(self, queryset=None):
#         if self.sub_title == 'covered_calls':
#             return covered_calls.objects.filter().first()
#         elif self.sub_title == 'shortputdata':
#             return ShortPut.objects.filter().first()
#         else:
#             return cread_spread.objects.filter().first()

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         return response


# class shortputupdate(UpdateView):
#     model = ShortPut
#     success_url = "/investing/shortputdata"
#     # fields = "__all__"
#     fields = ['comment']

#     template_name="main/snippets_templates/generalform.html"
#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         return super().form_valid(form)
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         return False


@login_required
@user_passes_test(lambda u: u.is_superuser)
def shortput_update(request, pk):
    *_,subtitle=path_values(request)
    shortput = get_object_or_404(ShortPut, pk=pk)
    success_url = reverse('investing:shortput')

    if request.method == 'POST':
        form = ShortPutForm(request.POST, instance=shortput)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = ShortPutForm(instance=shortput)

    context = {
        'form': form,
        'title': 'Update Short Put',
    }
    return render(request, 'main/snippets_templates/generalform.html', context)


    
class covered_calls_update(UpdateView):
    model = covered_calls
    success_url = "/investing/covered_calls"
    # fields = "__all__"
    fields = ['Symbol','comment','is_featured']
    template_name="main/snippets_templates/generalform.html"
    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    
class cread_spread_update(UpdateView):
    model = cread_spread
    success_url = "/investing/credit_spread"
    # fields = "__all__"
    fields = ['Symbol','comment','is_featured']
    template_name="main/snippets_templates/generalform.html"
    def form_valid(self, form):
        return super().form_valid(form)
    def test_func(self):
        # interview = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False

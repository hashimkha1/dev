from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.urls import reverse
import math
from django.db.models import Q,Max,F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, UpdateView
from datetime import date,datetime,time,timezone
from .utils import (compute_pay,get_over_postions,investment_test,
                    computes_days_expiration,get_user_investment)

from main.filters import ReturnsFilter
from main.utils import path_values,dates_functionality

from .forms import (
    OptionsForm,
    InvestmentForm,
    InvestmentRateForm
)
from .models import (
    stockmarket,
    ShortPut,
    covered_calls,
    credit_spread,
    Investments,
    Investment_rates,
    Oversold,
    Options_Returns,
    Cost_Basis
)
from django.db.models import Q
from accounts.models import CustomerUser
from getdata.utils import (
    main_shortput,
)



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
            instance.client=request.user
            instance.save()
            # return redirect('investing:user_investments', request.user) 
            return redirect('finance:newoptioncontract', request.user) 
    else:
        form = InvestmentForm()
    return render(request, 'investing/investment_form.html', {'form': form})

@login_required
def newinvestmentrate(request):
    if request.method == 'POST':
        form = InvestmentRateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('investing:investments') 
    else:
        form = InvestmentRateForm()
    return render(request, 'main/snippets_templates/generalform.html', {'form': form})

@login_required
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

@login_required
def user_investments(request, username=None, *args, **kwargs):
    user = get_object_or_404(CustomerUser, username=username)
    investments = Investments.objects.filter(client=user)
    latest_investment_rates = Investment_rates.objects.order_by('-created_date').first()
    # latest_investment_rates if Investment_rates.exists() else None
    (total_amount,protected_capital,amount_invested,
     bi_weekly_returns,number_positions,minimum_duration
     )=get_user_investment(investments,latest_investment_rates)
    
    context = {
        "investments": investments,
        # "latest_investment": latest_investment if investments.exists() else None,
        "title": "training",
        "amount": total_amount,
        "protected_capital": protected_capital,
        "number_positions": number_positions,
        "amount_invested": amount_invested,
        "minimum_duration": minimum_duration,
        "returns": bi_weekly_returns
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


# def optiondata(request):

#     path_list,sub_title,pre_sub_title = path_values(request)
#     all_returns = Options_Returns.objects.all()
#     all_return_symbols = set(Options_Returns.objects.values_list('symbol', flat=True))

#     symbols = []
#     for obj in all_returns:
#         if obj.wash_days >= 40:
#             symbols.append(obj.symbol)
#     distinct_returns_symbols = list(set(symbols))

#     date_today = datetime.now(timezone.utc)
#     if sub_title == 'covered_calls':
#         title = 'COVERED CALLS'
#         stockdata = covered_calls.objects.all().filter(is_featured=True)
#     elif sub_title == 'shortputdata':
#         title = 'SHORT PUT'
#         stockdata = ShortPut.objects.all().filter(is_featured=True)
#     else:
#         title = 'CREDIT SPREAD'
#         stockdata = credit_spread.objects.all().filter(is_featured=True)

#     url_mapping = {
#     'shortputdata': 'investing:shortputupdate',
#     'credit_spread': 'investing:creditspreadupdate',
#     'covered_calls': 'investing:coveredupdate',
#     }
#     url_name = url_mapping[sub_title]

#     def get_edit_url(row_id):
#         return reverse(url_name, args=[row_id])
    
#     expiry_date,days_to_expiration=computes_days_expiration(stockdata)

#     filtered_stockdata = []

#     for x in stockdata:
#         if x.symbol not in all_return_symbols or x.symbol in distinct_returns_symbols:
#             if days_to_expiration >= 21:
#                 url = reverse(url_name, args=[x.id])  
#                 filtered_stockdata.append(x)
    
#     context = { 
#         "data": filtered_stockdata,
#         "days_to_expiration": days_to_expiration,
#         "subtitle": sub_title,
#         "pre_sub_title": pre_sub_title,
#         'title': title,
#         "get_edit_url": get_edit_url,
#         "url_name": url_name,
#     }
#     return render(request, "main/snippets_templates/output_snippets/option_data.html", context)

def optionlist(request):
    title="creditspread"
    return render(request, "main/snippets_templates/output_snippets/option_data.html")


# def optiondata(request,title=None,*arg,**kwargs):
#     print("title=======>",title)
#     path_list,sub_title,pre_sub_title = path_values(request)
#     all_returns = Options_Returns.objects.all()
#     all_return_symbols = set(Options_Returns.objects.values_list('symbol', flat=True))

#     symbols = []
#     for obj in all_returns:
#         if obj.wash_days >= 40:
#             symbols.append(obj.symbol)
#     distinct_returns_symbols = list(set(symbols))

#     date_today = datetime.now(timezone.utc)
#     if sub_title == 'covered_calls':
#         title = 'COVERED CALLS'
#         stockdata = covered_calls.objects.all().filter(is_featured=True)
#     elif sub_title == 'shortputdata':
#         title = 'SHORT PUT'
#         stockdata = ShortPut.objects.all().filter(is_featured=True)
#     else:
#         title = 'CREDIT SPREAD'
#         stockdata = credit_spread.objects.all().filter(is_featured=True)

#     url_mapping = {
#     'shortputdata': 'investing:shortputupdate',
#     'credit_spread': 'investing:creditspreadupdate',
#     'covered_calls': 'investing:coveredupdate',
#     }
#     url_name = url_mapping[sub_title]

#     def get_edit_url(row_id):
#         return reverse(url_name, args=[row_id])
    
#     expiry_date,days_to_expiration=computes_days_expiration(stockdata)

#     filtered_stockdata = []

#     for x in stockdata:
#         if x.symbol not in all_return_symbols or x.symbol in distinct_returns_symbols:
#             if days_to_expiration >= 21:
#                 url = reverse(url_name, args=[x.id])  
#                 filtered_stockdata.append(x)
    
#     context = { 
#         "data": filtered_stockdata,
#         "days_to_expiration": days_to_expiration,
#         "subtitle": sub_title,
#         "pre_sub_title": pre_sub_title,
#         'title': title,
#         "get_edit_url": get_edit_url,
#         "url_name": url_name,
#     }
#     return render(request, "main/snippets_templates/output_snippets/option_data.html", context)


def optiondata(request, title=None, *arg, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)

    # Get symbols with wash_days >= 40 directly using list comprehension
    distinct_returns_symbols = list(set([
        obj.symbol for obj in Options_Returns.objects.all() if obj.wash_days >= 40
    ]))

    model_mapping = {
        'covered_calls': {
            'model': covered_calls,
            'title': 'COVERED CALLS'
        },
        'shortputdata': {
            'model': ShortPut,
            'title': 'SHORT PUT'
        },
        'credit_spread': {
            'model': credit_spread,
            'title': 'CREDIT SPREAD'
        }
    }

    stock_model = model_mapping[sub_title]['model']
    title = model_mapping[sub_title]['title']

    stockdata = stock_model.objects.filter(is_featured=True)
    
    url_mapping = {
        'shortputdata': 'investing:shortputupdate',
        'credit_spread': 'investing:creditspreadupdate',
        'covered_calls': 'investing:coveredupdate',
    }
    url_name = url_mapping[sub_title]

    def get_edit_url(row_id):
        return reverse(url_name, args=[row_id])
    
    expiry_date, days_to_expiration = computes_days_expiration(stockdata)
    
    filtered_stockdata = [
        x for x in stockdata if (
            not Options_Returns.objects.filter(symbol=x.symbol).exists() or
            x.symbol in distinct_returns_symbols
        ) and days_to_expiration >= 21
    ]
    
    context = { 
        "data": filtered_stockdata,
        "days_to_expiration": days_to_expiration,
        "subtitle": sub_title,
        "pre_sub_title": pre_sub_title,
        'title': title,
        "get_edit_url": get_edit_url,
        "url_name": url_name,
    }
    return render(request, "main/snippets_templates/output_snippets/option_data.html", context)

class OptionList(ListView):
    model=stockmarket
    template_name="getdata/options.html"
    context_object_name = "stocks"


@login_required
@user_passes_test(lambda u: u.is_superuser)
def shortput_update(request, pk):
    path_list,subtitle,pre_sub_title=path_values(request)
    shortput = get_object_or_404(ShortPut, pk=pk)
    success_url = reverse('investing:option_list', kwargs={'title': 'shortputdata'})

    if request.method == 'POST':
        form = OptionsForm(request.POST, instance=shortput)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = OptionsForm(instance=shortput)

    context = {
        'form': form,
        'title': 'Update Short Put',
    }
    return render(request, 'main/snippets_templates/generalform.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def covered_update(request, pk):
    path_list,subtitle,pre_sub_title=path_values(request)
    covered = get_object_or_404(covered_calls, pk=pk)
    success_url = reverse('investing:option_list', kwargs={'title': 'covered_calls'})

    if request.method == 'POST':
        form = OptionsForm(request.POST, instance=covered)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = OptionsForm(instance=covered)

    context = {
        'form': form,
        'title': 'Update covered Calls',
    }
    return render(request, 'main/snippets_templates/generalform.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def credit_spread_update(request, pk):
    spread = get_object_or_404(credit_spread, pk=pk)
    success_url = reverse('investing:option_list', kwargs={'title': 'credit_spread'})

    if request.method == 'POST':
        form = OptionsForm(request.POST, instance=spread)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = OptionsForm(instance=spread)

    context = {
        'form': form,
        'title': 'Update Credit spread',
    }
    return render(request, 'main/snippets_templates/generalform.html', context)



# class covered_calls_update(UpdateView):
#     model = covered_calls
#     success_url = reverse('investing:option_list', kwargs={'title': 'covered_calls'})
#     # fields = "__all__"
#     fields = ['symbol','comment','is_featured']
#     template_name="main/snippets_templates/generalform.html"
#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         return super().form_valid(form)
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         return False
    
# class credit_spread_update(UpdateView):
#     model = credit_spread
#     success_url = "/investing/credit_spread"
#     # fields = "__all__"
#     fields = ['symbol','comment','is_featured']
#     template_name="main/snippets_templates/generalform.html"
#     def form_valid(self, form):
#         return super().form_valid(form)
#     def test_func(self):
#         # interview = self.get_object()
#         if self.request.user.is_superuser:
#             return True
#         return False

@login_required
def oversoldpositions(request):
    path_list,sub_title,pre_sub_title = path_values(request)
    # Get current datetime with UTC timezone
    table_name = "investing_oversold"
    get_over_postions(table_name)
    overboughtsold_records = Oversold.objects.all()
    # expiry_date,days_to_expiration=computes_days_expiration(stockdata)
    # for record in overboughtsold_records:
        # print("record========>",record)

    context = { 
        "overboughtsold": overboughtsold_records,
        "overboughtsold": overboughtsold_records,
        # "expiry_date": expiry_date,
        # "days_to_expiration": days_to_expiration,
    }
    return render(request, "investing/oversold.html", context)

class oversold_update(UpdateView):
    model = Oversold
    success_url = "/investing/overboughtsold"
    fields ="__all__"
    # fields = ['symbol','comment','is_featured']
    template_name="main/snippets_templates/generalform.html"
    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    


from django import template

register = template.Library()

@register.filter
def subtract_dates(date1, date2):
    return date1 - date2

@login_required
def options_returns(request):
    date_today = datetime.now(timezone.utc)
    ytd_duration,current_year = dates_functionality()
    
    ytd_weeks=int(ytd_duration/7)
    ytd_bi_weekly=int(ytd_duration/14)
    ytd_month=int(ytd_duration/30)


    stockdata=Options_Returns.objects.all()
    washdata=Options_Returns.objects.filter(event='Wash')
    ReturnsFilters=ReturnsFilter(request.GET,queryset=stockdata)
    total_returns_on_options=0
    total_returns_on_stocks=0
    transactions=0
    total_proceeds=0
    wash_amount=0
    days_to_expiration=0
    for amt in stockdata:
        total_proceeds += amt.proceeds
        transactions += amt.qty
        total_returns_on_options += amt.ST_GL 
        total_returns_on_stocks += amt.LT_GL

    total_proceeds = float(total_proceeds)
    total_returns_on_options = float(total_returns_on_options)
    total_returns_on_stocks = float(total_returns_on_stocks)
    net_returns=total_returns_on_options + total_returns_on_stocks
    monthly_returns=net_returns/ytd_month
    ytd_bi_weekly_returns=net_returns/ytd_bi_weekly
    weekly_returns=net_returns/ytd_weeks

    for amt in washdata:
        wash_amount += amt.ST_GL
    context = { 
        'title': "CODA INVESTMENT PORTAL",
        # "data": stockdata,
        "data": ReturnsFilters,
        "days_to_expiration": days_to_expiration,
        "total_proceeds": total_proceeds,
        "transactions": transactions,
        "options_amount": total_returns_on_options,
        "stocks_amount": total_returns_on_stocks,
        "wash_amount": wash_amount,
        "net_returns": net_returns,
        "monthly_returns": monthly_returns,
        "bi_weekly_returns": ytd_bi_weekly_returns,
        "weekly_returns": weekly_returns,
        "duration": ytd_month,

    }
    return render(request, "investing/company_returns.html", context)

@login_required
def cost_basis(request):
    ytd_duration,current_year = dates_functionality()
    date_today = datetime.now(timezone.utc)
    ytd_days =ytd_duration
    ytd_weeks=int(ytd_days/7)
    ytd_bi_weekly=int(ytd_days/14)
    ytd_month=int(ytd_days/30)

    stockdata=Cost_Basis.objects.all()

    context = { 
        'title': "COST BASIS ANALYSIS",
        "data": stockdata,
        "duration": ytd_month,

    }
    return render(request, "investing/cost_basis.html", context)
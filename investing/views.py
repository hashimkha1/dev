from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.db.models import Q,Max,F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import CreateView,ListView, DetailView, UpdateView

from datetime import date,datetime,time,timezone
from .utils import (compute_pay,get_over_postions,risk_ratios,
                    computes_days_expiration,get_user_investment,financial_categories)

from main.filters import ReturnsFilter
from main.utils import path_values,dates_functionality

from .forms import (
    OptionsForm,
    InvestmentForm,
    InvestmentRateForm
)


from .models import (
    Unusual_Volume,
    Liquidity,
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
from django.utils import timezone
from getdata.utils import fetch_data_util

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


def optionlist(request):
    title="creditspread"
    return render(request, "main/snippets_templates/output_snippets/option_data.html")


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

class VolumeCreateView(LoginRequiredMixin, CreateView):
    model = Unusual_Volume
    template_name='main/snippets_templates/generalform.html'
    success_url = "/investing/volume"
    fields = "__all__"

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
                        "investing:unusual_volume", 
                        # kwargs={
                        #     'taskid':  self.idval
                        # }
                    )
    
class LiquidityCreateView(LoginRequiredMixin, CreateView):
    model = Liquidity
    template_name='main/snippets_templates/generalform.html'
    success_url = "/investing/liquidity"
    fields = "__all__"

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse(
                        "investing:liquidity", 
                        # kwargs={
                        #     'taskid':  self.idval
                        # }
                    )
    
class LiquidityList(ListView):
    model=Liquidity
    template_name="getdata/options.html"
    context_object_name = "stocks"

class VolumeList(ListView):
    model=Unusual_Volume
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


@login_required
def oversoldpositions(request):
    path_list,sub_title,pre_sub_title = path_values(request)
    # Get current datetime with UTC timezone
    table_name = "investing_oversold"
    get_over_postions(table_name)
    current_date_str = timezone.now().strftime('%Y-%m-%d')
    overboughtsold_records = Oversold.objects.filter(
        Q(expiry__gte=current_date_str) | Q(expiry__isnull=True)
    )
    # overboughtsold_records = Oversold.objects.all()
    # expiry_date,days_to_expiration=computes_days_expiration(stockdata)
    # for record in overboughtsold_records:
        # print("record========>",record)

    context = { 
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

def oversoldpositions(request,symbol=None):
    path_list,sub_title,pre_sub_title = path_values(request)
    # Get current datetime with UTC timezone
    table_name = "investing_oversold"
    get_over_postions(table_name)
    current_date_str = timezone.now().strftime('%Y-%m-%d')
    overboughtsold_records = Oversold.objects.filter(
        Q(expiry__gte=current_date_str) | Q(expiry__isnull=True)
    )
    # overboughtsold_records = Oversold.objects.all()
    # print("symbol=====>",symbol)
    if request.method == "POST":
        ticker_symbol = request.POST['ticker']
        category = request.POST['category']
        # print("category====>",category)
        if category == 'financials':
            url = f'https://finance.yahoo.com/quote/{ ticker_symbol }/{category}?p={ticker_symbol}'
            return redirect(url)
        # Assuming the utility function can handle the category. fetch_financial_data
        # If not, you'll need to modify the utility function or handle the category differently.
        financial_data = fetch_data_util(category,ticker_symbol)
        # print("data=====>",financial_data)
        if category == 'risk':
            if financial_data['beta'] > 1:
                Oversold.objects.filter(symbol=ticker_symbol).update(is_featured=False)

        context = { 
            "overboughtsold": overboughtsold_records,
            "financial_data": financial_data,
            "title":  f"Fetched Financial Data(Yahoo)-{ticker_symbol}",
            "financial_categories": financial_categories,
            "category": category,
            "risk_ratios": risk_ratios,
        }
    else:
        # Handle GET requests (for first-time loading)
        context = {
            "overboughtsold": overboughtsold_records,
            "title": "Click On a Symbol",
            "financial_categories": financial_categories,
        }
    return render(request, "investing/oversold.html", context)

from collections import Counter
from datetime import date, datetime
from django.db.models import Count
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q,Max,F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import  UpdateView
from django import template
from datetime import date,datetime,time,timezone

import openai
from application.models import UserProfile

from main.models import Service, Testimonials
from finance.models import Payment_History, Transaction
from .utils import (compute_pay,risk_ratios,
                    computes_days_expiration, computes_days_expiration_option_return, get_user_investment,financial_categories,investment_rules
                    )
from main.filters import ReturnsFilter
from main.utils import path_values,dates_functionality

from .forms import (
    OptionsForm,
    InvestmentForm,
    InvestmentRateForm
)

from .models import (
    InvestmentContent,
    ShortPut,
    covered_calls,
    credit_spread,
    Investments,
    Investment_rates,
    Oversold,
    OverBoughtSold,
    Options_Returns,
    Cost_Basis,
    Ticker_Data
)
from django.db.models import Q
from accounts.models import CustomerUser
from django.utils import timezone
# from getdata.utils import fetch_data_util
from django.db.models import Subquery, OuterRef, F, CharField


register = template.Library()
User=get_user_model

# Create your views here.
def home(request):
    return render(request, 'main/home_templates/investing_home.html', {'title': 'home'})

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
def get_or_create_investment_content():
    slug = 'your-slug'  # Replace with the actual slug
    try:
        # Try to get existing content
        investment_content = InvestmentContent.objects.filter(slug=slug).first()
        if investment_content and investment_content.description:
            print("Using existing content from the database.")
            return investment_content.description
        else:
            raise InvestmentContent.DoesNotExist
    except InvestmentContent.DoesNotExist:
        # If content doesn't exist, create it with ChatGPT
        openai.api_key = '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'  # Replace with your OpenAI API key
        context = "On the Coda platform, users can collaborate in real-time to create"
        query = "Explain the key features of Coda and how users can benefit from them."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{context}\n\n{query}",
            temperature=0.7,
            max_tokens=200,
            n=1,
        )
        generated_description = response['choices'][0]['text']

        # Create the new content in the database or update the existing one
        investment_content = InvestmentContent.objects.filter(slug=slug).first()
        if investment_content:
            investment_content.description = generated_description
            investment_content.save()
        else:
            InvestmentContent.objects.create(
                slug=slug,
                title="Your Title",  # Replace with your title
                description=generated_description
            )
        print("Generated content using ChatGPT and saved in the database.")
        return generated_description

# Test the function and print the result
print(get_or_create_investment_content())
def InvestmentPlatformOverview(request):
    # count_to_class = {
    #     2: "col-md-6",
    #     3: "col-md-4",
    #     4: "col-md-3"
    # }
    # latest_posts = Testimonials.objects.values('writer').annotate(latest=Max('date_posted')).order_by('-latest')
    # testimonials = []
    # for post in latest_posts:
    #     writer = post['writer']
    #     #querying for the latest post
    #     user_profile = UserProfile.objects.filter(user=writer,user__is_client=True).first()
    #     # user_profile = UserProfile.objects.filter(user=writer).first()
    #     if user_profile:
    #         latest_post = Testimonials.objects.filter(writer=writer, date_posted=post['latest']).first()
    #         testimonials.append(latest_post)

    # number_of_testimonials = len(testimonials)
    # selected_class = count_to_class.get(number_of_testimonials, "default-class")
    # services = Service.objects.filter(is_active=True).order_by('serial')
    investment_content = get_or_create_investment_content()

    # Use the existing or generated content
    generated_content = investment_content # Assuming investment_content is the description field

    data = []
    today = date.today()  # Create a date object
    for year in range(2021, today.year + 1):
        year_data = {
            "year": year,
            "sales": Payment_History.objects.filter(client_date__contains=str(year)).aggregate(total_amount=Sum('payment_fees'))['total_amount'] or 0,
            "expenses": Transaction.objects.filter(
                Q(category__in=["employee", "developer", "other_expense"]),  # Use __in for efficient filtering
                activity_date__year=year
            ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0,
            "net_income": (Payment_History.objects.filter(client_date__contains=str(year)).aggregate(total_amount=Sum('payment_fees'))['total_amount'] or 0) - (Transaction.objects.filter(
                Q(category__in=["employee", "developer", "other_expense"]),  # Use __in again
                activity_date__year=year
            ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0)
        }
        data.append(year_data)
    # Get total active users
    total_active_users = CustomerUser.objects.filter(is_active=True).count()

    # Get active user counts by category
    active_user_counts = CustomerUser.objects.filter(is_active=True).values('category').annotate(count=Count('id'))

    # Create a mapping from numerical values to English names
    category_mapping = dict(CustomerUser.Category.choices, Unknown="Unknown")

    # Replace numerical values with English names in the query result
    active_user_counts_with_names = [
        {'category': category_mapping.get(entry['category'], 'Unknown'), 'count': entry['count']} 
        for entry in active_user_counts
    ]

    # Aggregate counts for each category
    aggregated_counts = {}
    for entry in active_user_counts_with_names:
        category = entry['category']
        count = entry['count']
        if category not in aggregated_counts:
            aggregated_counts[category] = count
        else:
            aggregated_counts[category] += count

    # Create a list of dictionaries with unique category names and their counts
    categories_data = [{'category': category, 'count': count} for category, count in aggregated_counts.items()]

    # Print categories for debugging
    category_names = [entry['category'] for entry in categories_data]
    print("Category Names:", category_names)

    # Fetch data for the bar chart (user registrations this month by subcategory)
    today = date.today()
    current_month = today.month
    monthly_registrations = CustomerUser.objects.filter(
        Q(date_joined__month=current_month) & Q(date_joined__year=today.year)
    ).values('sub_category').annotate(count=Count('id'))

    # Map integer subcategory values to user-friendly labels
    subcategory_mapping = dict(CustomerUser.SubCategory.choices)

    monthly_registrations_data = {
        'labels': [subcategory_mapping.get(entry['sub_category'], 'Unknown') for entry in monthly_registrations],
        'counts': [entry['count'] for entry in monthly_registrations],
    }
    count_to_class = {
        2: "col-md-6",
        3: "col-md-4",
        4: "col-md-3"
    }

    # Query the Investments model to get the relevant data
    investments = Investments.objects.all()

    selected_class = count_to_class.get(len(investments), "default-class")

    context = {
        # "services": services,
        # "posts": testimonials,
        # "title": "layout",
        "investments": investments,
        "selected_class": selected_class,
        # "selected_class": selected_class,
        'generated_content': generated_content,
        'chart_data': data,
        'total_active_users': total_active_users, 
        'categories_data': categories_data,
        # 'active_users_json': active_users_json,
        # 'monthly_registrations_json': monthly_registrations_json
    }
    return render(request, 'investing/platformoverview.html',context)

@login_required
def investments(request):
    investments=Investments.objects.all()
    latest_investment = Investments.objects.latest('investment_date')
    total_amt=0
    for amt  in investments:
        total_amt=total_amt+amt.amount
    amount_invested=float(total_amt)*float(0.33)
    amount = float(total_amt)
    returns=compute_pay(amount)
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
    default_title = "creditspread"
    title = request.GET.get('title', default_title)
    return render(request, "main/snippets_templates/output_snippets/option_data.html", {"title": title})



@login_required
def optiondata(request, title=None,symbol=None, *arg, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    # Taking distinct symbols which meets wash sale rule.
    distinct_returns_symbols = list(set([
        obj.symbol for obj in Options_Returns.objects.all() if obj.wash_days >= 40
    ]))

    filter_name = request.GET.get('filter_by', None)
    extra_filter = request.GET.get('extra_filter_by', None)

    # Taking distinct symbols which in oversold/overbought.
    distinct_overboughtsold_symbols = list(set([
        obj.symbol for obj in OverBoughtSold.objects.all()]))
    # Query to count distinct symbols for each model
    covered_calls_count=covered_calls.objects.all().count()
    shortputdata_count=ShortPut.objects.all().count()
    credit_spread_count=credit_spread.objects.all().count()

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
    page_title = model_mapping[sub_title]['title']  # Renamed to avoid conflict

    context = {
        "data": [],  # Empty data when stockdata does not exist
        "days_to_expiration": 0,
        "subtitle": sub_title,
        "pre_sub_title": pre_sub_title,
        'title': page_title,
        "get_edit_url": "",
        "url_name": "",
    }

    for key, value in model_mapping.items():

        current_stock_model = value['model']
        # Subquery to get the computed value from other_model
        subquery = Ticker_Data.objects.filter(symbol=OuterRef('symbol')).values('industry')[:1]

        # Annotate the queryset with the computed field
        current_stockdata = current_stock_model.objects.distinct().annotate(
            industry = Subquery(subquery, output_field=CharField())
        ) #is_featured=True

        if current_stockdata.exists():  # Using exists() for clarity
            url_mapping = {
                'shortput': 'investing:shortputupdate',
                'credit_spread': 'investing:creditspreadupdate',
                'covered_calls': 'investing:coveredupdate',
            }
            url_name = url_mapping.get(value['model'], '')

            def get_edit_url(row_id):
                return reverse(url_name, args=[row_id])

            # Efficiently fetch all symbols from Options_Returns to avoid repetitive DB calls
            all_return_symbols = Options_Returns.objects.distinct()
            
            current_days_to_expiration = computes_days_expiration(current_stockdata)[1]
            
            # for testing with option_return expiration days, i created this function, but need to test by chrish
            # current_days_to_expiration_returns = computes_days_expiration_option_return(all_return_symbols)[1]
            # print(current_days_to_expiration, current_days_to_expiration_returns)
            
            all_return_symbols = all_return_symbols.values_list('symbol', flat=True)
            
            #filtering symbol which is there in overboughtsold
            filtered_stockdata_by_oversold = [
                x for x in current_stockdata if x.symbol in distinct_overboughtsold_symbols
            ]
           
            #filtering symbol which is not in option_return  
            filtered_stockdata_by_returns = [x for x in filtered_stockdata_by_oversold if x.symbol not in all_return_symbols or (x.symbol in distinct_returns_symbols and current_days_to_expiration >= 21)]
            
    
            context[f"{current_stock_model.__name__.lower()}_option_return_count"] = len(filtered_stockdata_by_returns)
            context[f"{current_stock_model.__name__.lower()}_oversold_count"] = len(filtered_stockdata_by_oversold)
            
            if current_stock_model == stock_model:
                context['days_to_expiration'] = current_days_to_expiration
                context['get_edit_url'] = get_edit_url
                context['url_name'] = url_name

                if filter_name == 'by_option_return':
                    context['data'] = filtered_stockdata_by_returns
                elif filter_name == 'by_over_sold':
                    context['data'] = filtered_stockdata_by_oversold
                else:
                    context['data'] = current_stockdata

                if extra_filter == 'top_5':

                    if key != 'credit_spread':
                        context['data'] = sorted(context['data'], key=lambda x: float(x.raw_return[:-1]), reverse=True)[:5]
                    else:
                        context['data'] = sorted(context['data'], key=lambda x: float(x.sell_strike[1:].replace(',', '')), reverse=True)[:5]
            
    context.update({
        # "data": filtered_stockdata_by_oversold,
        
        "covered_calls_original_count":covered_calls_count,
        "shortput_original_count":shortputdata_count,
        "credit_spread_original_count":credit_spread_count,
        
        # "covered_calls_option_return_count":None,
        # "shortput_option_return_count":None,
        # "credit_spread_option_return_count":None,
        
        # "covered_calls_oversold_count":None,
        # "shortput_oversold_count":None,
        # "credit_spread_oversold_count":None,
        
        # "days_to_expiration": days_to_expiration,
        # "get_edit_url": get_edit_url,
        # "url_name": url_name,

        "categories": investment_rules,
        "subtitle": sub_title,
        "pre_sub_title": pre_sub_title,
        'title': page_title,  # Using renamed title
        
    })
    

    if request.method == 'GET':
        selected_symbol = request.GET.get('symbol')
       
        # Filter data from each model based on the selected symbol
        credit_spread_data = credit_spread.objects.filter(symbol=selected_symbol)
        short_put_data = ShortPut.objects.filter(symbol=selected_symbol)
        covered_calls_data = covered_calls.objects.filter(symbol=selected_symbol)

            # Fetch distinct symbols from all three models
        symbols_from_credit_spread = list(credit_spread.objects.values_list('symbol', flat=True).distinct())
        symbols_from_short_put = list(ShortPut.objects.values_list('symbol', flat=True).distinct())
        symbols_from_covered_calls = list(covered_calls.objects.values_list('symbol', flat=True).distinct())

            # Consolidate the unique symbols
        all_symbols = list(set(
                symbols_from_credit_spread + symbols_from_short_put + symbols_from_covered_calls
            ))
        selected_symbol_action = None
        selected_symbol_stock_price = None
        selected_symbol_strike_price = None
        selected_symbol_days_to_expiry = None
        selected_symbol_annualized_return = None
        selected_symbol_raw_return  = None
        selected_symbol_expiry  = None
        selected_symbol_earnings_date  = None
        if covered_calls_data.exists():
            selected_symbol_action = covered_calls_data.first().action
            selected_symbol_stock_price  = covered_calls_data.first().stock_price
            selected_symbol_strike_price = covered_calls_data.first().strike_price 
            selected_symbol_days_to_expiry = covered_calls_data.first().days_to_expiry
            selected_symbol_annualized_return = covered_calls_data.first().annualized_return
            selected_symbol_earnings_date  = covered_calls_data.first().earnings_date 
            selected_symbol_expiry = covered_calls_data.first().expiry 
            selected_symbol_raw_return = covered_calls_data.first().raw_return
            
            # Update the context with the filtered data and symbols
        context.update({
                'credit_spread_data': credit_spread_data,
                'short_put_data': short_put_data,
                'covered_calls_data': covered_calls_data,
                'symbols': all_symbols,
                'selected_symbol':selected_symbol,
                'selected_symbol_action':selected_symbol_action,
                'selected_symbol_stock_price':selected_symbol_stock_price,
                'selected_symbol_strike_price':selected_symbol_strike_price,
                'selected_symbol_days_to_expiry':selected_symbol_days_to_expiry,
                'selected_symbol_annualized_return':selected_symbol_annualized_return,
                'selected_symbol_earnings_date ':selected_symbol_earnings_date ,
                'selected_symbol_expiry ':selected_symbol_expiry ,
                'selected_symbol_raw_return':selected_symbol_raw_return,
                
            })


    return render(request, "main/snippets_templates/output_snippets/option_data.html", context)
    # else:
    #     context = {
    #         "title": "STOCKS ERROR",
    #         "message": 'Hi, No valid expiry dates found in stockdata..'
    #     }
    # return render(request, "main/errors/generalerrors.html", context)


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
    path_list, subtitle, pre_sub_title = path_values(request)
    covered = get_object_or_404(covered_calls, pk=pk)

    # Check if the object exists
    if not covered:
        context = {
            "title": "STOCKS ERROR",
            "message": 'Hi, No covered_calls matches the given query.'
        }
        return render(request, "main/errors/generalerrors.html", context)
    
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


class oversold_update(UpdateView):
    # model = Oversold
    model = OverBoughtSold
    success_url = "/investing/overboughtsold/None"
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

def ticker_measures(request):
    # Get current datetime with UTC timezone
    ticker_data = Ticker_Data.objects.all()
    context = { 
        "ticker_data": ticker_data,
    }
    return render(request, "investing/ticker_data.html", context)


@login_required
def oversoldpositions(request,symbol=None):
    current_date_str = timezone.now().strftime('%Y-%m-%d')
    # overboughtsold_records = Oversold.objects.filter(
    #     (Q(expiry__gte=current_date_str) | Q(expiry__isnull=True)) & ~Q(comment='') & ~Q(comment__isnull=True)
    # )
    # overboughtsold_records = Oversold.objects.all()
    overboughtsold_records = OverBoughtSold.objects.all()
    

    if symbol is None:
        # Handle GET requests (for first-time loading)
        context = {
            "overboughtsold": overboughtsold_records,
            # "condition":condition,
            "title": "Click On a Symbol",
            "financial_categories": financial_categories,
        }
    else:
        # ticker_symbol = request.POST['ticker']
        ticker_symbol = symbol
        ticker_measures = Ticker_Data.objects.filter(symbol=ticker_symbol)
    
        context = { 
            "overboughtsold": overboughtsold_records,
            # "condition": condition,
            "ticker_data": ticker_measures,
            "title":  f"Fetched Financial Data(Yahoo)-{ticker_symbol}",
            "financial_categories": financial_categories,
            "risk_ratios": risk_ratios,
        }

    return render(request, "investing/oversold.html", context)

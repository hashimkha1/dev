import math
from datetime import date,datetime,time,timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
from coda_project.settings import dba_values ,source_target
User=get_user_model

host,dbname,user,password=dba_values()

from decimal import Decimal

def compute_pay(amount, minimum_amount=Decimal('2000'), base_return=Decimal('5'), inc_rate=Decimal('7'), increment_threshold_amt=Decimal('2000'), decrease_threshold_amt=Decimal('2000')):
    if amount <= minimum_amount:
        print(base_return)
        return base_return
    elif amount <= decrease_threshold_amt:
        print(Decimal(amount),Decimal(minimum_amount))
        difference = (Decimal(amount) -Decimal(minimum_amount)) // increment_threshold_amt
        print(f'{amount},Base Amount:{base_return},difference_amount>2000:{difference},rate:{inc_rate}')
        print(difference * inc_rate)
        print(base_return + difference * inc_rate)
        return base_return + difference * inc_rate
    else:
        remaining_amount = amount - decrease_threshold_amt
        decrease_in_increments = remaining_amount // increment_threshold_amt
        new_increment_rate = max(inc_rate - decrease_in_increments, Decimal('3'))
        return base_return + ((decrease_threshold_amt - minimum_amount) // increment_threshold_amt) * inc_rate + (remaining_amount // increment_threshold_amt) * (new_increment_rate + inc_rate) // Decimal('2')

def get_user_investment(investments, latest_investment_rates):
    if investments.exists():
        minimum_amount = latest_investment_rates.base_amount
        base_return = latest_investment_rates.initial_return
        inc_rate = latest_investment_rates.increment_rate
        increment_threshold_amt = latest_investment_rates.increment_threshold
        decrease_threshold_amt = latest_investment_rates.decrease_threshold
        rate_investment = latest_investment_rates.investment_rate
        minimum_duration = latest_investment_rates.duration
        total_amt = 0

        for amt in investments:
            total_amt += amt.amount

        amount_invested = float(total_amt) * float(rate_investment)
        # print(total_amt,amount_invested,rate_investment)
        total_amount = float(total_amt)
        protected_capital = total_amount - amount_invested
        number = (amount_invested / 1000)
        fractional_part = number - math.floor(number)

        if fractional_part >= 0.5:
            number_positions = math.ceil(number)
        else:
            number_positions = math.floor(number)

        if number_positions > 7:
            number_positions = 7

        returns = compute_pay(amount_invested, minimum_amount, base_return, inc_rate, increment_threshold_amt, decrease_threshold_amt)

    else:
        # Set default values for amount and returns or display an appropriate message
        total_amount = 0.0
        protected_capital = 0.0
        amount_invested = 0.0
        number_positions = 0
        minimum_duration = 0
        returns = 0

    return total_amount, protected_capital, amount_invested, returns, number_positions, minimum_duration


def investment_test():
    # Test cases
    investment_amount_1 = 5000
    investment_amount_2 = 8000
    investment_amount_3 = 11000
    investment_amount_4 = 14000

    return_amount_1 = compute_pay(investment_amount_1)
    return_amount_2 = compute_pay(investment_amount_2)
    return_amount_3 = compute_pay(investment_amount_3)
    return_amount_4 = compute_pay(investment_amount_4)

    # print("Return for $5000 investment:", return_amount_1)
    # print("Return for $8000 investment:", return_amount_2)
    # print("Return for $11000 investment:", return_amount_3)
    # print("Return for $14000 investment:", return_amount_4)

    return return_amount_1,return_amount_2,return_amount_3,return_amount_4


def computes_days_expiration(stockdata):
    date_today = datetime.now(timezone.utc)
    days_to_expiration = 0
    expiry_date = None  # initializing expiry_date here
    
    for x in stockdata:
        if isinstance(x.expiry, str):
            expiry_str = x.expiry
            expirydate = datetime.strptime(expiry_str, "%m/%d/%Y")
            expiry_date = expirydate.astimezone(timezone.utc)
        elif isinstance(x.expiry, datetime):
            expiry_date = x.expiry.astimezone(timezone.utc)
        else:
            continue

        days_to_exp = expiry_date - date_today
        days_to_expiration = days_to_exp.days
        
        
    return expiry_date, days_to_expiration


financial_categories = [
    {
        "title": "statistics",
        "description":"accesses the yahoo valuation Measures",
    },
    {
        "title": "risk",
        "description":"accesses the yahoo yahoo risk informatio",
    },
    {
        "title": "financials",
        "description":"Income(net income),Balance*(Total debt/Equity),Cashflow(Free Cashflow)",
    },
]

investment_rules = {
    "general_rules" : [
                {
                    "rule": "IV(Implied Volatility)",
                    "description":"20-55%",
                },
                {
                    "rule":"Days To Expiration",
                    "description":">21 days",
                },
                {
                    "rule": "Earning date",
                    "description":None
                },
                {
                    "rule": "Annualized Returns",
                    "description":">65%",
                },  
            ],
    "yahoo": [
                {
                    "rule":"EBIDTA",
                    "description":">=0",
                },
                {
                    "rule":"Overall Risk",
                    "description":"<7",
                },
                
    ],
    "thinkorswim": [
                {
                    "rule":"RSI-Scans",
                    "description":"<30 and >80",
                },
                {
                    "rule":"Margin Reqs",
                    "description":"Initial:50% and Maintenace:25%",
                },
    ],
    "reports": [
                {
                    "rule":"Unusual_volume",
                    "description":"",
                },
                {
                    "rule":"liquidity",
                    "description":"",
                },
]
}

risk_ratios = [
        # {
        #         "title":"Alpha (α)",
        #         "description":"performance of an investment against a benchmark. +-->outperformed the benchmark,(-)underperformance.",

        # },
        {
                "title":"Beta (β)",
                "description":"volatility of investment.> 1 more volatile,beta < 1 less volatile.",

        },
        # {
        #         "title":"Mean Annual Return",
        #         "description":"average return over a year.",
        # },
        # {
        #         "title":"R-squared",
        #         "description":"Measures how closely the investment's performance correlates with the benchmark. Values range from 0 to 100. 50->100, the more the investment's performance is explained by the benchmark. below 50 low correlation with the benchmark.",

        # },
        {
                 "title":"std",
                "description":"Represents the volatility or risk of an investment. Higher values more risk.",
        },
        {
                "title":"Sharpe Ratio",
                "description":"Measures risk-adjusted performance. A higher=better risk-adjusted returns. ",
        },

        # {
        #                 "title":"Treynor Ratio",
        #                 "description":"Another measure of risk-adjusted performance. A higher indicates better risk-adjusted performance relative to the market.",
        # }

]
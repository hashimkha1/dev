import psycopg2
import math
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date,datetime,time,timezone
from .models import (ShortPut,covered_calls)
from django.db.models import Q
from coda_project.settings import SITEURL
from django.contrib.auth import get_user_model
from coda_project.settings import dba_values ,source_target
User=get_user_model

host,dbname,user,password=dba_values()


def compute_pay(amount,minimum_amount= 2000, base_return=10, inc_rate=7, increment_threshold_amt=2000, decrease_threshold_amt=3000):
    if amount <= minimum_amount:
        return base_return
    elif amount <= decrease_threshold_amt:
        increments = (amount - minimum_amount) // increment_threshold_amt
        return base_return + increments * inc_rate
    else:
        remaining_amount = amount - decrease_threshold_amt
        decrease_in_increments = remaining_amount // increment_threshold_amt
        new_increment_rate = max(inc_rate - decrease_in_increments, 3)
        return base_return + ((decrease_threshold_amt - minimum_amount) // increment_threshold_amt) * inc_rate + (remaining_amount // increment_threshold_amt) * (new_increment_rate + inc_rate) // 2

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
        total_amount = float(total_amt)
        protected_capital = total_amount - amount_invested
        number = (amount_invested / 1000)
        fractional_part = number - math.floor(number)

        if fractional_part >= 0.5:
            number_positions = math.ceil(number)
        else:
            number_positions = math.floor(number)

        returns = compute_pay(amount_invested, minimum_amount, base_return, inc_rate, increment_threshold_amt, decrease_threshold_amt)

    else:
        # Set default values for amount and returns or display an appropriate message
        total_amount = 0.0
        protected_capital = 0.0
        amount_invested = 0.0
        number_positions = 0
        minimum_duration = 0

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
        
    return expiry_date,days_to_expiration


def get_over_postions(table_name):
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS {} (
                symbol VARCHAR(255),
                action VARCHAR(255),
                strike_price VARCHAR(255),
                implied_volatility_rank VARCHAR(255),
                stock_price VARCHAR(255),
                expiry VARCHAR(255),
                earnings_date VARCHAR(255),
                comment VARCHAR(255),
                is_active BOOLEAN,
                is_featured BOOLEAN
            )
        '''.format(table_name)
        cursor.execute(create_table_query)

        # Commit the changes
        conn.commit()

        # Query the covered_calls table to exclude records with an empty comment field
        over_bought_sold_calls = covered_calls.objects.exclude(Q(comment =' ')|Q(comment ='comment'))

        # Query the ShortPut table to exclude records with an empty comment field
        over_bought_sold_short_puts = ShortPut.objects.exclude(Q(comment =' ')|Q(comment ='comment'))
       
        # Check if each record already exists in the oversold table before appending
        existing_records = set()
        cursor.execute(f'SELECT symbol, action, strike_price FROM {table_name}')
        for row in cursor.fetchall():
            existing_records.add(row[:3])

        # Append the new records that do not exist in the oversold table
        oversold_records = []
        for record in over_bought_sold_calls:
            record_tuple = (
                record.symbol,
                record.action,
                record.strike_price,
                record.implied_volatility_rank,
                record.stock_price,
                record.expiry,
                record.earnings_date,
                record.comment,
                record.is_active,
                record.is_featured
            )
            if record_tuple[:3] not in existing_records:
                oversold_records.append(record_tuple)

        for record in over_bought_sold_short_puts:
            record_tuple = (
                record.symbol,
                record.action,
                record.strike_price,
                record.implied_volatility_rank,
                record.stock_price,
                record.expiry,
                record.earnings_date,
                record.comment,
                record.is_active,
                record.is_featured
            )
            if record_tuple[:3] not in existing_records:
                oversold_records.append(record_tuple)

        # Insert the new records into the oversold table
        if oversold_records:
            cursor.executemany(f'''
                INSERT INTO {table_name} (
                    symbol,
                    action,
                    strike_price,
                    implied_volatility_rank,
                    stock_price,
                    expiry,
                    earnings_date,
                    comment,
                    is_active,
                    is_featured
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', oversold_records)

        # Close the cursor and the connection
        cursor.close()
        conn.close()

    except Exception as e:
        # Handle the exception here (e.g., log the error, display an error message)
        print(f"An error occurred: {str(e)}")


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
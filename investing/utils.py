import psycopg2
from django.urls import reverse
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date,datetime,time,timezone
from .models import (
    ShortPut,
    covered_calls,
    credit_spread,
    Oversold
)
from django.db.models import Q
from accounts.models import CustomerUser
from main.utils import path_values

from django.contrib.auth import get_user_model
from coda_project.settings import dba_values ,source_target
User=get_user_model

host,dbname,user,password=dba_values() #herokudev() #dblocal() #,herokuprod()

def compute_pay(amount):
    if amount <= 2000:
        return 15
    elif amount <= 4000:
        return 15 + (amount - 2000) * (12.5 - 15) / 2000
    elif amount <= 6000:
        return 15 + 12.5 + (amount - 4000) * (10 - 12.5) / 2000
    else:
        return 15 + 12.5 + 10 + (amount - 6000) * (5 - 10) / 2000

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
        over_bought_sold_calls = covered_calls.objects.exclude(comment='')

        # Query the ShortPut table to exclude records with an empty comment field
        over_bought_sold_short_puts = ShortPut.objects.exclude(comment='')

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

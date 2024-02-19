import os
import random
import json
import requests
from datetime import datetime
from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Sum, Max
from django.contrib import messages
from django.conf import settings

# utils.py
from .models import BalanceSheetCategory, Payment_Information, TrainingLoan, Transaction,Payment_History
from accounts.models import Department
from main.utils import App_Categories,generate_chatbot_response
from django.http import JsonResponse

CustomUser = get_user_model()



@login_required
def fetch_and_process_financial_data(request):
    try:
        # Fetch and process transaction data
        transactions_data = Transaction.objects.values('category').annotate(
            total_amount=Sum('amount')
        ).order_by('-total_amount')

        # Fetch and process payment information data
        payment_information_data = Payment_History.objects.values(
            'plan', 'payment_fees', 'down_payment', 'fee_balance'
        ).order_by('-fee_balance')

        # Process the data into the format expected by OpenAI
        transactions_summary = "\n".join([f"{t['category']}: {t['total_amount']}" for t in transactions_data])
        payment_information_summary = "\n".join([f"Plan {p['plan']} - Fees: {p['payment_fees']}, Down Payment: {p['down_payment']}, Balance: {p['fee_balance']}" for p in payment_information_data])

        # Construct the prompt for OpenAI
        prompt = f"Consider the following financial data:\n\nTransactions:\n{transactions_summary}\n\nPayment Information:\n{payment_information_summary}\n\nGenerate the following Balance Sheet format:\n\n{{\n\
           'assets': [\n\
                {{'category': 'amount'}},\n\
                # Add additional categories as needed\n\
            ],\n\
            'Long-term Assets': [\n\
                {{'category': 'amount'}},\n\
                # Add additional categories as needed\n\
            ],\n\
            'liabilities': [\n\
                {{'plan': 'payment fees'}},\n\
                # Add additional liabilities as needed\n\
            ],\n\
            'Long-term Liabilities': [\n\
                {{'plan': 'payment fees'}},\n\
                # Add additional liabilities as needed\n\
            ]\n\
        }} , convert this data into a Balance Sheet, and ensure the following:\n\
        - Display the below mention names Long-term Assets based on a larger amount, and use only below mention assets with smaller amounts.\n\
        - Display the below mention Long-term Liabilities based on a larger amount, and use only below mention liabilities with smaller amounts.\n\
        - change the name of assets category to salary,Cash,Short-term Investments,Accounts Receivable,Inventory,Prepaid Expenses,Equipment,Future Growth Bonds,Technological Advancements,other assets \n\
        - change the name of long term assets category to Long-term Investments,Long-term Receivables,Equity Investment,Property,Partners,Sponsers,Intangible Assets,Talent Appreciation Fund,Contingent Prosperity Provisions \n\
        - change the name of liabilities plan to Short-term Borrowing,Lease Liabilities,Accrued Expenses,Long-term Debt,Deferred Tax Liabilities,Sponsers,Other,liabilities \n\
        - change the name of Long-term Liabilities plan to Long-term Borrowing,Pension Obligations,Accrued Expenses,Contingent Liabilities,Retirement Obligations,Long-term Warranty Provisions,Other,liabilities \n\
        - Do not show duplicate entries."
        # Send the prompt to OpenAI (replace with actual OpenAI call)
        openai_response = generate_chatbot_response(prompt)

        try:
            data_dict = json.loads(openai_response.replace("'", '"'))

            # Extract the balance sheet data from the response
            assets = data_dict.get("assets", [])
            long_term_assets = data_dict.get("Long-term Assets", [])
            liabilities = data_dict.get("liabilities", [])
            long_term_liabilities = data_dict.get("Long-term Liabilities", [])

            # Save the assets, liabilities, long-term assets, and long-term liabilities to the BalanceSheetCategory model
            save_balance_sheet_data(assets, 'Asset')
            save_balance_sheet_data(liabilities, 'Liability')
            save_balance_sheet_data(long_term_assets, 'Long-term Asset')
            save_balance_sheet_data(long_term_liabilities, 'Long-term Liability')

            return {'assets': assets, 'liabilities': liabilities}
        except json.JSONDecodeError as e:
            # Handle JSON parsing error
            print(f"Error processing OpenAI response: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")

    return {assets,long_term_assets,liabilities,long_term_liabilities}

# from django.http import JsonResponse
# import json

def calculate_revenue_and_expenses(request):
    # Calculate total revenue
    revenue_queryset = Payment_Information.objects.aggregate(
        total_payment_fees=Sum('payment_fees'),
        total_down_payments=Sum('down_payment'),
        total_student_bonuses=Sum('student_bonus')
    )

    total_revenue = (
        (revenue_queryset.get('total_payment_fees') or 0) +
        (revenue_queryset.get('total_down_payments') or 0) +
        (revenue_queryset.get('total_student_bonuses') or 0)
    )

    # Calculate total expenses
    expenses_queryset = Transaction.objects.values('category').annotate(
        total_amount=Sum('amount')
    ).order_by()

    # Preparing data for OpenAI prompt
    expenses_summary = "\n".join([f"{t['category']}: {t['total_amount']}" for t in expenses_queryset])
    prompt = f"Generate a financial statement based on the following data:\n\n" \
             f"**Revenue Summary:**\n" \
             f"- Total Payment Fees: {revenue_queryset.get('total_payment_fees') or 0}\n" \
             f"- Total Down Payments: {revenue_queryset.get('total_down_payments') or 0}\n" \
             f"- Total Student Bonuses: {revenue_queryset.get('total_student_bonuses') or 0}\n\n" \
             f"**Total Revenue:**\n" \
             f"{total_revenue}\n\n" \
             f"{expenses_summary}\n\n" \
             f"**Net Income:**\n" \
             f"[net_income]\n\n" \
             f"Please use this data to create a comprehensive financial statement, including total revenue, total expenses, and net income. Ensure the statement is well-organized and provides a clear overview of the financial health. Do not pass any string and make a json response. The generated data should be consistent every time."

    try:
        openai_response = generate_chatbot_response(prompt)
        if openai_response.strip():
            data_dicts = json.loads(openai_response.replace("'", '"'))
            financial_statement = data_dicts.get("Financial Statement", {})
        else:
            print("OpenAI response is empty.")
            financial_statement = {}
    except json.JSONDecodeError as e:
        print(f"Error parsing OpenAI response: {e}")
        financial_statement = {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        financial_statement = {}

    # Process financial statement data
    total_revenue = financial_statement.get("Total Revenue", 0)
    total_expenses = financial_statement.get("Total Expenses", 0)
    net_income = financial_statement.get("Net Income", 0)
    revenue_breakdown = financial_statement.get("Revenue Breakdown", {})
    expense_breakdown = financial_statement.get("Expenses Breakdown", {})

    # Save breakdown data
    save_breakdown_data(revenue_breakdown, 'Revenue')
    save_breakdown_data(expense_breakdown, 'Expenses')

    # Prepare the JSON response
    response_data = {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_income": net_income,
        "revenue_breakdown": revenue_breakdown,
        "expense_breakdown": expense_breakdown,
    }

    return JsonResponse(response_data)

# Additional utility functions like 'generate_chatbot_response' and 'save_breakdown_data' are assumed to be defined elsewhere in your code.

def get_existing_revenue_expenses_data():
    existing_revenue = BalanceSheetCategory.objects.filter(category_type='Revenue')
    existing_expenses = BalanceSheetCategory.objects.filter(category_type='Expenses')
    total_revenue = existing_revenue.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = existing_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    net_income = total_revenue - total_expenses

    return existing_revenue.exists() and existing_expenses.exists(), existing_revenue, existing_expenses, total_revenue, total_expenses,net_income

def save_breakdown_data(breakdown_data, category_type):
    for item in breakdown_data:
        category_name = item.get("category")
        amount = item.get("amount")

        existing_category = BalanceSheetCategory.objects.filter(name=category_name, category_type=category_type).first()

        if existing_category:
            existing_category.amount = float(amount)
            existing_category.save()
            print(f"Updated {category_type}: {category_name} - {amount}")
        else:
            BalanceSheetCategory.objects.create(name=category_name, category_type=category_type, amount=float(amount))
            print(f"Saved {category_type}: {category_name} - {amount}")
def save_balance_sheet_data(data, category_type):
    for item in data:
        for name, amount in item.items():
            existing_category = BalanceSheetCategory.objects.filter(name=name, category_type=category_type).first()
            if existing_category:
                existing_category.amount = float(amount)
                existing_category.save()
                print(f"Updated {category_type}: {name} - {amount}")
            else:
                BalanceSheetCategory.objects.create(name=name, category_type=category_type, amount=float(amount))
                print(f"Saved {category_type}: {name} - {amount}")


# def balance_sheet_analysis(request):
#     # Fetch and process transaction data
#     transactions_data = Transaction.objects.annotate(
#         total_amount=Sum('amount')
#     ).values('category', 'total_amount')

#     # Fetch and process payment information data
#     payment_history_data = Payment_History.objects.values(
#         'plan', 'payment_fees', 'down_payment', 'fee_balance'
#     )

#     # Process the data into the format expected by OpenAI
#     transactions_summary = "\n".join([f"{t['category']}: {t['total_amount']}" for t in transactions_data])
#     payment_history_summary = "\n".join([f"Plan {p['plan']} - Fees: {p['payment_fees']}, Down Payment: {p['down_payment']}, Balance: {p['fee_balance']}" for p in payment_history_data])
#     print(transactions_summary,payment_history_summary)

#     # Construct the prompt for OpenAI
#     prompt = f"Based on the following transaction and payment history information, generate a balance sheet summary.\n\nTransactions:\n{transactions_summary}\n\nPayment History:\n{payment_history_summary}\n\nGenerate balance sheet:"

#     # Send the prompt to OpenAI (placeholder function, replace with actual OpenAI call)
#     openai_response = generate_chatbot_response(prompt)

#     # Handle the OpenAI response (assumes JSON response with keys 'assets', 'liabilities', 'equity')
#     try:
#         data_dict = json.loads(openai_response)
#         assets = data_dict.get("assets", [])
#         liabilities = data_dict.get("liabilities", [])
#         equity = data_dict.get("equity", [])
#     except json.JSONDecodeError as e:
#         print(f"Error processing OpenAI response: {e}")
#         assets, liabilities, equity = [], [], []

#     return assets,liabilities,equity



def calculate_loan(user):
    debit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.DEBIT
    ).aggregate(Sum('value'))
    if debit['value__sum'] == None:
        debit['value__sum'] = 0
    credit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.CREDIT
    ).aggregate(Sum('value'))
    if credit['value__sum'] == None:
        credit['value__sum'] = 0
    loan = debit['value__sum'] - credit['value__sum']
    return loan

def balance_loan(user):
    debit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.DEBIT
    ).aggregate(Sum('value'))
    if debit['value__sum'] == None:
        debit['value__sum'] = 0
    credit = TrainingLoan.objects.filter(
        user=user,
        category=TrainingLoan.CREDIT
    ).aggregate(Sum('value'))
    if credit['value__sum'] == None:
        credit['value__sum'] = 0
    balloan = debit['value__sum'] - credit['value__sum']
    return balloan


def upload_csv(request):
    context = {
        "categories": App_Categories,
    }
    if request.method == "POST":
        csv_file = request.FILES.get("csv_upload")
        if not csv_file.name.endswith(".csv"):
            # return HttpResponseRedirect(request.path_info)
            messages.warning(request, "Not a CSV file")
            return render(request, "getdata/uploaddata.html", context)
        # file= csv_file.read().decode("utf-8")
        try:
            file = csv_file.read().decode("ISO-8859-1")
            file_data = file.split("\n")
            csv_data = [line for line in file_data if line.strip() != ""]
            for x in csv_data:
                fields = x.split(",")
                date = datetime.strptime(str(fields[0]), '%m/%d/%Y').date()
                created = Transaction.objects.update_or_create(
                    activity_date=date,
                    sender=CustomUser.objects.filter(first_name=fields[0]).first(),
                    receiver=fields[2],
                    phone=fields[3],
                    qty=fields[4],
                    amount=fields[5],
                    payment_method=fields[6],
                    department=Department.objects.filter(id=fields[7]).first(),
                    category=fields[8],
                    type=fields[9],
                    description=fields[10],
                    receipt_link=fields[11],
                )
            # url = reverse("admin:index")
            messages.info(request, "data populated successsfully")
            return render(request, "getdata/uploaddata.html", context)
        except Exception as e:
            messages.warning(request, e)
            return render(request, "getdata/uploaddata.html", context)
    if request.method == 'GET':
        return render(request, "getdata/uploaddata.html", context)

    # form = CsvImportForm()
    # data = {"form": form}
    # return render(request, "admin/csv_upload.html", data)

# def EOQ():
#     today = datetime.date.today()
#     lastMonth = today + dateutil.relativedelta.relativedelta(months=-3)
#     task_max_point = TaskHistory.objects.filter(
#         date__gte=lastMonth
#     ).aggregate(Max('point'))['point__max']
#     if(task_max_point > 0):
#         return TaskHistory.objects.filter(point=task_max_point)
#     return False
#
# def EOY():
#     today = datetime.date.today()
#     lastYear = today + dateutil.relativedelta.relativedelta(years=-1)
#     task_max_point = TaskHistory.objects.filter(
#         date__gte=lastYear
#     ).aggregate(Max('point'))['point__max']
#     if(task_max_point > 0):
#         return TaskHistory.objects.filter(point=task_max_point)
#     return False


def check_default_fee(Default_Payment_Fees,username):
    try:
        default_fee = get_object_or_404(Default_Payment_Fees, user=username)
    except:
        default_payment_fees = Default_Payment_Fees(job_down_payment_per_month=500,
				job_plan_hours_per_month=40,
				student_down_payment_per_month=500,
				student_bonus_payment_per_month=100)
        default_payment_fees.save()
        default_fee = Default_Payment_Fees.objects.get(id=1)
    return default_fee


#This function obtains exchange rate information
def get_exchange_rate(base, target):
    # api_key = 'YOUR_APP_ID'
    exchange_api_key = os.environ.get('EXCHANGE_API_KEY')
    # api_key = exchange_api_key
    try:
        url = f'https://openexchangerates.org/api/latest.json?app_id={exchange_api_key}&base={base}'
        response = requests.get(url)
        data = response.json()
        rate=data['rates'][target]
    except:
        rate=139.00
    return rate

# ====================================================================
#DYC Implementation
def DYCpay():
    context_dict = {
        "student": {'cost': 100, 'message': 'if in error kindly go back'},
        "business": {'cost': 200, 'message': 'if in error kindly go back'},
        "greencard": {'cost': 300, 'message': 'if in error kindly go back'},
        
    }
    for usertype, values in context_dict.items():
        if usertype=='student':
            cost= values["cost"]
    return cost
    
# ==================================================
def DYCDefaultPayments():
    context_dict = {
        "student": {'total_amount': 5000, 'down_payment': 500,'early_registration_bonus':100,},
        "business": {'total_amount': 10000, 'down_payment': 500,'early_registration_bonus':100,},
        "greencard": {'total_amount': 20000, 'down_payment': 500,'early_registration_bonus':100,},
    }
    for usertype, values in context_dict.items():
        if usertype=='student':
            total_amount= values["total_amount"]
            down_payment= values["down_payment"]
            early_registration_bonus= values["early_registration_bonus"]
            print(total_amount,down_payment,early_registration_bonus)
    return total_amount,down_payment,early_registration_bonus

# ======================PAYPAL CHARGES============================
def calculate_paypal_charges(amount):
    # Define the PayPal charge brackets and corresponding fees
    charge_brackets = [
        (0, 500.00, 0.029, 0.30),
        (500.01, 1000.00, 0.027, 0.30),
        (1000.01, 5000.00, 0.025, 0.30),
        (5000.01, 10000.00, 0.023, 0.30),
        (10000.01, 15000.00, 0.021, 0.30),
        (15000.01, float('inf'), 0.019, 0.30)
    ]
    # Cast the amount to float
    amount = float(amount)
    # Iterate over the charge brackets to find the applicable fee
    for bracket in charge_brackets:
        start_amount, end_amount, fee_percentage, fee_fixed = bracket
        if start_amount <= amount <= end_amount:
            # Calculate the PayPal charge
            charge = amount * fee_percentage + fee_fixed
            return charge

    # If the amount is not within any of the charge brackets, return None
    return None


def update_link(service_array, user_payment_history, service_categories):
	updated_automation = []
	for automation_service in service_array:
		if automation_service['service_category_slug'] and automation_service['service_category_slug'] in service_categories.keys():
			# import pdb; pdb.set_trace()
			payment_plan=user_payment_history.filter(plan = service_categories[automation_service['service_category_slug']])
			if user_payment_history.filter(plan = service_categories[automation_service['service_category_slug']]).exists():
				updated_automation.append(automation_service)	
			
			else:
				automation_service['link'] = automation_service['service_url']
				updated_automation.append(automation_service)
		else:
			updated_automation.append(automation_service)
	return updated_automation


def generate_and_send_otp(user_email):
    otp = str(random.randint(100000, 999999))
    send_mail(
        'OTP Confirmation',
        f'Your OTP for payment confirmation is: {otp}',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
    return otp

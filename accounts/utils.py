from django.db.models import Q
from django.db.models.aggregates import  Sum
from datetime import date
from accounts.models import CustomerUser,Transaction
from django.contrib.auth import get_user_model

import string
import secrets
import os,requests,openai
import json
from datetime import datetime
from django.db.models import Sum

User = get_user_model()

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%&"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def agreement_data(request):
    contract_data = {}
    contract_data["first_name"] = request.POST.get("first_name")
    contract_data["last_name"] = request.POST.get("last_name")
    contract_data["address"] = request.POST.get("address")
    contract_data["category"] = request.POST.get("category")
    contract_data["sub_category"] = request.POST.get("sub_category")
    contract_data["username"] = request.POST.get("username")
    contract_data["password1"] = request.POST.get("password1")
    contract_data["password2"] = request.POST.get("password2")
    contract_data["email"] = request.POST.get("email")
    contract_data["phone"] = request.POST.get("phone")
    contract_data["gender"] = request.POST.get("gender")
    contract_data["city"] = request.POST.get("city")
    contract_data["state"] = request.POST.get("state")
    contract_data["country"] = request.POST.get("country")
    contract_data["resume_file"] = request.POST.get("resume_file")
    today = date.today()
    contract_date = today.strftime("%d %B, %Y")
    return contract_data,contract_date

def compute_default_fee(category, default_amounts, Default_Payment_Fees):
    if default_amounts:
        default_fee = default_amounts.first()
    else:
        default_fee = Default_Payment_Fees.objects.create(
            job_down_payment_per_month=1000,
            job_plan_hours_per_month=40,
            student_down_payment_per_month=500,
            student_bonus_payment_per_month=100,
            )
    return default_fee

# ================================USERS========================================
def employees():
    active_employees = CustomerUser.objects.filter(
                                             Q(is_staff=True),Q(is_active=True)
                                          ).order_by("-date_joined")
    employees_categories_list = CustomerUser.objects.values_list(
                    'sub_category', flat=True).distinct()
    employees_categories = [subcat for subcat in employees_categories_list if subcat in (1,2,3)]
    employee_subcategories=list(set(employees_categories))
    return (employee_subcategories,active_employees)

# ================================USERS========================================
def get_clients_time(current_info,history_info,trackers):
	# Payment Infor
	payment_latest_record = current_info
	first_history_record = history_info
	history_time = first_history_record.plan if first_history_record else 0
	added_time = payment_latest_record.plan if payment_latest_record else 0
	
	# Examining Tracker
	num = trackers.count()
	Used = trackers.aggregate(Used_Time=Sum("duration"))
	Usedtime = Used.get("Used_Time") if Used.get("Used_Time") else 0
	plantime=history_time+added_time
	try:
		delta = round(plantime - Usedtime)
	except (TypeError, AttributeError):
		delta = 0
	return plantime,history_time,added_time,Usedtime,delta,num


JOB_SUPPORT_CATEGORIES = [
    "Job_Support", "job_support", "jobsupport", "Jobsupport", 
    "JobSupport", "Job Support", "Job support", "job support"
]





# Set the OpenAI API key
# openai.api_key = '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'

# def fetch_sample_data(limit=10):
#     transactions = Transaction.objects.all()[:limit]
#     data = [
#         {
#             "sender": str(transaction.sender),
#             "department": str(transaction.department),
#             "receiver": transaction.receiver,
#             "phone": transaction.phone,
#             "type": transaction.type,
#             "activity_date": transaction.activity_date.strftime('%Y-%m-%d %H:%M:%S'),
#             "receipt_link": transaction.receipt_link,
#             "qty": float(transaction.qty),
#             "amount": float(transaction.amount),
#             "transaction_cost": float(transaction.transaction_cost),
#             "description": transaction.description,
#             "payment_method": transaction.payment_method,
#             "category": transaction.category
#         }
#         for transaction in transactions
#     ]
#     return json.dumps(data, indent=4)

# def generate_data_with_openai(sample_data):
#     prompt = f"Here are some sample transaction records:\n{sample_data}\n\nGenerate 50 new similar transaction records:"

#     response = openai.Completion.create(
#         model="gpt-3.5-turbo-0125",
#         prompt=prompt,
#         max_tokens=2000  
#     )

#     return response.choices[0].text

# def generate_new_transactions(openai_response):
#     new_transactions = json.loads(openai_response)

#     for t in new_transactions:
#         Transaction.objects.create(
#             sender=t["sender"], 
#             department=t["department"],  
#             receiver=t["receiver"],
#             phone=t["phone"],
#             type=t["type"],
#             activity_date=datetime.strptime(t["activity_date"], '%Y-%m-%d %H:%M:%S'),
#             receipt_link=t["receipt_link"],
#             qty=t["qty"],
#             amount=t["amount"],
#             transaction_cost=t["transaction_cost"],
#             description=t["description"],
#             payment_method=t["payment_method"],
#             category=t["category"]
#         )

# # Example usage
# sample_data = fetch_sample_data()
# generated_data = generate_data_with_openai(sample_data)
# generate_new_transactions(generated_data)

def mock_generate_new_transactions():
    # This is a sample format. Adjust it according to your actual data structure
    generated_data = [
        {
            "sender": "Sample Sender 1",
            "department": "HR Department",
            "receiver": "Sample Receiver 1",
            "phone": "123456789",
            "type": "Expense",
            "activity_date": "2022-01-01 10:00:00",
            "receipt_link": "http://example.com/receipt1",
            "qty": 10,
            "amount": 100,
            "transaction_cost": 5,
            "description": "Sample transaction 1",
            "payment_method": "Cash",
            "category": "Salary"
        },
        # Add more sample transactions as needed
    ]
    for transaction_data in generated_data:
        sender_username = transaction_data['sender']
        receiver_username = transaction_data['receiver']

        # Retrieve or create CustomerUser instances
        sender, _ = User.objects.get_or_create(username=sender_username)
        receiver, _ = User.objects.get_or_create(username=receiver_username)

        transaction_data['sender'] = sender.id
        transaction_data['receiver'] = receiver.id
    return json.dumps(generated_data)

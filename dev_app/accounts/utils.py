from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from accounts.models import User
from finance.utils import DYCDefaultPayments


from django.contrib.auth.decorators import login_required

# def get_default_sender():
#     # Custom logic to determine the default sender
#     return User.objects.get(username="default_sender")

@login_required
def user_categories(user,UserCategory):
    # get the current logged in user
    # user = request.user

    # filter UserCategory objects by the current user
    user_categories = UserCategory.objects.filter(user=user)

    # create an empty dictionary to store the category and subcategory names
    categories = {}

    # iterate over the user_categories queryset and populate the categories dictionary
    for category in user_categories:
        category_name = UserCategory.Category(category.category).name
        subcategory_name = UserCategory.SubCategory(category.sub_category).name if category.sub_category else ""
        categories[category_name] = subcategory_name

    # render the categories in a template or return a JSON response
    return categories

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
    # contract_data["city"] = request.POST.get("city")
    # contract_data["state"] = request.POST.get("state")
    # contract_data["country"] = request.POST.get("country")
    # contract_data["resume_file"] = request.POST.get("resume_file")
    today = date.today()
    contract_date = today.strftime("%d %B, %Y")
    return contract_data,contract_date

def compute_default_fee(category, default_amounts,Default_Payment_Fees):
    if default_amounts:
        default_fee = default_amounts.first()
    else:
        if category == "4" : #and subcategory == "1":
            default_fee = Default_Payment_Fees.objects.create(
                job_down_payment_per_month=1000,
                job_plan_hours_per_month=40,
                student_down_payment_per_month=500,
                student_bonus_payment_per_month=100,
            )
        else:
            default_fee = Default_Payment_Fees.objects.create(
                job_down_payment_per_month=1000,
                job_plan_hours_per_month=40,
                student_down_payment_per_month=500,
                student_bonus_payment_per_month=100,
            )
    return default_fee

# ============================FDYC===========================================
def dyc_compute_default_fee(category,subcategory,dyc_default_amounts, Default_Payment_Fees):
    if dyc_default_amounts:
        dyc_default_fee = dyc_default_amounts.first()
    else:
        # if category == "4" and subcategory == "7":
        #     default_fee = Default_Payment_Fees.objects.create(
        #         job_down_payment_per_month=1000,
        #         job_plan_hours_per_month=40,
        #         student_down_payment_per_month=500,
        #         student_bonus_payment_per_month=100,
        #     )
        # else:
        default_fee = Default_Payment_Fees.objects.create(
            job_down_payment_per_month=1000,
            job_plan_hours_per_month=40,
            student_down_payment_per_month=500,
            student_bonus_payment_per_month=100,
        )
    return default_fee


# ================================USERS========================================
def employees():
    active_employees = User.objects.filter(
                                             Q(is_staff=True),Q(is_active=True)
                                          ).order_by("-date_joined")
    employees_categories_list = User.objects.values_list(
                    'sub_category', flat=True).distinct()
    employees_categories = [subcat for subcat in employees_categories_list if subcat in (3,4)]
    employee_subcategories=list(set(employees_categories))
    return (employee_subcategories,active_employees)
from accounts.choices import CategoryChoices,SubCategoryChoices
from finance.models import Payment_History

def check_payment_history_permission_student(user):
    # Define your custom logic here to check if the user has the permission
    # For example, you might check if the user belongs to a specific group or has a certain attribute set.
    
    if user.is_authenticated:
        # if not Payment_History.objects.filter(customer=user).exists() and user.category == CategoryChoices.Student and user.sub_category == SubCategoryChoices.Short_Term:
        #     return  False

        if not Payment_History.objects.filter(customer=user).exists() and user.category == CategoryChoices.Student:
            return  False

        return True
    
    return False

def check_payment_history_permission_job_support(user):
    # Define your custom logic here to check if the user has the permission
    # For example, you might check if the user belongs to a specific group or has a certain attribute set.
    if user.is_authenticated:
        
        if not Payment_History.objects.filter(customer=user).exists() and user.category == CategoryChoices.Jobsupport:
            return  False

        return True
    
    return False
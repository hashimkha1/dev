import math
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import UserForm,shoppingForm
from coda_project import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.urls import reverse
from .models import CustomerUser,shopping
from .utils import agreement_data,employees,compute_default_fee,get_clients_time
from main.filters import UserFilter
# from management.models import Task
#from application.models import UserProfile,Assets
# from finance.models import Payment_History,Payment_Information
# from mail.custom_email import send_email
import string, random
from .utils import generate_random_password,JOB_SUPPORT_CATEGORIES

from django.urls import reverse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from allauth.account.signals import user_logged_in
# from django.dispatch import receiver
# from allauth.socialaccount.models import SocialAccount
from allauth.core.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect

# Create your views here..

# @allowed_users(allowed_roles=['admin'])
def home(request):
    return render(request, "main/home_templates/newlayout.html")

 

def shoppinglist(request):
    shoppings = shopping.objects.all()
    return render(request, "accounts/shoppingList.html", {"shoppings":shoppings})



def shoppingCreate(request):
    if request.method == 'POST':
        form = shoppingForm(request.POST)
        if form.is_valid():
            form.save()
          #  messages.success(request, "goods created successfully.")
            return redirect('accounts:shoppingList') 
    else:
        form = shoppingForm()
    return render(request, 'accounts/shoppingForm.html', {'form':form})


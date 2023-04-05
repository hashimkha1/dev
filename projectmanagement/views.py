import calendar
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.timezone import datetime
from django.contrib.auth import get_user_model,login,authenticate
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import TransactionForm
from .models import Transaction #,Task ,Category Activity, Category, Employee ,Department


#User=settings.AUTH_USER_MODEL
User = get_user_model()


def home(request):
    return render(request, 'main/home_templates/management_home.html',{'title': 'home'})

def construction(request):
    return render(request, 'projectmanagement/construction.html', {'title': 'construction'})

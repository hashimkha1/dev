from django.db.models import Q
from django.utils.text import capfirst
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import (
CreateView,
DeleteView,
ListView,
DetailView,
UpdateView,
)
from.models import InvestmentStrategy
# from .forms import propertiesForm

# User=settings.AUTH_USER_MODEL
import json
from coda_project import settings
User = get_user_model

def investStrategyList(request):
    strategy = InvestmentStrategy.objects.all()
    print("strategy====>",strategy)
    return render(request,"application/strategylist.html",{'strategy':strategy})
import calendar
from datetime import date, datetime, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q
from management.utils import email_template
from .forms import (
    DepartmentForm,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from .models import (
    Services,
)
from data.models import DSU

from django.conf import settings
from django.contrib.auth import get_user_model
from finance.models import Transaction,Inflow,TrainingLoan
from accounts.models import Tracker,Department, TaskGroups
from coda_project import settings
from datetime import date, timedelta
from django.db.models import Q

# User=settings.AUTH_USER_MODEL
User = get_user_model()

class ServicesListView(ListView):
    queryset=Services.objects.all()
    template_name="testing/display.html"

def Services_List(request):
    services = Services.objects.all()
    context={
        "services":services
    }
    return render (request, "testing/display.html",context)

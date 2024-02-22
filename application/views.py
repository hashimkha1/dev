from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Tracker

class TrackerrListView(ListView):
    model = Trackerr
    template_name = 'application/application.list.html'
    context_object_name = 'trackerr'
from django import forms
from django.forms import ModelForm, Textarea
from django.db.models import Q
from data.models import DSU
from accounts.models import CustomerUser
from .models import Services
from finance.models import Transaction,Inflow
from accounts.models import Department

class DepartmentForm(forms.ModelForm):  
    class Meta:  
        model = Department  
        fields = ['name', 'slug','description', 'is_active','is_featured']
        widgets = {"description": Textarea(attrs={"cols": 40, "rows": 2})}

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields["name"].empty_label = "Select"
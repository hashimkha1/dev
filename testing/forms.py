from django import forms
from django.contrib.auth.models import User
from .models import Employee
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = ['name', 'contact', 'email'] #https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'email': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'contact': forms.TextInput(attrs={ 'class': 'form-control' }),
      }

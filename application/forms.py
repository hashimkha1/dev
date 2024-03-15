from django import forms
from django.forms import Textarea
from django.db.models import Q
from .models import (
   Exception
)

class ExceptionForm(forms.ModelForm):
    class Meta:
        model = Exception
        fields = '__all__'

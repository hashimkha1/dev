from django import forms
from django.forms import Textarea
from .models import InvestmentStrategy
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

# from django.db import transaction

class strategyForm(forms.ModelForm):
    class Meta:
        model = InvestmentStrategy
        fields = '__all__'



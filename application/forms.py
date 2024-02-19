from django import forms

#from .models import WCAGSTANDARD_WEBSITE
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator
import re

from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms import ModelForm, Textarea






# class WCAGSTANDARDForm(forms.ModelForm):
#     class Meta:
#         model = WCAGSTANDARD_WEBSITE
#         fields = '__all__'


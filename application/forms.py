from django import forms

from .models import WCAG_STANDARD_WEBSITE
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator
import re

from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms import ModelForm, Textarea






class WCAG_STANDARD_WEBSITEForm(forms.ModelForm):
    class Meta:
        model = WCAG_STANDARD_WEBSITE
        fields = '__all__'


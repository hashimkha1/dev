from django import forms
from django.forms import  Textarea
from .models import WCAGStandard
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator
import re
# from django.db import transaction



class WCAGStandardWebsiteForm(forms.ModelForm):
    class Meta:
        model = WCAGStandard
        fields = '__all__'
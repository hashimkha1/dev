from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
#from accounts.models import CustomerUser, Tracker,CredentialCategory,Credential
#from .models import Testimonials
from django.utils.translation import gettext_lazy as _
# from .models import Expenses
#from data.models import DSU
from .models import WCAG_STANDWEBINTERNATIONAL
# from django.db import transaction

class WCAG_STANDWEBINTERNATIONALForm(forms.ModelForm):
    class Meta:
        model = WCAG_STANDWEBINTERNATIONAL
        fields ='__all__'


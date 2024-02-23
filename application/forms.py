from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
#from accounts.models import CustomerUser, Tracker,CredentialCategory,Credential
#from .models import Testimonials
from django.utils.translation import gettext_lazy as _
# from .models import Expenses
#from data.models import DSU
from .models import WCAG_TAB
# from django.db import transaction

class WCAG_TAB_Form(forms.ModelForm):
    class Meta:
        model = WCAG_TAB
        fields ='__all__'

# class WCAG_TAB_Form(forms.Form):
#     #Enter your website ie www.example.com
#     # web_url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     upload_file = forms.FileField()
#     website_url = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     page_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

#     class Meta:
#         model = WCAG_TAB
#         fields = ['upload_file', 'website_url', 'page_name',]
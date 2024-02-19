from django import forms
from django.forms import  Textarea
from .models import company_properties
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator

# from django.db import transaction

#phone_regex = r'^\d{10}$'

# # #==========================CREDENTIAL FORM================================
# # class CredentialCategoryForm(forms.ModelForm):  
# #     class Meta:  
# #         model = CredentialCategory  
# #         fields = ['department','category', 'slug','description', 'is_active','is_featured']
# #         widgets = {
# #             # Use SelectMultiple below
# #             "category":forms.SelectMultiple(attrs={'class':'form-control', 'category':'category'}),
# #             "description": Textarea(attrs={"cols": 40, "rows": 2})
# #             }

# # class CredentialForm(forms.ModelForm):  
# #     class Meta:  
# #         model = Credential
# #         fields = ['category','name', 'added_by','slug','user_types','description','password','link_name','link','is_active','is_featured']
# #         labels={
# #                 'link_name':'username/email',
# #                 'link':'Link/url',
# #                 'user_types':'Specify Who Can Access this Credential?'
# #         }
# #         widgets = {
# #             # Use SelectMultiple below
# #             "category":forms.SelectMultiple(attrs={'class':'form-control', 'id':'category'}),
# #             "description": Textarea(attrs={"cols": 40, "rows": 2})
# #             }


class propertiesForm(forms.ModelForm):
    class Meta:
        model = company_properties
        fields = '__all__'

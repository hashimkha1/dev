from django import forms
from django.forms import  Textarea
from .models import exception_client
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator
import re
# from django.db import transaction

class xForm(forms.ModelForm):  
     class Meta:  
         model = exception_client
         fields = ['id','date','week','year','comments','type_id','user_id','user_rts_id','flag','pitch_flag','late_nights','vacation']
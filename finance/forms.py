
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    TrainingLoan,

)

class LoanForm(forms.ModelForm):
    class Meta:
        model = TrainingLoan
        fields = [ "user","category","amount","is_active"]
        labels = {
            "user":"user",
            "category":"category",
            "amount":"amount",
            "is_active":"is_active",
        }

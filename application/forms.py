from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Application


class ApplicationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name','username','resume']
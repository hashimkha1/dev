from django import forms
from django.forms import  Textarea
from .models import CustomerUser,Transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator
import re
# from django.db import transaction



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


phone_regex = r'^\d{10}$'

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)
    phone = forms.CharField(label="Phone", max_length=10, validators=[RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits (e.g., 5551234567).",
    )])
    email = forms.EmailField()

    class Meta:
        model = CustomerUser
        fields = [
            "category",
            "sub_category",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "phone",
            "gender",
            "email",
            "address",
            "city",
            "state",
            "country",
            "resume_file",
            "is_staff",
            "is_applicant",
        ]
        labels = {
            "sub_category": "",
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "gender": "",
            "phone": "",
            "address": "",
            "city": "",
            "state": "",
            "country": "",
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")

        # List of disallowed usernames
        disallowed_usernames = ["test", "testing"]

        if username in disallowed_usernames:
            raise forms.ValidationError("This username is not allowed.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        # List of disallowed first names
        disallowed_first_names = ["test", "testing"]

        if first_name in disallowed_first_names:
            raise forms.ValidationError("This first name is not allowed.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        # List of disallowed last names
        disallowed_last_names = ["test", "testing"]

        if last_name in disallowed_last_names:
            raise forms.ValidationError("This last name is not allowed.")
        return last_name

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

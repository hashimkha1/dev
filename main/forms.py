from django import forms
from django.contrib.auth.forms import UserCreationForm

from data.models import DSU


class ContactForm(forms.ModelForm):
    class Meta:
        model = DSU
        fields = [
            "trained_by",
            "client_name",
            "type",
            "category",
            "task",
            "plan",
            "challenge",
            "uploaded",
        ]
        labels = {
            "type": "Client/Staff?",
            "client_name": "Manager",
            "trained_by": "Staff/Employee",
            "category": "Category",
            "task": "What Did You Work On?",
            "plan": "What is your next plan of action on areas that you have not touched on?",
            "challenge": "What specific questions/Challenges are you facing?",
            "uploaded": "Have you uploaded any DAF evidence/1-1 sessions?",
        }
'''
from .models import Codadoc

class CodadocumentsForm(forms.ModelForm):
    class Meta:
        model = Codadoc
        fields = ['id','document_name','description','codadoc']

'''
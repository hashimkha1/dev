from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomerUser, Tracker,CredentialCategory,Credential
from management.models import Whatsapp
from .models import Testimonials
from django.utils.translation import gettext_lazy as _

# from .models import Expenses
from data.models import DSU

# from django.db import transaction
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
            "type": "Are You a Client/Staff?(Select Other if None of the above)",
            "client_name": "Manager",
            "trained_by": "Staff/Employee",
            "category": "Pick your Category</h2>",
            "task": "What Did You Work On?",
            "plan": "What is your next plan of action on areas that you have not touched on?",
            "challenge": "How Can We Help You?",
            "uploaded": "Have you uploaded any DAF evidence/1-1 sessions?",
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['trained_by'].required=False
        self.fields['client_name'].required=False
        self.fields['type'].required=False
        self.fields['category'].required=False
        self.fields['task'].required=False
        self.fields['plan'].required=False
        self.fields['challenge'].required=False
        # self.fields['uploaded'].required=False


class PostForm(forms.ModelForm):
    class Meta:  
        model = Testimonials  
        # fields = ['writer', 'title', 'content']
        fields = ['title', 'content']
        widgets = {"content": Textarea(attrs={"cols": 40, "rows": 3})}

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
class WhatsappForm(forms.ModelForm):
    class Meta:
        model = Whatsapp
        fields = [
                    "group_name",
                    "group_id",
                    "image_url",
                    "message",
                    "product_id",
                    "screen_id",
                    "token",
        ]
        labels = {
                    "group_name":"Enter Whatsapp Group",
                    "group_id ":"Enter Whatsapp Group id",
                    "image_url":"Enter url Image",
                    "message":"Describe the message to be posted",
                    "product_id ":"Enter Product ID",
                    "screen_id":"Enter Screen ID",
                    "token":"Enter token",
        }
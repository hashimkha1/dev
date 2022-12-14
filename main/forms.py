from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Expenses
from data.models import DSU


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['id','sender','receiver','phone','department', 'category','payment_method','quantity','amount','description','receipt']
        labels={
                'sender':'Your full Name',
                'receiver':'Enter Receiver Name',
                'phone':'Receiver Phone',
                'department':'Department',
                'category':'Category',
                'payment_method':'Payment Method',
                'quantity':'Quantity',
                'amount':'Enter Amount',
                'description':'Description',
                'receipt':'Receipt',

        }
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label= "Select"


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
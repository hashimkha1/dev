from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Expense

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['id','sender','receiver','phone','department', 'activity','payment_method','amount','description']
        labels={
                'sender':'Your full Name',
                'receiver':'Enter Receiver Name',
                'phone':'Receiver Phone',
                'department':'Department',
                'activity':'Activity',
                'payment_method':'Payment Method',
                'amount':'Enter Amount',
                'description':'Description',

        }
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label= "Select"
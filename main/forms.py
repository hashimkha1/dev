from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Expenses

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['id','sender','receiver','phone','department', 'category','payment_method','amount','description','receipt']
        labels={
                'sender':'Your full Name',
                'receiver':'Enter Receiver Name',
                'phone':'Receiver Phone',
                'department':'Department',
                'category':'Category',
                'payment_method':'Payment Method',
                'amount':'Enter Amount',
                'description':'Description',
                'receipt':'Receipt',

        }
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label= "Select"
'''
from .models import Codadoc

class CodadocumentsForm(forms.ModelForm):
    class Meta:
        model = Codadoc
        fields = ['id','document_name','description','codadoc']

'''
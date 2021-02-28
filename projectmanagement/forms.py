from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Transanct

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transanct
        fields = ['id','full_name','project_name', 'activity','payment_method','amount','description']
        labels={
                'full_name':'Your full Name',
                'project_name':'Project Name',
                'activity':'Activity',
                'payment_method':'Payment Method',
                'amount':'Enter Amount',
                'description':'Description',

        }
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label= "Select"
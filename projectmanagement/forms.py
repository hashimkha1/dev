from django import forms
from django.forms import ModelForm, Textarea

from .models import Employee, Transaction


class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = ['first_name', 'last_name','contact', 'email'] #https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'email': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'contact': forms.TextInput(attrs={ 'class': 'form-control' }),
      }



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction

        fields = ['id','sender','receiver','phone','department', 'category','type','payment_method','qty','amount','transaction_cost','description','receipt_link']
        labels={
                'sender':'Your full Name',
                'receiver':'Enter Receiver Name',
                'phone':'Receiver Phone',
                'department':'Department',
                'category':'Category',
                'type':'Type',
                'payment_method':'Payment Method',
                'qty':'Quantity',
                'amount':'Unit Price',
                'transaction_cost':'Transaction Cost',
                'description':'Description',
                'receipt_link':'Link',

        }
        widgets = {
            'description': Textarea(attrs={'cols': 30, 'rows': 1})  

        }
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label= "Select"
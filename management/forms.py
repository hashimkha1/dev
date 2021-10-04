from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField,UserCreationForm
from django.contrib.auth.models import User
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
        fields = ['id','sender','receiver','phone','department', 'category','payment_method','qty','amount','description','receipt']
        labels={
                'sender':'Your full Name',
                'receiver':'Enter Receiver Name',
                'phone':'Receiver Phone',
                'department':'Department',
                'category':'Category',
                'payment_method':'Payment Method',
                'qty':'Quantity',
                'amount':'Enter Amount',
                'description':'Description',
                'receipt':'Receipt',

        }
    def __init__(self, *args, **kwargs):
        super(TransactionForm,self).__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label= "Select"
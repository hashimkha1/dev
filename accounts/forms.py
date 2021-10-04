from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User

from .models import CustomerUser
#from django.db import transaction

class CustomerForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ['category','first_name','last_name','username','password1','password2','phone','gender', 'email','address','city','state','country']
        labels={
                'category':'Registering For:',
                'first_name':'First Name',
                'last_name':'Last Name',
                'username':'User Name',
                'email':'Email',
                'gender':'Gender',
                'phone':'Phone',
                'address':'Address',
                'city':'City',
                'state':'State',
                'country':'Country',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(CustomerForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

class Meta:
    model = CustomerUser
    fields = ('email','password','date_joined','is_active','is_admin')

def clean_password(self):
    return self.initial['password']


'''
class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = Employee  
        fields = ['name', 'contact', 'email'] #https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'email': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'contact': forms.TextInput(attrs={ 'class': 'form-control' }),
      }

class CustomerForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = CustomerUser
        fields = ['first_name','last_name','username','phone','gender', 'email','address','city','state','country']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'username':'User Name',
                'email':'Email',
                'gender':'Gender',
                'phone':'Phone',
                'address':'Address',
                'city':'City',
                'state':'State',
                'country':'Country',
        }

#'password1','password2',


#from .models import Customer,Applicant,User
class CustomerSignupForm(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'

    @transaction.atomic
    def data_save(self):
        user=super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('first_name')
        user.save()
        customer=Customer.objects.create(user=user)
        customer.phone=self.cleaned_data.get('phone')
        customer.email=self.cleaned_data.get('email')
        customer.address=self.cleaned_data.get('address')
        customer.city=self.cleaned_data.get('city')
        customer.save()
        return customer
        
class ApplicantSignUpForm(UserCreationForm):
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    phone_number=forms.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'

    @transaction.atomic
    def data_save(self):
        user=super().save(commit=False)
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('first_name')
        user.save()
        applicant=Applicant.objects.create(user=user)
        #applicant.applicant_id=self.cleaned_data.get('applicant_id')
        applicant.username=self.cleaned_data.get('username')
        applicant.phone=self.cleaned_data.get('phone')
        applicant.gender=self.cleaned_data.get('gender')
        applicant.email=self.cleaned_data.get('email')
        applicant.city=self.cleaned_data.get('city')
        applicant.country=self.cleaned_data.get('country')
        applicant.save()
        return applicant
'''
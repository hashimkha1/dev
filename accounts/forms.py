from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
'''
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
from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django.urls import reverse
import calendar
from datetime import datetime
from decimal import *

# Create your models here.
class CustomerUser(AbstractUser):
    class Category(models.IntegerChoices):
        Data_Analysis_Course= 1
        Trading_Course=2
        Employee = 3
        Applicant =4
    class Score(models.IntegerChoices):
        Male = 1
        Female =2
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    email=models.CharField(max_length=100)
    gender=models.IntegerField(default=9999,choices=Score.choices)
    phone=models.CharField(default='90001',max_length=100)
    address=models.CharField(blank=True,null=True,max_length=100)
    city=models.CharField(blank=True,null=True,max_length=100)
    state=models.CharField(blank=True,null=True,max_length=100)
    country=CountryField(blank=True,null=True)
    category=models.IntegerField(default=9999,choices=Category.choices)

    class Meta:
        ordering=['date_joined']

'''
class User(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_applicant=models.BooleanField(default=False)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

class Customer(models.Model):
    class Score(models.IntegerChoices):
        Male = 1
        Female =2
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    email=models.CharField(max_length=100)
    gender=models.IntegerField(choices=Score.choices)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)


class Applicant(models.Model):
    class Score(models.IntegerChoices):
        Male = 1
        Female =2
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    username=models.CharField(max_length=100)
    gender=models.IntegerField(choices=Score.choices)
    phone=models.CharField(default='90001',max_length=100)
    application_date = models.DateTimeField(default=timezone.now)
    phone=models.CharField(max_length=100,blank=True, null=True)
    city=models.CharField(max_length=100,blank=True, null=True)
    country=models.CharField(max_length=100,blank=True, null=True)
    resume=models.FileField(upload_to='resumes/doc/')

     @property
     def get_unique_id(self):
         a = self.last_name[:2].upper()     #First 2 letters of last name
         b = self.birth_date.strftime('%d')     #Day of the month as string
         c = self.city_of_birth[:2].upper()     #First 2 letters of city
         return a + b + c 
'''


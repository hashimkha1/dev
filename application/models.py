from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from random import randint
# # Create your models here.
from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model() 



#

class app_policy(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    upload_date = models.DateTimeField(null=True)
    policy_type = models.CharField(max_length=100)  
    description = models.TextField(null=False)

    def __str__(self):
        return (first_name)

class EmployeeProject(models.Model):
    employee_name = models.CharField(max_length=255)  
    topic = models.CharField(max_length=100)
    uploadlinkurl = models.CharField(max_length=100)
    rating_date = models.DateTimeField()
    projectDescription = models.BooleanField()
    requirementsAnalysis = models.BooleanField()
    development = models.BooleanField()
    testing = models.BooleanField()
    deployment = models.BooleanField()
    totalpoints = models.IntegerField()

    def __str__(self):
        return (employee_name)
   
   

class company_properties(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)  
    purchase_date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
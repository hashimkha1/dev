from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from random import randint
# # Create your models here.
from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model() 



class work_department(models.Model):
    name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=255, null=False)
    is_featured = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=False, null=False)


#class group_task(models.Model):
     #title = models.CharField(max_length=55)
     #description = models.TextField()
     #created_at = models.DateTimeField(auto_now_add=True)
   
 

    def __str__(self):
        return self.name

class policies(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    upload_date = models.DateTimeField(null=True)
    policy_type = models.CharField(max_length=100)  
    description = models.TextField(null=False)   

class company_resources(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)  
    purchase_date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name         
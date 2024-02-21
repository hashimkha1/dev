from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from random import randint
# # Create your models here.
from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model() 






class wcagsWebsite(models.Model):
    website_url  = models.CharField(max_length=500)
    page_name    = models.CharField(max_length=500)
    improvements = models.TextField(null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website_url




#class group_task(models.Model):
     #title = models.CharField(max_length=55)
     #description = models.TextField()
     #created_at = models.DateTimeField(auto_now_add=True)
   
 

    # def __str__(self):
    #     return self.name


 
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from random import randint
# # Create your models here.
from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model() 


class Company_Rating(models.Model):  
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    rating_date = models.DateTimeField()
    punctuality = models.IntegerField()
    communication = models.IntegerField()
    understanding = models.IntegerField()
    rater = models.IntegerField()


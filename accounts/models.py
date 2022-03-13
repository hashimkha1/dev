from decimal import *
import datetime
from datetime import date ,timedelta
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.utils import timezone
from django_countries.fields import CountryField
import requests

# Create your models here.
class CustomerUser(AbstractUser):
    class Category(models.IntegerChoices):
        Client_OR_Customer_or_Student= 1
        Applicant_or_Job_Applicant=2
        # Employee = 3
        # Applicant =4
    class Score(models.IntegerChoices):
        Male = 1
        Female =2
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    email=models.CharField(max_length=100)
    gender=models.IntegerField(choices=Score.choices,blank=True,null=True)
    phone=models.CharField(default='90001',max_length=100)
    address=models.CharField(blank=True,null=True,max_length=100)
    city=models.CharField(blank=True,null=True,max_length=100)
    state=models.CharField(blank=True,null=True,max_length=100)
    country=CountryField(blank=True,null=True)
    category=models.IntegerField(choices=Category.choices,default=999)

    class Meta:
        ordering=['date_joined']

# 1. Correct the number of hours for client
#
'''
class Profile(models.Model):
    user = models.OneToOneField('accounts.CustomerUser', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    #def save(self, *args, **kwargs):
       # super().save(*args, **kwargs)

        # img=image.open(self.image.path)

        # if img.height> 300 or img.width>300:
          #   output_size=(300,300)
           #  img.thumbnail(output_size)
           #  img.save(self.image.path)

class UserProfile(models.Model):
    user = models.OneToOneField('CustomerUser', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
'''

# Time Tracking Model
class Tracker(models.Model):
    class Duration(models.IntegerChoices):
        One_Hour = 1
        Two_Hours =2
        Three_Hours = 3
        Four_Hours = 4
        Five_Hours = 5
        Eight_Hours = 8
        Ten_Hours = 10
    # Job Category.
    Job_Support = 'Job_Support'
    Interview = 'Interview'
    Training = 'Training'
    Mentorship = 'Mentorship'
    Other = 'Other'
    # Task/Activities
    Reporting='reporting'
    Database='database'
    Business_Analysis = 'Business Analysis'
    ETL ='Data Cleaning'
    Other='Any Other'

    CAT_CHOICES = [
        (Job_Support , 'Job_Support'),
        (Interview , 'Interview'),
        (Training , 'Training'),
        (Mentorship , 'Mentorship' ),      
        (Other , 'Other' ),     
       
    ]
    TASK_CHOICES = [
        (Reporting,'reporting'),
        (Database,'database'),
        (Business_Analysis , 'Business Analysis'),
        (ETL ,'Data Cleaning'),
        (Other, 'Other'),
    ]
    category= models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
    )
    task= models.CharField(
        max_length=25,
        choices=TASK_CHOICES,
    )
    plan = models.CharField(
        verbose_name=_('group'),
        help_text=_('Required'),
        max_length=255,
        default="B"
        )
    author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)
    login_date = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    duration = models.IntegerField(choices=Duration.choices,default=2)
    time = models.PositiveIntegerField(
        #max_digits=3, 
            help_text=_('Maximum 200'),
            error_messages={
                "name":{
                   ' max_length':("The maximum hours must be between 0 and 199")
                
                }
            },
            default=120
            )
    class Meta:
        ordering=['login_date']

    def get_absolute_url(self):
        return reverse('tracker-detail', kwargs={'pk': self.pk})

    @property
    def end(self):
        #date_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        date_time = self.login_date + datetime.timedelta(hours=0)
        endtime = date_time.strftime("%H:%M")
        return endtime
    
    @property
    def total_payment(self):
        total = self.duration.objects.aggregate(TOTAL = Sum('duration'))['TOTAL']
        return total
    ''' 
    @property
    def amt_per_plan(self):
        if self.plan=='A':
            return 30
        elif self.plan=='B':
            return 120
        else:
            return 9999
    '''
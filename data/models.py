from django.db.models import Q
from posixpath import basename
import random
import os
import calendar
from decimal import *
from django.utils.translation import gettext_lazy as _
from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import requests
from django.http import request

from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

from django.utils import timezone

#User=settings.AUTH_USER_MODEL
User = get_user_model()

 #==================================INTERVIEWS====================================
class InterviewQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(featured=True ,is_active=True)
        
    def search(self,query):
        lookups=(
                Q(category__icontains=query)|Q(question_type__icontains=query)|
                Q(last_name__icontains=query)|Q(first_name__icontains=query)|
                Q(upload_date__icontains=query)|Q(username__username__icontains=query)
              )
        return self.filter(lookups).distinct()

class InterviewManager(models.Manager):
    def get_queryset(self):
        #return super(TaskManager, self).get_queryset().filter(is_active=True)
        return InterviewQuerySet(self.model,using=self._db)

    def all(self):
        return self.get_queryset()

    """ def featured(self):
        return self.get_queryset().featured() """

    def get_by_slug(self,slug):
        qs=self.get_queryset().filter(slug=slug)
        if qs.count()==1:
            return qs.first()
        return None

    def search(self,query):
        return self.get_queryset().active().search(query)
''' 
#Interview Model
class Uploaded(models.Model):
    # Job Category.
    Project_Management = 'Project Management'
    Business_Analysis = 'Business Analyst'
    Quality_Assurance = 'Quality Assurance'
    User_Experience = 'User Interface'
    Reporting = 'Reporting'
    ETL = 'ETL'
    Database = 'Database'
    Python = 'Python'
    Other = 'Other'
    # Question Type
    Introduction = 'introduction'
    Project_Story = 'Project Story'
    Performance = 'performance'
    Methodology = 'methodology'
    SDLC = 'sdlc'
    Testing = 'testing'
    Environment = 'environment'
    Resume = 'resume'

    CAT_CHOICES = [
        (Project_Management, 'Project Management'),
        (Business_Analysis, 'Business Analysis'),
        (Quality_Assurance, 'Quality Assurance'),
        (User_Experience, 'User Experience'),
        (Reporting, 'Reporting'),
        (ETL, 'ETL'),
        (Database, 'Database'),
        (Python, 'Python'),
        (Other, 'Other'),
    ]
    
    QUESTION_CHOICES = [
    (Introduction , 'introduction'),
    (Project_Story , 'project story'),
    (Performance , 'performance'),
    (Methodology , 'methodology'),
    (SDLC , 'sdlc'),
    (Testing , 'testing'),
    (Environment , 'environment'),
    (Resume , 'resume'),
    (Other, 'Other'),
    ]
    #id = models.AutoField(primary_key=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_interview',default=999)
    #author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)

    first=models.CharField(max_length=100,null=True,blank=True)
    last=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now,null=True,blank=True)

    category= models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default=Other,
    )
    question_type= models.CharField(
        max_length=25,
        choices=QUESTION_CHOICES,
        default=Other,
    )

    doc=models.FileField(default="None",upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)
    is_active=models.BooleanField(default=True)
    featured=models.BooleanField(default=True)

    objects=InterviewManager()

    class Meta:
        verbose_name_plural = 'uploads'   

    def __str__(self):
        return f'{self.username} upload'

'''

#Interview Model
class InterviewUpload(models.Model):
    # Job Category.
    Project_Management = 'Project Management'
    Business_Analysis = 'Business Analyst'
    Quality_Assurance = 'Quality Assurance'
    User_Experience = 'User Interface'
    Reporting = 'Reporting'
    ETL = 'ETL'
    Database = 'Database'
    Python = 'Python'
    Other = 'Other'
    # Question Type
    Introduction = 'introduction'
    Project_Story = 'Project Story'
    Performance = 'performance'
    Methodology = 'methodology'
    SDLC = 'sdlc'
    Testing = 'testing'
    Environment = 'environment'
    Resume = 'resume'

    CAT_CHOICES = [
        (Project_Management, 'Project Management'),
        (Business_Analysis, 'Business Analysis'),
        (Quality_Assurance, 'Quality Assurance'),
        (User_Experience, 'User Experience'),
        (Reporting, 'Reporting'),
        (ETL, 'ETL'),
        (Database, 'Database'),
        (Python, 'Python'),
        (Other, 'Other'),
    ]
    
    QUESTION_CHOICES = [
    (Introduction , 'introduction'),
    (Project_Story , 'project story'),
    (Performance , 'performance'),
    (Methodology , 'methodology'),
    (SDLC , 'sdlc'),
    (Testing , 'testing'),
    (Environment , 'environment'),
    (Resume , 'resume'),
    (Other, 'Other'),
    ]
    #id = models.AutoField(primary_key=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    #midle=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now,null=True,blank=True)

    category= models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default=Other,
    )
    question_type= models.CharField(
        max_length=25,
        choices=QUESTION_CHOICES,
        default=Other,
    )

    doc=models.FileField(default="None",upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    objects=InterviewManager()

    class Meta:
        verbose_name_plural = 'InterviewUploads'   

    def __str__(self):
        return f'{self.username} upload'


class DocUpload(models.Model):
    id = models.AutoField(primary_key=True)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Uploads'

    def __str__(self):
        return f'{self.id} Uploads'


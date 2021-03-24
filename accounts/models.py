'''
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

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
'''
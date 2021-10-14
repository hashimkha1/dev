from decimal import *

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


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
''' 
class UserProfile(models.Model):
    user = models.OneToOneField('CustomerUser', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
'''
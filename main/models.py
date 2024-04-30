from django.contrib.auth.models import User
from django.db import models

from django.db.models import Q
from django.utils.text import slugify
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

# from tableauhyperapi import DatabaseName

User = get_user_model()
# Create your models here.

class BalanceSheetCategory(models.Model):
    CATEGORY_TYPES = [
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Equity', 'Equity'),
    ]

    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='Asset')

    class Meta:
        unique_together = ('name', 'category_type')
        verbose_name_plural = "Balance Sheet Categories"

    def __str__(self):
        return f"{self.name} ({self.category_type})"


class CompanyAsset(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,null=True)
    quantity = models.PositiveIntegerField()
    unit_value = models.DecimalField(max_digits=12,decimal_places=2,default=9999)
    serial_number = models.CharField(max_length=50,null=True)
    purchase_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    location = models.CharField(max_length=50,null=True,blank=True)

    @property
    def total_value(self):
        return self.quantity * self.unit_value

    def __str__(self):
        return self.name  

        from django.db import models

class Application(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.IntegerField()  
    phone = models.CharField(max_length=100)
    application_date = models.DateTimeField()
    country = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')  
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.application_date}"




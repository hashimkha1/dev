from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
'''
class Transanct(models.Model):
    Cash = 'Cash'
    Mpesa = 'Mpesa'
    Check = 'Check'
    Other = 'Other'
    CHOICES = [
        (Cash, 'Cash'),
        (Mpesa, 'Mpesa'),
        (Check, 'Check'),
        (Other, 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    sender=models.CharField(max_length=100,null=True,default=None)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    department=models.CharField(max_length=100,default=None)
    activity=models.CharField(max_length=100,default=None)
    activity_date = models.DateTimeField(default=timezone.now)
    payment_method= models.CharField(
        max_length=25,
        choices=CHOICES,
        default=Other,
    )
    amount = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    description=models.CharField(max_length=100,default=None)
    def __str__(self):
        return f'{self.id} Transanct'
'''
class Expense(models.Model):
    Cash = 'Cash'
    Mpesa = 'Mpesa'
    Check = 'Check'
    Other = 'Other'
    CHOICES = [
        (Cash, 'Cash'),
        (Mpesa, 'Mpesa'),
        (Check, 'Check'),
        (Other, 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    sender=models.CharField(max_length=100,null=True,default=None)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    department=models.CharField(max_length=100,default=None)
    activity=models.CharField(max_length=100,default=None)
    activity_date = models.DateTimeField(default=timezone.now)
    payment_method= models.CharField(
        max_length=25,
        choices=CHOICES,
        default=Other,
    )
    amount = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    description=models.CharField(max_length=100,default=None)
    def __str__(self):
        return f'{self.id} Expense'
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Transanct(models.Model):
    class payment(models.IntegerChoices):
        Cash =1
        Mpesa =2
        Check =3
    id = models.AutoField(primary_key=True)
    full_name=models.CharField(max_length=100)
    project_name=models.CharField(max_length=100,default=None)
    activity=models.CharField(max_length=100,default=None)
    activity_date = models.DateTimeField(default=timezone.now)
    payment_method = models.IntegerField(choices=payment.choices)
    amount = models.CharField(max_length=100,default=None)
    description=models.CharField(max_length=100,default=None)
    def __str__(self):
        return f'{self.id} Transanct'
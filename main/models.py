from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

# from tableauhyperapi import DatabaseName

User = get_user_model()
# Create your models here.


class Picture(models.Model):
    backgroundImage = models.ImageField(default="default.jpg", upload_to="background")


class Assets(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(default='background',max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    # price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(default='Data Analysis',max_length=200,null=True, blank=True)
    # subcategory_category = models.CharField(default='Data Analysis',max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.id} Service"

    def get_absolute_url(self):
        return reverse("main:layout")
        # return reverse('employee-detail', kwargs={'pk': self.pk})

class Order(models.Model):
    service = models.ForeignKey(
        Service, max_length=200, null=True, blank=True, on_delete=models.SET_NULL
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service.name

class Payments(models.Model):
    pay_name = models.CharField(max_length=100, null=True, default=None)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )

    def __str__(self):
        return self.pay_name
from email.policy import default
from django.db.models import Q
from posixpath import basename
import random
import os
import calendar
from decimal import *
from django.forms import CharField
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
from accounts.models import Tracker
from django.utils import timezone

#User=settings.AUTH_USER_MODEL
User = get_user_model()

class Services(models.Model):
    title = models.CharField(
        max_length=55,
        unique=True,
        default="Group A"
    )
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(decimal_places=2,max_digits=20,default=39.99)
    # image=models.ImageField(upload_to=upload_image_path,null=True, blank=True)
    image=models.ImageField(upload_to="Uploads/Images/",null=True, blank=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title

#User=settings.AUTH_USER_MODEL
User = get_user_model()

# class Supplier(models.Model):
#     added_by= models.ForeignKey(
#         User,
#         verbose_name=_("staff"),
#         related_name="staff",
#         null=True,
#         blank=True,
#         on_delete=models.RESTRICT,
#         limit_choices_to={"is_employee": True, "is_active": True},
#     )
#     supplier = models.CharField(
#         max_length=255,
#     )
#     slug = models.SlugField(blank=True, null=True)
#     phone = models.CharField(default="90001",
#             max_length=100,
#             help_text=_("Start with Country Code ie 254******"),
#     )
#     location = models.CharField(max_length=255,default='Makutano')
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     featured=models.BooleanField(default=True)
#     active=models.BooleanField(default=True)

#     def get_absolute_url(self):
#         return "/services/{slug}/".format(slug=self.slug)

#     def __str__(self):
#         return self.supplier

# class Food(models.Model):
#     supplier = models.ForeignKey(
#         Supplier,
#         on_delete=models.RESTRICT,
#         limit_choices_to=Q(active=True)
#     )
#     item = models.CharField(
#         max_length=255,
#         unique=True,
#     )
#     unit_amt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     slug = models.SlugField(blank=True, null=True)
#     qty=models.PositiveIntegerField()
#     bal_qty=models.PositiveIntegerField()
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     featured=models.BooleanField(default=False)
#     active=models.BooleanField(default=True)

#     def get_absolute_url(self):
#         return "/services/{slug}/".format(slug=self.slug)

#     def __str__(self):
#         return self.item
    
#     @property
#     def budgeted_items(self):
#         budgeted_qty=self.qty-self.bal_qty
#         return budgeted_qty

#     @property
#     def total_amt(self):
#         total_amt=Decimal(self.qty-self.bal_qty)*self.unit_amt
#         return total_amt


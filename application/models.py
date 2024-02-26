from datetime import datetime,timedelta
from decimal import *
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q,F
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

#------------create models here----------------
class Balancesheet_categories(models.Model):
    CATEGORY_TYPES = [
        ("assets", 'Asset'),
        ("liability", 'Liability'),
        ("equity", 'Equity'),
    ]

    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=255, choices=CATEGORY_TYPES, default='assets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('name', 'category_type')
        verbose_name_plural = 'Balance Sheet Categories'

    def __str__(self):
        return f"{self.name} ({self.category_type})"

       




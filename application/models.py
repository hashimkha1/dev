# # from coda_project.application.views import first_interview
# from datetime import datetime
# from distutils.command.upload import upload

from django.db import models
from django.utils import timezone
# from accounts.models import CustomerUser
# from main.models import Assets
from django.db.models import Q,F
# from coda_project.storage import GoogleDriveStorage

#===========222222=============================#


class BALANCE_SHEET_CATEGORY11(models.Model):
    CATEGORY_CHOICES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name=models.CharField(max_length=255)
    amount= models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together=('name','category_type')
        verbose_name_plural='Balance sheet categories'
    def __str__(self):
        return f"{self.name} ({self.category_type})"


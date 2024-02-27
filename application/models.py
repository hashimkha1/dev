# # from coda_project.application.views import first_interview
from datetime import datetime
# from distutils.command.upload import upload

from django.db import models
# from django.utils import timezone
# from accounts.models import CustomerUser
# from main.models import Assets
from django.db.models import Q,F
# from coda_project.storage import GoogleDriveStorage

#create models here

class Balance_sheetCategory(models.Model):
    CATEGORY_TYPES = [
        ("assets", "Asset"),
        ("liability", "Liability"),
        ("equity", "Equity"),
    ]
    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=255, choices=CATEGORY_TYPES, default='assets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('name', 'category_type'),)
        verbose_name_plural = 'Balancesheet Categories'

    def __str__(self):
        return f"{self.name} ({self.category_type})"
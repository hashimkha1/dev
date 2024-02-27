# # from coda_project.application.views import first_interview
from datetime import datetime
# from distutils.command.upload import upload

from django.db import models
from django.utils import timezone
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




class BalanceSheetSummary(models.Model):
    date = models.DateField(default=timezone.now)

    @property
    def total_assets(self):
        return self.entries.filter(category__category_type='Asset').aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def total_liabilities(self):
        return self.entries.filter(category__category_type='Liability').aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def total_equity(self):
        return self.entries.filter(category__category_type='Equity').aggregate(models.Sum('amount'))['amount__sum'] or 0

    class Meta:
        verbose_name_plural = "Balance Sheets"
        ordering = ["-date"]

    def __str__(self):
        return f"Balance Sheet as of {self.date}"

class Balance_Sheet_Entry(models.Model):
    balance_sheet = models.ForeignKey('BalanceSheetSummary', on_delete=models.CASCADE, related_name='entries')
    category = models.ForeignKey('Balance_SheetCategory', on_delete=models.CASCADE)
   

    class Meta:
        verbose_name_plural = "Balance Sheet Entries"

    def __str__(self):
        return f"{self.category.name}: {self.amount}"
    

class Balance_Sheet_Entry(models.Model):
    CATEGORY_TYPES = [
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Equity', 'Equity'),
    ]

    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES, default='Asset')

    balance_sheet = models.ForeignKey('BalanceSheetSummary', on_delete=models.CASCADE, related_name='entries')
    category = models.ForeignKey('Balance_SheetCategory', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Balance Sheet Entries"

    def __str__(self):
        return f"{self.category.name}: {self.amount}"



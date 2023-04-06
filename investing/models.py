from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models
from decimal import Decimal
from datetime import datetime,date
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# Create your models here.
class stockmarket(models.Model):
	symbol = models.CharField(max_length=255)
	action = models.CharField(max_length=255)
	qty=models.PositiveIntegerField()
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField()

	class Meta:
		verbose_name_plural = "stockmarket"

class cryptomarket(models.Model):
	symbol = models.CharField(max_length=255)
	action = models.CharField(max_length=255)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	date = models.DateTimeField()

	class Meta:
		verbose_name_plural = "cryptomarket"

	def __str__(self):
		return self.symbol
	
class cread_spread(models.Model):
	Symbol = models.CharField(max_length=255)
	Strategy = models.CharField(max_length=255)
	Type = models.CharField(max_length=255)
	Price = models.CharField(max_length=255)
	Sell_Strike = models.CharField(max_length=255)
	Buy_Strike = models.CharField(max_length=255)
	Expiry = models.CharField(max_length=255)
	Premium = models.CharField(max_length=255)
	Width = models.CharField(max_length=255)
	Prem_Width = models.CharField(max_length=255)
	Rank = models.CharField(max_length=255)
	Earnings_Date = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "cread_spread"

	def __str__(self):
		return self.Symbol
	
class ShortPut(models.Model):
	Symbol = models.CharField(max_length=255)
	Action = models.CharField(max_length=255)
	Expiry = models.CharField(max_length=255)
	Days_To_Expiry = models.CharField(max_length=255)
	Strike_Price = models.CharField(max_length=255)
	Mid_Price = models.CharField(max_length=255)
	Bid_Price = models.CharField(max_length=255)
	Ask_Price = models.CharField(max_length=255)
	Implied_Volatility_Rank = models.CharField(max_length=255)
	Earnings_Date = models.CharField(max_length=255)
	Earnings_Flag =  models.BooleanField(),
	Stock_Price = models.CharField(max_length=255)
	Raw_Return = models.CharField(max_length=255)
	Annualized_Return = models.CharField(max_length=255)
	Distance_To_Strike  = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "ShortPut"

	def __str__(self):
		return self.Symbol

class covered_calls(models.Model):
	Symbol = models.CharField(max_length=255)
	Action = models.CharField(max_length=255)
	Expiry = models.CharField(max_length=255)
	Days_To_Expiry = models.CharField(max_length=255)
	Strike_Price = models.CharField(max_length=255)
	Mid_Price = models.CharField(max_length=255)
	Bid_Price = models.CharField(max_length=255)
	Ask_Price = models.CharField(max_length=255)
	Implied_Volatility_Rank = models.CharField(max_length=255)
	Earnings_Date = models.CharField(max_length=255)
	Earnings_Flag =  models.BooleanField(),
	Stock_Price = models.CharField(max_length=255)
	Raw_Return = models.CharField(max_length=255)
	Annualized_Return = models.CharField(max_length=255)
	Distance_To_Strike  = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "covered_calls"

	def __str__(self):
		return self.Symbol


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    document_date = models.DateTimeField(default=timezone.now)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='document/doc/')

    class Meta:
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f'{self.id} Document'

class Uploads(models.Model):
    id = models.AutoField(primary_key=True)
    document_date = models.DateTimeField(default=timezone.now)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Uploads'

    def __str__(self):
        return f'{self.id} Uploads'
        

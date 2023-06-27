from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.db import models
from decimal import Decimal
from datetime import datetime,date
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model()

# Create your models here.

from django.conf import settings


class Investments(models.Model):
    client = models.ForeignKey(
	    		   User,
			       limit_choices_to={'is_active': True, 'is_client': True},
			       on_delete=models.CASCADE
				   )
    investment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"Investment ID: {self.id}, Client: {self.client.username}"

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
	comment=models.CharField(max_length=255,default='Enter Comment')
	is_active = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = "cread_spread"

	def __str__(self):
		return self.Symbol
	
class ShortPut(models.Model):
	Symbol = models.CharField(max_length=255,blank=True,null=True)
	Action = models.CharField(max_length=255,blank=True,null=True)
	Expiry = models.CharField(max_length=255,blank=True,null=True)
	Days_To_Expiry = models.CharField(max_length=255,blank=True,null=True)
	Strike_Price = models.CharField(max_length=255,blank=True,null=True)
	Mid_Price = models.CharField(max_length=255,blank=True,null=True)
	Bid_Price = models.CharField(max_length=255,blank=True,null=True)
	Ask_Price = models.CharField(max_length=255,blank=True,null=True)
	Implied_Volatility_Rank = models.CharField(max_length=255,blank=True,null=True)
	Earnings_Date = models.CharField(max_length=255,blank=True,null=True)
	Earnings_Flag =  models.CharField(max_length=255,blank=True,null=True),
	Stock_Price = models.CharField(max_length=255,blank=True,null=True)
	Raw_Return = models.CharField(max_length=255,blank=True,null=True)
	Annualized_Return = models.CharField(max_length=255,blank=True,null=True)
	Distance_To_Strike  = models.CharField(max_length=255,blank=True,null=True)
	comment=models.CharField(max_length=255,default='Enter Comment')
	is_active = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=True)

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
	Earnings_Flag =  models.CharField(max_length=255)
	Stock_Price = models.CharField(max_length=255)
	Raw_Return = models.CharField(max_length=255)
	Annualized_Return = models.CharField(max_length=255)
	Distance_To_Strike  = models.CharField(max_length=255)
	comment=models.CharField(max_length=255,default='Enter Comment')
	is_active = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=True)

	class Meta:
		verbose_name_plural = "covered_calls"

	def __str__(self):
		return self.Symbol
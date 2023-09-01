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


class Investor_Information(models.Model):
	investor= models.ForeignKey(
	    		   User,
			       limit_choices_to={'is_active': True, 'is_client': True},
			       on_delete=models.CASCADE
				   )
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	protected_capital = models.DecimalField(max_digits=10, decimal_places=2)
	amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
	duration = models.PositiveIntegerField(blank=True,null=True)
	positions= models.PositiveIntegerField(blank=True,null=True)
	bi_weekly_returns= models.DecimalField(max_digits=10, decimal_places=2)
	payment_method= models.CharField(max_length=255,blank=True,null=True)
	client_signature =models.CharField(max_length=255,blank=True,null=True)
	company_rep= models.CharField(max_length=255,blank=True,null=True)
	contract_date=models.DateField(auto_now_add=True,blank=True,null=True)

	class Meta:
		verbose_name_plural = "Investor_Information"

	def __str__(self):
		return self.payment_method

class Investment_rates(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    created_date = models.DateField(auto_now_add=True,blank=True,null=True)
    base_amount=models.PositiveIntegerField(blank=True,null=True)
    initial_return = models.PositiveIntegerField(blank=True,null=True)
    increment_rate =models.PositiveIntegerField(blank=True,null=True)
    increment_threshold = models.PositiveIntegerField(blank=True,null=True)
    decrease_threshold = models.PositiveIntegerField(blank=True,null=True)
    duration = models.PositiveIntegerField(blank=True,null=True)
    investment_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.33)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Investment_rates"

    def __str__(self):
        return self.name


class Liquidity(models.Model):
	symbol = models.CharField(max_length=255)
	liquidity = models.CharField(max_length=255)
	rank = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

	class Meta:
		verbose_name_plural = "Liquidity"

class Unusual_Volume(models.Model):
	symbol = models.CharField(max_length=255,blank=True, null=True)
	price = models.CharField(max_length=255,blank=True, null=True)
	average_volume = models.CharField(max_length=255,blank=True, null=True)
	expiry = models.CharField(max_length=255,blank=True, null=True)
	strike_price = models.CharField(max_length=255,blank=True, null=True)
	type = models.CharField(max_length=255,blank=True, null=True)
	volume = models.CharField(max_length=255,blank=True, null=True)
	option_sizzle = models.CharField(max_length=255,blank=True, null=True)

	class Meta:
		verbose_name_plural = "Sizzling Options"

	def __str__(self):
		return self.symbol
	
class credit_spread(models.Model):
    symbol = models.CharField(max_length=255,blank=True, null=True)
    strategy = models.CharField(max_length=255,blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    price = models.CharField(max_length=255,blank=True, null=True)
    sell_strike = models.CharField(max_length=255,blank=True, null=True)
    buy_strike = models.CharField(max_length=255,blank=True, null=True)
    expiry = models.CharField(max_length=255,blank=True, null=True)
    premium = models.CharField(max_length=255,blank=True, null=True)
    width = models.CharField(max_length=255,blank=True, null=True)
    prem_width = models.CharField(max_length=255,blank=True, null=True)
    rank = models.CharField(max_length=255,blank=True, null=True)
    earnings_date = models.CharField(max_length=255,blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    on_date = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "credit_spread"

    # def __str__(self):
    #     return self.symbol

class ShortPut(models.Model):
    symbol = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)
    expiry = models.CharField(max_length=255, blank=True, null=True)
    days_to_expiry = models.CharField(max_length=255, blank=True, null=True)
    strike_price = models.CharField(max_length=255, blank=True, null=True)
    mid_price = models.CharField(max_length=255, blank=True, null=True)
    bid_price = models.CharField(max_length=255, blank=True, null=True)
    ask_price = models.CharField(max_length=255, blank=True, null=True)
    implied_volatility_rank = models.CharField(max_length=255, blank=True, null=True)
    earnings_date = models.CharField(max_length=255, blank=True, null=True)
    earnings_flag = models.CharField(max_length=255, blank=True, null=True)
    stock_price = models.CharField(max_length=255, blank=True, null=True)
    raw_return = models.CharField(max_length=255, blank=True, null=True)
    annualized_return = models.CharField(max_length=255, blank=True, null=True)
    distance_to_strike = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    on_date = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "ShortPut"

    # def __str__(self):
    #     return self.symbol

class covered_calls(models.Model):
    symbol = models.CharField(max_length=255,blank=True, null=True)
    action = models.CharField(max_length=255,blank=True, null=True)
    expiry = models.CharField(max_length=255,blank=True, null=True)
    days_to_expiry = models.CharField(max_length=255,blank=True, null=True)
    strike_price = models.CharField(max_length=255,blank=True, null=True)
    mid_price = models.CharField(max_length=255,blank=True, null=True)
    bid_price = models.CharField(max_length=255,blank=True, null=True)
    ask_price = models.CharField(max_length=255,blank=True, null=True)
    implied_volatility_rank = models.CharField(max_length=255,blank=True, null=True)
    earnings_date = models.CharField(max_length=255,blank=True, null=True)
    earnings_flag = models.CharField(max_length=255,blank=True, null=True)
    stock_price = models.CharField(max_length=255,blank=True, null=True)
    raw_return = models.CharField(max_length=255,blank=True, null=True)
    annualized_return = models.CharField(max_length=255,blank=True, null=True)
    distance_to_strike = models.CharField(max_length=255,blank=True, null=True)
    comment = models.CharField(max_length=255,blank=True, null=True)
    on_date = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "covered_calls"

    # def __str__(self):
    #     return self.symbol


class Oversold(models.Model):
    symbol = models.CharField(max_length=255,blank=True, null=True)
    action = models.CharField(max_length=255,blank=True, null=True)
    strike_price = models.CharField(max_length=255,blank=True, null=True)
    implied_volatility_rank = models.CharField(max_length=255,blank=True, null=True)
    stock_price = models.CharField(max_length=255,blank=True, null=True)
    expiry = models.CharField(max_length=255,blank=True, null=True)
    earnings_date = models.CharField(max_length=255,blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    on_date = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "ShortPut"

    def __str__(self):
        return self.symbol
    

class Options_Returns(models.Model):
    symbol=models.CharField(max_length=255,blank=True, null=True)
    expiration_date=models.CharField(max_length=255,blank=True, null=True)
    action=models.CharField(max_length=255,blank=True, null=True)
    event=models.CharField(max_length=255,blank=True, null=True)
    qty=models.CharField(max_length=255,blank=True, null=True)
    strike_price=models.CharField(max_length=255,blank=True, null=True)
    open_date=models.CharField(max_length=255,blank=True, null=True)
    closed_date=models.CharField(max_length=255,blank=True, null=True)
    cost=models.CharField(max_length=255,blank=True, null=True)
    LT_GL=models.CharField(max_length=255,blank=True, null=True)
    ST_GL=models.CharField(max_length=255,blank=True, null=True)
    proceeds=models.CharField(max_length=255,blank=True, null=True)
    covered=models.CharField(max_length=255,blank=True, null=True)
    security_number=models.CharField(max_length=255,blank=True, null=True)
    cbm=models.CharField(max_length=255,blank=True, null=True)
    other=models.CharField(max_length=255,blank=True, null=True)
    description=models.CharField(max_length=255,blank=True, null=True)

    # is_active = models.BooleanField(default=True)
    # is_featured = models.BooleanField(default=True)

    @property
    def wash_days(self):
         date_today = datetime.now(timezone.utc)
         date_today_date = date_today.date()
         wash_days = (date_today_date - self.closed_date).days
         return wash_days
    
    @property
    def wait_time(self):
         wait_time=(self.closed_date-self.open_date).days
         return wait_time

    class Meta:
        verbose_name_plural = "returns"

    def __str__(self):
        return self.symbol
    
class Cost_Basis(models.Model):
    symbol=models.CharField(max_length=255,blank=True, null=True)
    expiration_date=models.CharField(max_length=255,blank=True, null=True)
    action=models.CharField(max_length=255,blank=True, null=True)
    # event=models.CharField(max_length=255,blank=True, null=True)
    qty=models.CharField(max_length=255,blank=True, null=True)
    strike_price=models.CharField(max_length=255,blank=True, null=True)
    open_date=models.CharField(max_length=255,blank=True, null=True)
    cost=models.CharField(max_length=255,blank=True, null=True)
    covered=models.CharField(max_length=255,blank=True, null=True)
    security_number=models.CharField(max_length=255,blank=True, null=True)
    description=models.CharField(max_length=255,blank=True, null=True)

    # is_active = models.BooleanField(default=True)
    # is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "cost_basis"

    def __str__(self):
        return self.symbol
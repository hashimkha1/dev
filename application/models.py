from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from random import randint
# # Create your models here.
from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model()

from django.db import models
class InvestmentStrategy(models.Model):
    symbol = models.CharField(max_length=10)
    action = models.CharField(max_length=50)
    expiry = models.DateField()
    days_to_expiry = models.IntegerField()
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    mid_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    ask_price = models.DecimalField(max_digits=10, decimal_places=2)
    implied_volatility_rank = models.DecimalField(max_digits=5, decimal_places=2)
    earnings_date = models.DateField()
    earnings_flag = models.BooleanField()
    stock_price = models.DecimalField(max_digits=10, decimal_places=2)
    raw_return = models.DecimalField(max_digits=10, decimal_places=2)
    annualized_return = models.DecimalField(max_digits=10, decimal_places=2)
    distance_to_strike = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField()
    on_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.symbol

# class app_policy(models.Model):
#     first_name = models.CharField(max_length=100, null=True)
#     last_name = models.CharField(max_length=100, null=True)
#     upload_date = models.DateTimeField(null=True)
#     policy_type = models.CharField(max_length=100)
#     description = models.TextField(null=False)

# def __str__(self):
#     return (first_name)
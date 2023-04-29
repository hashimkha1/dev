from django.db import models
from django.http import Http404
from decimal import Decimal
from datetime import datetime,date
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# Create your models here.
class CashappMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	full_path = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)
	parsed_date = models.DateTimeField(auto_now_add=True)
	amount = models.CharField(max_length=255,blank=True,null=True)
	destination = models.CharField(max_length=255,blank=True,null=True)

	class Meta:
		verbose_name_plural = "Cashapp"

	def __str__(self):
		return self.subject
	
	@property
	def received_date_format(self):
		time_text_date = self.received_date.replace(" ", "").split(",")[-1]
		new_received_date=datetime.strptime(time_text_date,'%d%b%Y%H:%M:%S+0000').date()
		return new_received_date

class ReplyMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "ReplyMail"

	def __str__(self):
		return self.subject

class Editable(models.Model):
	name = models.CharField(max_length=255,blank=True,null=True)
	putsrow = models.PositiveIntegerField(blank=True,null=True)
	callsrow = models.PositiveIntegerField(blank=True,null=True)

	class Meta:
		verbose_name_plural = "General"

	def __str__(self):
		return self.name

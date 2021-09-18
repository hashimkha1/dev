from django.db import models
from django.utils import timezone

# Create your models here.
class Picture(models.Model):
    backgroundImage = models.ImageField(default='default.jpg', upload_to='background')

'''

class Codadoc(models.Model):
    id = models.AutoField(primary_key=True)
    document_name=models.CharField(max_length=100)
    #codalink=models.CharField(max_length=10000)
    date_uploaded = models.DateTimeField(default=timezone.now)
    codadoc=models.FileField(default=None,upload_to='codadoc/doc/')
    description = models.TextField(max_length=220, blank=True, default=None)
    #cover=models.FileField(default=None,upload_to='cover/doc/')
 
    def __str__(self):
        return f'{self.document_name} Codadoc'

'''

from django.db import models

# Create your models here.

class Service(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank=True)
	image_url = models.CharField(max_length=1000, null=True, blank=True)
	price = models.FloatField(null=True, blank=True)

	def __str__(self):
		return self.name


class Order(models.Model):
	service = models.ForeignKey(Service, max_length=200, null=True, blank=True, on_delete = models.SET_NULL)
	created =  models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.service.name



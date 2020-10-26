from django.db import models
from django.utils import timezone

# Create your models here.
class Picture(models.Model):
    backgroundImage = models.ImageField(default='default.jpg', upload_to='background')
'''
class Codadocuments(models.Model):
    id = models.AutoField(primary_key=True)
    document_name=models.CharField(max_length=100)
    #codalink=models.CharField(max_length=10000)
    date_uploaded = models.DateTimeField(default=timezone.now)
    codadoc=models.FileField(default=None,upload_to='codadoc/doc/')
    description = models.TextField(max_length=220, blank=True, default=None)
    #cover=models.FileField(default=None,upload_to='cover/doc/')
 
    def __str__(self):
        return f'{self.document_name} Codadocuments'

class Codadocs(models.Model):
    id = models.AutoField(primary_key=True)
    document_name=models.CharField(max_length=100)
    #codalink=models.CharField(max_length=10000)
    date_uploaded = models.DateTimeField(default=timezone.now)
    codadoc=models.FileField(default=None,upload_to='codadoc/doc/')
    description = models.TextField(max_length=220, blank=True, default=None)
    #cover=models.FileField(default=None,upload_to='cover/doc/')
 
    def __str__(self):
        return f'{self.document_name} Codadocs'
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


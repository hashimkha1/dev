from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    document_date = models.DateTimeField(default=timezone.now)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='document/doc/')

    def __str__(self):
        return f'{self.id} Document'

class Uploads(models.Model):
    id = models.AutoField(primary_key=True)
    document_date = models.DateTimeField(default=timezone.now)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return f'{self.id} Uploads'
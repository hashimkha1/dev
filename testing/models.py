from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Employee(models.Model):
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    contact = models.CharField(max_length=15)
    entry_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('employee-list')
        #return reverse('employee-detail', kwargs={'pk': self.pk})
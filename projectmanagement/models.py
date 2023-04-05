from django.db.models import Q
import calendar
from datetime import datetime
from decimal import *
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.contrib.auth import get_user_model

#User=settings.AUTH_USER_MODEL
User = get_user_model()


#--------------------------------------

class Transaction(models.Model):
# Method of Payment
    Cash = 'Cash'
    Mpesa = 'Mpesa'
    Check = 'Check'
    Other = 'Other'
    #  Cost Category.
    Salary='Salary'
    Health='Health'
    Transport='Transport'
    Food_Accomodation='Food & Accomodation'
    Internet_Airtime='Internet & Airtime'
    Recruitment='Recruitment'
    Labour='Labour'
    Management='Management'
    Electricity='Electricity'
    Construction='Construction'
    Other = 'Other'

    # Department
    HR = 'HR Department'
    IT = 'IT Department'
    MKT = 'Marketing Department'
    FIN = 'Finance Department'
    SECURITY = 'Security Department'
    MANAGEMENT = 'Management Department'
    HEALTH = 'Health Department'
    Other='Other'
    DEPARTMENT_CHOICES = [
        (HR , 'HR Department'),
        (IT , 'IT Department'),
        (MKT , 'Marketing Department'),
        (FIN , 'Finance Department'),
        (SECURITY , 'Security Department'),
        (MANAGEMENT , 'Management Department'),
        (HEALTH , 'Health Department'),
        (Other , 'Other'),
        ]
    CAT_CHOICES = [
        (Salary,'Salary'),
        (Health,'Health'),
        (Transport,'Transport'),
        (Food_Accomodation,'Food & Accomodation'),
        (Internet_Airtime,'Internet & Airtime'),
        (Recruitment,'Recruitment'),
        (Labour,'Labour'),
        (Management,'Management'),
        (Electricity,'Electricity'),
        (Construction,'Construction'),
        (Other , 'Other'),
        ]
    PAY_CHOICES = [
        (Cash, 'Cash'),
        (Mpesa, 'Mpesa'),
        (Check, 'Check'),
        (Other, 'Other'),
        ]
    sender=models.CharField(max_length=100,null=True,default=None)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    department=models.CharField(max_length=100,default=None)
    type=models.CharField(max_length=100,default=None,null=True)
    activity_date = models.DateTimeField(default=timezone.now)
    receipt_link=models.CharField(max_length=100,blank=True, null=True)
    qty= models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    transaction_cost = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    description=models.TextField(max_length=1000, default=None)

    payment_method= models.CharField(
            max_length=25,
            choices=PAY_CHOICES,
            default=Other,
        )
    department= models.CharField(
            max_length=100,
            choices=DEPARTMENT_CHOICES,
            default=Other,
        )

    category= models.CharField(
            max_length=100,
            choices=CAT_CHOICES,
            default=Other,
        )
    class Meta:
            verbose_name_plural = 'Transactions'

    def __str__(self):
            return f'{self.id} Transactions'

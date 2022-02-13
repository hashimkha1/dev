import calendar
from datetime import datetime
from decimal import *
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

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
    #id = models.AutoField(primary_key=True,default=99999999)
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

    def get_absolute_url(self):
        return reverse('management:transaction-detail', kwargs={'pk': self.pk})
        
    class Meta:
            verbose_name_plural = 'Transactions'

    def __str__(self):
            return f'{self.id} Transactions'

# -------------------------------------CASH FLOW MODEL---------------------------------------
class Outflow(models.Model):
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
    employee = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)
    sender=models.CharField(max_length=100,null=True,default=None)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    department=models.CharField(max_length=100,default=None)
    type=models.CharField(max_length=100,default=None,null=True)
    activity_date = models.DateTimeField(default=timezone.now)
    #receipt_link=models.CharField(max_length=100,blank=True, null=True)
    #upload_receipt=models.FileField(default=None,upload_to='Receipt/doc/')
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

    def get_absolute_url(self):
        return reverse('management:outflow_detail', kwargs={'pk': self.pk})
        
    class Meta:
            verbose_name_plural = 'Transactions'

    def __str__(self):
            return f'{self.id} Transactions'

# -------------------------------------CASH FLOW MODEL---------------------------------------

class Inflow(models.Model):
    # Period of Payment
    Weekly = 'Weekly'
    Bi_Weekly ='Bi_Weekly'
    Monthly = 'Monthly'
    Yearly = 'Yearly'

    # Method of Payment
    Cash = 'Cash'
    Mpesa = 'Mpesa'
    Check = 'Check'
    Cashapp = 'Cashapp'
    Zelle = 'Zelle'
    Venmo = 'Venmo'
    Paypal = 'Paypal'

    # Category.
    Job_Support = 'Job_Support'
    Interview = 'Interview'
    Training = 'Training'
    Stocks = 'Stocks'
    Blockchain = 'Blockchain'
    Mentorship = 'Mentorship'
    Other = 'Other'
    # Task/Activities
    Reporting='reporting'
    Database='database'
    Business_Analysis = 'Business Analysis'
    ETL ='Data Cleaning'
    Options='Options'
    Other='Any Other'

    PERIOD_CHOICES = [
        (Weekly, 'Weekly'),
        (Bi_Weekly,'Bi_Weekly'),
        (Monthly, 'Monthly'),
        (Yearly, 'Yearly'),
    ]

    CAT_CHOICES = [
        (Job_Support , 'Job_Support'),
        (Interview , 'Interview'),
        (Training , 'Training'),
        (Stocks ,'Stocks'),
        (Blockchain ,'Blockchain'),
        (Mentorship , 'Mentorship' ),      
        (Other , 'Other' ),     
    ]
    TASK_CHOICES = [
        (Reporting,'reporting'),
        (Database,'database'),
        (Business_Analysis , 'Business Analysis'),
        (ETL ,'Data Cleaning'),
        (Options,'Options'),
        (Other, 'Other'),
    ]

    PAY_CHOICES = [
        (Cash, 'Cash'),
        (Mpesa, 'Mpesa'),
        (Check, 'Check'),
        (Cashapp ,'Cashapp'),
        (Zelle , 'Zelle'),
        (Venmo , 'Venmo'),
        (Paypal , 'Paypal'),
        (Other, 'Other'),
        ]

    category= models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
    )
    task= models.CharField(
        max_length=25,
        choices=TASK_CHOICES,
    )
    method= models.CharField(
        max_length=25,
        choices=PAY_CHOICES,
        default=Other,
        )
    
    period= models.CharField(
        max_length=25,
        choices=PERIOD_CHOICES,
        default=Other,
        )

    sender = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    transaction_date = models.DateTimeField(default=timezone.now)
    receipt_link=models.CharField(max_length=100,blank=True, null=True)
    qty= models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    transaction_cost = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=0)
    description=models.TextField(max_length=1000, default=None)

    class Meta:
        ordering=['transaction_date']

    def get_absolute_url(self):
        return reverse('management:inflow-detail', kwargs={'pk': self.pk})

    @property
    def end(self):
        #date_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        date_time = self.login_date + datetime.timedelta(hours=0)
        endtime = date_time.strftime("%H:%M")
        return endtime

    @property
    def total_payment(self):
        total = self.amount.objects.aggregate(TOTAL = Sum('amount'))['TOTAL']
        return total

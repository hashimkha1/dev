from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Picture(models.Model):
    backgroundImage = models.ImageField(default='default.jpg', upload_to='background')

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

class Expenses(models.Model):
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
    id = models.AutoField(primary_key=True)
    sender=models.CharField(max_length=100,null=True,default=None)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    department=models.CharField(max_length=100,default=None)
    activity_date = models.DateTimeField(default=timezone.now)
    receipt=models.FileField(upload_to='Uploads/Receipt_doc/', null=False)
    quantity=models.IntegerField( null=False)
    amount = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
    description=models.TextField(default=None)

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
            verbose_name_plural = 'Expenses'

    def __str__(self):
            return f'{self.id} Expenses'

    def get_absolute_url(self):
        return reverse('transaction-list')
        #return reverse('employee-detail', kwargs={'pk': self.pk})
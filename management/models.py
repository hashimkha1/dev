from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
import calendar
from dateutil.parser import parse
from datetime import datetime
from decimal import *
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
    id = models.AutoField(primary_key=True)
    sender=models.CharField(max_length=100,null=True,default=None)
    receiver=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=50,null=True,default=None)
    department=models.CharField(max_length=100,default=None)
    activity_date = models.DateTimeField(default=timezone.now)
    receipt=models.FileField(default="None",upload_to='Uploads/Receipt_doc/')
    qty= models.PositiveIntegerField(default=1)
    amount = models.DecimalField (max_digits=10, decimal_places=2, null=True, default=None)
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
            verbose_name_plural = 'Expenses'

    def __str__(self):
            return f'{self.id} Expenses'
'''
class ActivityManager(models.Manager):
    def get_queryset(self):
        return super(ActivityManager, self).get_queryset().filter(is_active=True)
'''

class Department(models.Model):
    """Department Table will provide a list of the different departments in CODA"""
    name = models.CharField(
        verbose_name=_('Department Name'),
        help_text=_('Required'),
        max_length=255, 
        unique=True,
        )

    slug = models.SlugField(verbose_name=_('Department safe URL'), max_length=255, unique=True)

    is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name=_('Department')
        verbose_name_plural=_('Departments')

    def get_absolute_url(self):
        return reverse('management:department_list', args=[self.slug])

    def __str__(self):
        return self.name   

class Employee(models.Model):
    """Employee Table will provide a list of the employees working on activities"""
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(
        verbose_name=_('Employee Name'),
        help_text=_('Required'),
        max_length=255, 
        unique=True,
        )
    last_name = models.CharField(
        verbose_name=_('Employee Name'),
        help_text=_('Required'),
        max_length=255, 
        unique=True,
        )

    email = models.EmailField(
        verbose_name=_('email'),
        help_text=_('Required'),
        max_length=255, 
        unique=True,
        )
    contact = models.CharField(max_length=15)
    entry_date = models.DateTimeField(_('entered on'),auto_now_add=True, editable=True)
    is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name=_('Employee')
        verbose_name_plural=_('Employees')
    
    def get_absolute_url(self):
        return reverse('employee-list')
        #return reverse('employee-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.last_name
'''  
     @property
     def get_unique_id(self):
         a = self.last_name[:2].upper()     #First 2 letters of last name
         b = self.birth_date.strftime('%d')     #Day of the month as string
         c = self.city_of_birth[:2].upper()     #First 2 letters of city
         return a + b + c 
''' 

class Category(MPTTModel):
    '''Category Table implemented with MPTT'''
    department=models.ForeignKey(Department, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_('Category'),
        help_text=_('Required and Unique'),
        max_length=255, 
        unique=True,
        )
    slug = models.SlugField(verbose_name=_('Category safe URL'), max_length=255, unique=True)
    parent=TreeForeignKey('self',on_delete=models.CASCADE,null=True, blank=True,related_name="children")
    is_active=models.BooleanField(default=True)

    def get_all_activities(self):
        # To display all activities from all subcategories
        return Activity.objects.filter(category__in=self.get_descendants(include_self=True))
        
    class MPTTMeta:
        order_insertion_by =['name']

    class Meta:
        verbose_name=_('Category')
        verbose_name_plural=_('Categories')

    def get_absolute_url(self):
        return reverse('management:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Activity(models.Model):
    category = models.ForeignKey(Category, related_name='acitivity', on_delete=models.CASCADE)
    created_by = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE, related_name='activity_creator')
    activity_name = models.CharField(
        verbose_name=_('Activity Name'),
        help_text=_('Required'),
        max_length=255, 
        )
    description = models.TextField(
        verbose_name=_('description'),
        help_text=_('Not Required'),
        )
    slug = models.SlugField(max_length=255)
    point = models.PositiveIntegerField(
            #max_digits=3, 
            help_text=_('Should be less than Maximum Points assigned'),
            error_messages={
                "name":{
                   ' max_length':("Points must be less than Maximum Points")
                
                }
            },
            )
    mx_point = models.PositiveIntegerField(
            #max_digits=3, 
            help_text=_('Maximum 200'),
            error_messages={
                "name":{
                   ' max_length':("The maximum points must be between 0 and 199")
                
                }
            },
            )
    mx_earning = models.DecimalField(
            max_digits=10, 
            help_text=_('Maximum 4999.99'),
            error_messages={
                "name":{
                   ' max_length':("The earning must be between 0 and 4999.99")
                
                }
            },
            decimal_places=2 
            )
    submission = models.DateTimeField(
         help_text=_('Date formart :mm/dd/yyyy'),
         auto_now_add=False,
         auto_now=False,
         blank=False,
         null=False
         )
    created = models.DateTimeField(_('created on'),auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated at'),auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def late_penalty(self):
        #submission=datetime.strptime(str(self.submission),'%Y-%m-%d %H:%M:%S+%f:%z')
        submission=datetime.date(self.submission)
        today = datetime.today()
        deadline_date=datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
        #deadline=datetime.strptime(str(deadline_date),'%Y-%m-%d %H:%M:%S')
        deadline=datetime.date(deadline_date)
       
        if submission >deadline:
            return 0.98
        else:
            return 1
    @property
    def pay(self):
        if self.point>self.mx_point:
            return 0
        else:
            Earning= round(Decimal(self.point/self.mx_point)*self.mx_earning ,2)
            compute_pay=Earning * Decimal(self.late_penalty)
            pay=round(compute_pay)
            return pay
        
        
        
        

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ('-created',)

    def get_absolute_url(self):
       return reverse('management:activity-detail', args=[self.slug])
    
    def __str__(self):
        return self.activity_name



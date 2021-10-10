'''
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
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=200)
    point = models.PositiveBigIntegerField(default=10)
    mxpoint = models.PositiveBigIntegerField(default=10)
    earning = models.CharField(max_length=200, default=10)

    @property
    def pay(self):
        if self.point>self.mx_point:
            return 0
        else:
            compute_pay= round(Decimal(self.point/self.mx_point)*self.mx_earning ,2)
            #compute_pay=Earning * Decimal(self.late_penalty)
            pay=round(compute_pay)
            return pay


    def __str__(self):
        return self.name


class Category(models.Model):
    #Category Table implemented with MPTT
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)
    name = models.CharField(
        verbose_name=_('Category'),
        help_text=_('Required and Unique'),
        max_length=255, 
        unique=True,
        )
    slug = models.SlugField(verbose_name=_('Category safe URL'), max_length=255, unique=True)
    is_active=models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    class Meta:
        verbose_name=_('Category')
        verbose_name_plural=_('Categories')
        ordering = ('ordering',)

    def get_absolute_url(self):
        return '/%s/' % (self.slug)

    #def get_absolute_url(self):
        #return reverse('management:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Task(models.Model):
    category = models.ForeignKey(Category, related_name='task', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    added_by = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE, related_name='task_creator')
    task_name = models.CharField(
        verbose_name=_('task Name'),
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
            help_text=_('Maximum 200'),
            error_messages={
                "name":{
                   ' max_length':("The quantity must be between 0 and 199")
                
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
    link=models.CharField(max_length=255,blank=True, null=True)
    is_active=models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)


    @property
    def updated(self):
        updated=datetime.date(self.submission)
        return updated

    @property
    def deadline(self):
        today = datetime.today()
        deadline_date=datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[-1])
        #deadline=datetime.strptime(str(deadline_date),'%Y-%m-%d %H:%M:%S')
        deadline=datetime.date(deadline_date)
        return deadline

    @property
    def late_penalty(self):
        #submission=datetime.strptime(str(self.submission),'%Y-%m-%d %H:%M:%S+%f:%z')
        submission=datetime.date(self.submission)

        if submission >self.deadline:
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
        return '/%s/%s/' % (self.category.slug, self.slug)

    #def get_absolute_url(self):
       #return reverse('management:task-detail', args=[self.slug])
    
    def __str__(self):
        return self.task_name

'''


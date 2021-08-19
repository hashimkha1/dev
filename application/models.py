#from coda_project.application.views import first_interview
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from DateTime import datetime,date
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Applicant_Profile(models.Model):
    applicant = models.OneToOneField('accounts.CustomerUser', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='applicant_profile_pics')

    def __str__(self):
        return f'{self.applicant.username} Applicant_Profile'

class Application(models.Model):
    class Score(models.IntegerChoices):
        Male = 1
        Female =2
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(default='90001',max_length=100)
    application_date = models.DateTimeField(default=timezone.now)
    phone=models.CharField(max_length=100,blank=True, null=True)
    country=models.CharField(max_length=100,blank=True, null=True)
    resume=models.FileField(upload_to='resumes/doc/')
    #cover=models.FileField(default=None,upload_to='cover/doc/')

    def __str__(self):
        return f'{self.username} application'

class InteviewUploads(models.Model):
    Id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=30,null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    ppt=models.FileField(default=None,upload_to='Powerpoints/doc/')
    report=models.FileField(default=None,upload_to='Reports/doc/')
    workflow=models.FileField(default=None,upload_to='Workflows/doc/')
    proc=models.FileField(default=None,upload_to='Procedures/doc/')
    other=models.FileField(default=None,upload_to='Others/doc/')
    Applicant=models.ManyToManyField(Application)

    def __str__(self):
        return f'{self.username} InteviewUploads'

class Policy(models.Model):
    Leave = 'Leave'
    Working_Hours = 'Working Hours'
    Working_Days = 'Working Days'
    Unpaid_Training = 'Unpaid Training'
    Location = 'Location'
    Other = 'Other'
    CHOICES = [
        (Leave, 'Leave'),
        (Working_Hours, 'Working Hours'),
        (Working_Days, 'Working Days'),
        (Unpaid_Training, 'Unpaid_Training'),
        (Location, 'Location'),
        (Other, 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    policy_type= models.CharField(
        max_length=25,
        choices=CHOICES,
        default=Other,
    )
    description = models.TextField()
    policy_doc=models.FileField(upload_to='policy/doc/',default=None,null=True,blank=True)

    def __str__(self):
        return f'{self.id} policy'

class Rated(models.Model):
    class Score(models.IntegerChoices):
        very_Poor = 1
        Poor =2
        Good = 3
        Very_good = 4
        Excellent = 5
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    topic=models.CharField(max_length=100,default=None)
    rating_date = models.DateTimeField(default=timezone.now)
    punctuality = models.IntegerField(choices=Score.choices)
    communication = models.IntegerField(choices=Score.choices)
    understanding = models.IntegerField(choices=Score.choices)

    def __str__(self):
        return f'{self.id} Rating'

class Employee(models.Model):
    class Score(models.IntegerChoices):
        very_Poor = 1
        Poor =2
        Good = 3
        Very_good = 4
        Excellent = 5
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    topic=models.CharField(max_length=100,default=None)
    employee_date = models.DateTimeField(default=timezone.now)
    punctuality = models.IntegerField(choices=Score.choices)
    communication = models.IntegerField(choices=Score.choices)
    understanding = models.IntegerField(choices=Score.choices)
    rated_by=models.CharField(default="CEO",max_length=100)
    
    def __str__(self):
        return f'{self.id} Employee'

class FirstUpload(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    ppt=models.FileField(upload_to='Powerpoints/doc/')
    report=models.FileField( upload_to='Reports/doc/',null=True,blank=True)
    workflow=models.FileField(upload_to='Workflows/doc/',null=True,blank=True)
    proc=models.FileField(upload_to='Procedures/doc/',null=True,blank=True)
    other=models.FileField(default="None",upload_to='Others/doc/')
    Applicant=models.ManyToManyField(Application)

    def __str__(self):
        return f'{self.username} upload'

class Reporting(models.Model):
    internal = 'Internal Interview'
    first_interview = 'First Interview'
    second_interview = 'Second Interview'
    third_interview = 'Third Interview'
    male = 'Male'
    female = 'Female'
    direct = 'Direct'
    indirect = 'Indirect'
    INTERVIEW_CHOICES = [
        (internal, 'Internal Interview'),
        (first_interview, 'First Interview'),
        (second_interview, 'Second Interview'),
        (third_interview, 'Third Interview'),
        
    ]
    GENDER_CHOICES= [
        (male, 'Male'),
        (female, 'Female'),
    ]
    METHOD_CHOICES= [
        (direct , 'Direct'),
        (indirect , 'Indirect'),
    ]
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    #gender=models.CharField(max_length=50,null=True,blank=True)
    #method=models.CharField(max_length=50,null=True,blank=True)
    interview_type= models.CharField(
        max_length=25,
        choices=INTERVIEW_CHOICES,
    )
    gender= models.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=GENDER_CHOICES,
    )
    method= models.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=METHOD_CHOICES,
    )
    reporting_date = models.DateTimeField("Reporting Date(mm/dd/yyyy)",auto_now_add=False,auto_now=False,blank=True,null=True)
    update_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    comment= models.TextField()

    def __str__(self):
        return f'{self.id} Reporting'


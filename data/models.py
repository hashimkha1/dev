from django.db import models
from django.utils import timezone

# Create your models here.
class Upload(models.Model):
    Project_Management = 'Project Management'
    Business_Analysis = 'Business Analyst'
    Quality_Assurance = 'Quality Assurance'
    User_Experience = 'User Interface'
    Reporting = 'Reporting'
    ETL = 'ETL'
    Database = 'Database'
    Python = 'Python'
    Other = 'Other'
    CHOICES = [
        (Project_Management, 'Project Management'),
        (Business_Analysis, 'Business Analysis'),
        (Quality_Assurance, 'Quality Assurance'),
        (User_Experience, 'User Experience'),
        (Reporting, 'Reporting'),
        (ETL, 'ETL'),
        (Database, 'Database'),
        (Python, 'Python'),
        (Other, 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now,null=True,blank=True)

    doc_type= models.CharField(
        max_length=25,
        choices=CHOICES,
        default=Other,
    )
    resume=models.FileField(upload_to='cvs/doc/')
    introduction=models.FileField( upload_to='intro/doc/',null=True,blank=True)
    project_Story=models.FileField(upload_to='pm/doc/',null=True,blank=True)
    sdlc=models.FileField(upload_to='sdlc/doc/',null=True,blank=True)
    environment=models.FileField(default="None",upload_to='environment/doc/')
    performance=models.FileField(default="None",upload_to='performance/doc/')
    testing=models.FileField(default="None",upload_to='testing/doc/')

    def __str__(self):
        return f'{self.username} upload'


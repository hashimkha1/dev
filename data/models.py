from django.db import models
from django.utils import timezone

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

    class Meta:
        verbose_name_plural = 'Uploads'

    def __str__(self):
        return f'{self.username} upload'

#Interview Model of Interest
class InterviewUpload(models.Model):
    # Job Category.
    Project_Management = 'Project Management'
    Business_Analysis = 'Business Analyst'
    Quality_Assurance = 'Quality Assurance'
    User_Experience = 'User Interface'
    Reporting = 'Reporting'
    ETL = 'ETL'
    Database = 'Database'
    Python = 'Python'
    Other = 'Other'
    # Question Type
    Introduction = 'introduction'
    Project_Story = 'Project Story'
    Performance = 'performance'
    Methodology = 'methodology'
    SDLC = 'sdlc'
    Testing = 'testing'
    Environment = 'environment'
    Resume = 'resume'

    CAT_CHOICES = [
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
    
    QUESTION_CHOICES = [
    (Introduction , 'introduction'),
    (Project_Story , 'project story'),
    (Performance , 'performance'),
    (Methodology , 'methodology'),
    (SDLC , 'sdlc'),
    (Testing , 'testing'),
    (Environment , 'environment'),
    (Resume , 'resume'),
    (Other, 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now,null=True,blank=True)

    category= models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default=Other,
    )
    question_type= models.CharField(
        max_length=25,
        choices=QUESTION_CHOICES,
        default=Other,
    )

    doc=models.FileField(default="None",upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'InterviewUploads'   

    def __str__(self):
        return f'{self.username} upload'

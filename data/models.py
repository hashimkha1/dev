from django.db import models
from django.utils import timezone


#Interview Model
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

class Upload(models.Model):
    id = models.AutoField(primary_key=True)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Uploads'

    def __str__(self):
        return f'{self.id} Uploads'

'''
class Cat(models.Model):
    category =models.CharField(max_length=100,blank=True, null=True)
    description=models.CharField(max_length=1000,blank=True, null=True)
    link=models.CharField(max_length=100,blank=True, null=True)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.id} Cat'

        '''
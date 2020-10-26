from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Applicant_Profile(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='applicant_profile_pics')

    def __str__(self):
        return f'{self.applicant.username} Applicant_Profile'

class Application(models.Model):
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

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    #username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    topic=models.CharField(max_length=100,default=None)
    rating_date = models.DateTimeField(default=timezone.now)
    punctuality=models.IntegerField(blank=True, null=True)
    communication=models.IntegerField(blank=True, null=True)
    understanding=models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.id} Rating'
'''
    @property
    def total_score(self):
        #returns the total score for candidates
        return self.punctuality+self.communication+self.topic
    total_score=total_score()
    #resume=models.FileField(upload_to='resumes/doc/')
    #cover=models.FileField(default=None,upload_to='cover/doc/')
'''


'''
    def baby_boomer_status(self):
            "Returns the person's baby-boomer status."
        import datetime
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"
'''
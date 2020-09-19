from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Applicant_Profile(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='applicant_profile_pics')

    def __str__(self):
        return f'{self.applicant.username} Applicant_Profile'


class Application(models.Model):
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    #last_name=models.CharField(default="None",max_length=100, NULL=False)
    #phone=models.CharField(default=None,max_length=100)
    #country=models.CharField(default=None,max_length=100)
    resume=models.FileField(upload_to='resumes/doc/')
    #cover=models.FileField(default=None,upload_to='cover/doc/')

    def __str__(self):
        return f'{self.username} application'



# from coda_project.application.views import first_interview
from datetime import datetime
from distutils.command.upload import upload

from django.db import models
from django.utils import timezone

# Create your models here.
class Applicant_Profile(models.Model):
    user = models.OneToOneField("accounts.CustomerUser", on_delete=models.CASCADE)
    section = models.CharField(max_length=2, default="A", blank=True)
    image = models.ImageField(
        default="default.jpg", upload_to="applicant_profile_pics", blank=True
    )
    upload_a = models.FileField(upload_to="applicant_profile/uploads")
    upload_b = models.FileField(upload_to="applicant_profile/uploads")
    upload_c = models.FileField(upload_to="applicant_profile/uploads")

    def __str__(self):
        return f"{self.user.username} Applicant Profile"


class Application(models.Model):
    class Sex(models.IntegerChoices):
        Male = 1
        Female = 2

    # Method of Payment
    Applicant = "Applicant"
    Other = "Other"

    APPLICATION_CHOICES = [
        (Applicant, "Applicant"),
        (Other, "Other"),
    ]
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.IntegerField(choices=Sex.choices, default=9999)
    phone = models.CharField(default="90001", max_length=100)
    application_date = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/doc/", blank=True, null=True)
    # cover=models.FileField(default=None,upload_to='cover/doc/')
    type = models.CharField(
        max_length=25,
        choices=APPLICATION_CHOICES,
        default=Other,
    )

    @property
    def submitted(self):
        submitted = datetime.date(self.application_date)
        return submitted

    def __str__(self):
        return f"{self.username} application"


class InteviewUploads(models.Model):
    Id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    ppt = models.FileField(default=None, upload_to="Powerpoints/doc/")
    report = models.FileField(default=None, upload_to="Reports/doc/")
    workflow = models.FileField(default=None, upload_to="Workflows/doc/")
    proc = models.FileField(default=None, upload_to="Procedures/doc/")
    other = models.FileField(default=None, upload_to="Others/doc/")
    Applicant = models.ManyToManyField(Application)

    def __str__(self):
        return f"{self.username} InteviewUploads"


class Policy(models.Model):
    Leave = "Leave"
    Working_Hours = "Working Hours"
    Working_Days = "Working Days"
    Unpaid_Training = "Unpaid Training"
    Location = "Location"
    Other = "Other"
    CHOICES = [
        (Leave, "Leave"),
        (Working_Hours, "Working Hours"),
        (Working_Days, "Working Days"),
        (Unpaid_Training, "Unpaid_Training"),
        (Location, "Location"),
        (Other, "Other"),
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    policy_type = models.CharField(
        max_length=25,
        choices=CHOICES,
        default=Other,
    )
    description = models.TextField()
    policy_doc = models.FileField(
        upload_to="policy/doc/", default=None, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} policy"


class Rated(models.Model):
    class Score(models.IntegerChoices):
        very_Poor = 1
        Poor = 2
        Good = 3
        Very_good = 4
        Excellent = 5

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100, default=None)
    rating_date = models.DateTimeField(default=timezone.now)
    punctuality = models.IntegerField(choices=Score.choices)
    communication = models.IntegerField(choices=Score.choices)
    understanding = models.IntegerField(choices=Score.choices)

    def __str__(self):
        return f"{self.id} Rating"


"""
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
   # Applicant=models.ManyToManyField(Application)

    def __str__(self):
        return f'{self.username} upload'
"""


class Reporting(models.Model):
    internal = "Internal Interview"
    first_interview = "First Interview"
    second_interview = "Second Interview"
    third_interview = "Third Interview"
    male = "Male"
    female = "Female"
    direct = "Direct"
    indirect = "Indirect"
    INTERVIEW_CHOICES = [
        (internal, "Internal Interview"),
        (first_interview, "First Interview"),
        (second_interview, "Second Interview"),
        (third_interview, "Third Interview"),
    ]
    GENDER_CHOICES = [
        (male, "Male"),
        (female, "Female"),
    ]
    METHOD_CHOICES = [
        (direct, "Direct"),
        (indirect, "Indirect"),
    ]
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    # gender=models.CharField(max_length=50,null=True,blank=True)
    # method=models.CharField(max_length=50,null=True,blank=True)
    interview_type = models.CharField(
        max_length=25,
        choices=INTERVIEW_CHOICES,
    )
    gender = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=GENDER_CHOICES,
    )
    method = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        choices=METHOD_CHOICES,
    )
    reporting_date = models.DateTimeField(
        "Reporting Date(mm/dd/yyyy)",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,
    )
    update_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.id} Reporting"

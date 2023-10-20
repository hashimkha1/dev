# from coda_project.application.views import first_interview
from datetime import datetime
from distutils.command.upload import upload

from django.db import models
from django.utils import timezone
from accounts.models import CustomerUser
from main.models import Assets
from django.db.models import Q
# from coda_project.storage import GoogleDriveStorage

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(
        "accounts.CustomerUser", related_name="profile", on_delete=models.CASCADE
    )
    position = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    company = models.CharField(max_length=254, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)
    section = models.CharField(max_length=2, default="A", blank=True)

    image = models.ImageField(
        default="default.jpg", upload_to="Application_Profile_pics", blank=True
    )
    image2 = models.ForeignKey(
        Assets, related_name="profile_image", on_delete=models.CASCADE,default=1
    )

    upload_a = models.FileField(upload_to="Application_Profile/uploads", null=True, blank=True)
    upload_b = models.FileField(upload_to="Application_Profile/uploads", null=True, blank=True)
    upload_c = models.FileField(upload_to="Application_Profile/uploads", null=True, blank=True)

    is_active = models.BooleanField("Is featured", default=True)
    laptop_status= models.BooleanField("Is lap_status", default=True)

    national_id_no = models.CharField(max_length=254, null=True, blank=True)
    id_file = models.ImageField(upload_to='id_files/', null=True, blank=True)

    emergency_name = models.CharField(max_length=254, null=True, blank=True)
    emergency_address = models.CharField(max_length=254, null=True, blank=True)
    emergency_citizenship = models.CharField(max_length=254, null=True, blank=True)
    emergency_national_id_no = models.CharField(max_length=254, null=True, blank=True)
    emergency_phone = models.CharField(max_length=254, null=True, blank=True)
    emergency_email = models.CharField(max_length=254, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} Applicant Profile"

    @property
    def img_url(self):
        if self.image2:
            return self.image2.image_url
        else:
            return "default_image_url.jpg"

    @property
    def img_category(self):
        img_cat=self.image2.category
        return img_cat

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
    phone = models.CharField(default="90001", max_length=100, blank=True, null=True)
    application_date = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/doc/", blank=True, null=True)
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


# class InteviewUploads(models.Model):
#     Id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=30, null=True)
#     upload_date = models.DateTimeField(default=timezone.now)
#     ppt = models.FileField(default=None, upload_to="Powerpoints/doc/")
#     report = models.FileField(default=None, upload_to="Reports/doc/")
#     workflow = models.FileField(default=None, upload_to="Workflows/doc/")
#     proc = models.FileField(default=None, upload_to="Procedures/doc/")
#     other = models.FileField(default=None, upload_to="Others/doc/")
#     Applicant = models.ManyToManyField(Application)

#     def __str__(self):
#         return f"{self.username} InteviewUploads"


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
    # class Score(models.IntegerChoices):
    #     very_Poor = 1
    #     Poor = 2
    #     Good = 3
    #     Very_good = 4
    #     Excellent = 5

    Type = [
        ("Exam", "Exam"),
        ("Symbosium", "Symbosium"),
        ("Exam_ChatGPT", "Exam_ChatGPT"),
        ("Other", "Other"),
    ]
    TOPIC_CHOICES = [
        ("Alteryx", "Alteryx"),
        ("Tableau", "Tableau"),
        ("Database", "Database"),
        ("Python", "Python"),
        ("SAS", "SAS"),
        ("English", "English"),
        ("Kiswahili", "Kiswahili"),
        ("Math", "Math"),
        ("Business", "Business"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("Biology", "Biology"),
        ("GHC", "GHC"),
        ("CRE", "CRE"),
        ("Agriculture", "Agriculture"),
        ("Other", "Other"),
    ]
    id = models.AutoField(primary_key=True)
    employeename =  models.ForeignKey(
                    "accounts.CustomerUser", limit_choices_to=Q(is_staff=True)|Q(is_applicant=True), 
                    on_delete=models.CASCADE, related_name="rating_empname",default=1,blank=True)
    type = models.CharField(
        max_length=255,
        choices=Type,
        default='Other'
    )
    topic = models.CharField(
        max_length=255,
        choices=TOPIC_CHOICES,
        default='Other'
    )
    uploadlinkurl = models.CharField(max_length=1000,blank=True, null=True)
    rating_date = models.DateTimeField(default=timezone.now)
    projectDescription = models.BooleanField(default=False)# 2
    requirementsAnalysis  = models.BooleanField(default=False)# 3
    development = models.BooleanField(default=False)# 5
    testing = models.BooleanField(default=False)# 3
    deployment = models.BooleanField(default=False)# 2
    totalpoints = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} Rating"


class Reporting(models.Model):
    internal = "Internal Interview"
    first_interview = "First Interview"
    second_interview = "Second Interview"
    third_interview = "Third Interview"
    Other = "Other"
    direct = "Direct"
    indirect = "Indirect"

    INTERVIEW_CHOICES = [
        (internal, "Internal Interview"),
        (first_interview, "First Interview"),
        (second_interview, "Second Interview"),
        (third_interview, "Third Interview"),
        (Other, "Other"),
    ]
    METHOD_CHOICES = [
        (direct, "Direct"),
        (indirect, "Indirect"),
    ]
    id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(
        "accounts.CustomerUser",
        related_name="reporting_user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        #  limit_choices_to=Q(is_staff=True)|Q(is_admin=True) | Q(is_superuser=True) and Q(is_active=True),
        # limit_choices_to={"is_staff": True, "is_active": True},
    )
    name=models.CharField(max_length=50,null=True,blank=True)
    rate=models.CharField(max_length=50,null=True,blank=True)
    interview_type = models.CharField(
        max_length=25,
        choices=INTERVIEW_CHOICES,
        default="other"
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
    link=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return f"{self.id} Reporting"
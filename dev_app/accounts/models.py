from datetime import timedelta
from decimal import *
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.modelmanager import DepartmentManager
from django_countries.fields import CountryField

# Create your models here.
class CustomerUser(AbstractUser):
    class Category(models.IntegerChoices):
        Job_Applicant = 1
        Coda_Staff_Member = 2
        Jobsupport = 3
        Student = 4
        investor = 5
        General_User = 6

    # added this column here
    class SubCategory(models.IntegerChoices):
        No_selection = 0
        Full_time = 1
        Contractual = 2
        Agent = 3
        Short_Term = 4
        Long_Term = 5
        Other = 6

    class Score(models.IntegerChoices):
        Male = 1
        Female = 2

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=100)
    gender = models.IntegerField(choices=Score.choices, blank=True, null=True)
    phone = models.CharField(default="90001", max_length=100)
    address = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    country = CountryField(blank=True, null=True)
    category = models.IntegerField(choices=Category.choices, default=999)
    # added this column here
    sub_category = models.IntegerField(
        choices=SubCategory.choices, blank=True, null=True
    )
    is_admin = models.BooleanField("Is admin", default=False)
    is_staff = models.BooleanField("Is employee", default=False)
    is_client = models.BooleanField("Is Client", default=False)
    is_applicant = models.BooleanField("Is applicant", default=False)
    # is_employee = models.BooleanField("Is employee", default=False)
    is_employee_contract_signed = models.BooleanField(default=False)
    resume_file = models.FileField(upload_to="resumes/doc/", blank=True, null=True)

    # is_active = models.BooleanField('Is applicant', default=True)
    class Meta:
        # ordering = ["-date_joined"]
        ordering = ["username"]
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        fullname = f'{self.first_name},{self.last_name}'
        return fullname
    
    def is_recent(self):
        return self.date_joined >= timezone.now() - timedelta(days=365)


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
    # image2 = models.ForeignKey(
    #     Assets, related_name="profile_image", on_delete=models.CASCADE,default=1
    # )

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


class Department(models.Model):
    """Department Table will provide a list of the different departments in CODA"""
    # Department
    HR = "HR Department"
    IT = "IT Department"
    MKT = "Marketing Department"
    FIN = "Finance Department"
    SECURITY = "Security Department"
    MANAGEMENT = "Management Department"
    HEALTH = "Health Department"
    Other = "Other"
    DEPARTMENT_CHOICES = [
        (HR, "HR Department"),
        (IT, "IT Department"),
        (MKT, "Marketing Department"),
        (FIN, "Finance Department"),
        (SECURITY, "Security Department"),
        (MANAGEMENT, "Management Department"),
        (HEALTH, "Health Department"),
        (Other, "Other"),
    ]

    name = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default=Other,
    )

    description = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(
        verbose_name=_("Department safe URL"), max_length=255, unique=True
    )
    # created_date = models.DateTimeField(_('entered on'),default=timezone.now, editable=True)
    is_featured = models.BooleanField("Is featured", default=True)
    is_active = models.BooleanField(default=True)

    objects=DepartmentManager()

    @classmethod
    def get_default_pk(cls):
        cat, created = cls.objects.get_or_create(
            name="Other", defaults=dict(description="this is not an cat")
        )
        return cat.pk

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name
    

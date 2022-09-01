from django.db.models import Q
from decimal import *
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone

# User=settings.AUTH_USER_MODEL
User = get_user_model()

# ==================================INTERVIEWS====================================
class InterviewQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(featured=True, is_active=True)

    def search(self, query):
        lookups = (
            Q(category__icontains=query)
            | Q(question_type__icontains=query)
            | Q(last_name__icontains=query)
            | Q(first_name__icontains=query)
            | Q(upload_date__icontains=query)
            | Q(username__username__icontains=query)
        )
        return self.filter(lookups).distinct()


class InterviewManager(models.Manager):
    def get_queryset(self):
        # return super(TaskManager, self).get_queryset().filter(is_active=True)
        return InterviewQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    """ def featured(self):
        return self.get_queryset().featured() """

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


#Interview Model
class JobRole(models.Model):
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
    user= models.ForeignKey(
                            User,
                            verbose_name=_("Client"),
                            related_name="Client_Name",
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL,
                            #  limit_choices_to=Q(is_client=True)|Q(is_admin=True) | Q(is_superuser=True) and Q(is_active=True),
                            limit_choices_to={"is_client": True, "is_active": True},
                           )
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
    videolink=models.CharField(max_length=255,blank=True, null=True)
    doclink=models.CharField(max_length=255,blank=True, null=True)
    desc1=models.TextField(max_length=1000,blank=True, null=True)
    desc2=models.TextField(max_length=1000,blank=True, null=True)
    is_active=models.BooleanField(default=True)

    # objects=InterviewManager()

    class Meta:
        verbose_name_plural = 'Roles'  

    def uploaded_doc(self):
        if self.doc is None or self.doc == "None":
            return reverse("main:404error")
        else:
            return self.doc

    def __str__(self):
        return f'{self.category} upload'

    



# Interviews Model
class Interviews(models.Model):
    # Job Category.
    Project_Management = "Project Management"
    Business_Analysis = "Business Analyst"
    Quality_Assurance = "Quality Assurance"
    User_Experience = "User Interface"
    Reporting = "Reporting"
    ETL = "ETL"
    Database = "Database"
    Python = "Python"
    Other = "Other"
    # Question Type
    Introduction = "introduction"
    Project_Story = "Project Story"
    Performance = "performance"
    Methodology = "methodology"
    SDLC = "sdlc"
    Testing = "testing"
    Environment = "environment"
    Resume = "resume"

    CAT_CHOICES = [
        (Project_Management, "Project Management"),
        (Business_Analysis, "Business Analysis"),
        (Quality_Assurance, "Quality Assurance"),
        (User_Experience, "User Experience"),
        (Reporting, "Reporting"),
        (ETL, "ETL"),
        (Database, "Database"),
        (Python, "Python"),
        (Other, "Other"),
    ]

    QUESTION_CHOICES = [
        (Introduction, "introduction"),
        (Project_Story, "project story"),
        (Performance, "performance"),
        (Methodology, "methodology"),
        (SDLC, "sdlc"),
        (Testing, "testing"),
        (Environment, "environment"),
        (Resume, "resume"),
        (Other, "Other"),
    ]
    # id = models.AutoField(primary_key=True,default=9999999)
    # client= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="client_assiged", default=1
    )
    # first_name=models.CharField(max_length=100,null=True,blank=True)
    # midle=models.CharField(max_length=100,null=True,blank=True)

    # last_name=models.CharField(max_length=100,null=True,blank=True)
    upload_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default=Other,
    )
    question_type = models.CharField(
        max_length=25,
        choices=QUESTION_CHOICES,
        default=Other,
    )

    doc = models.FileField(default="None", upload_to="Uploads/doc/")
    link = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = InterviewManager()

    class Meta:
        verbose_name_plural = "InterviewUploaded"

    def __str__(self):
        return f"{self.client} upload"


"""
class DocUpload(models.Model):
    #id = models.AutoField(primary_key=True)
    doc_type=models.CharField(max_length=100,blank=True, null=True)
    doc_name=models.CharField(max_length=100,blank=True, null=True)
    doc=models.FileField(upload_to='Uploads/doc/')
    link=models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Uploads'

    def __str__(self):
        return f'{self.id} Uploads'
"""
# ==================================TRAINING====================================
class FeaturedCategory(models.Model):
    # Job Category.
    Course_Overview = "Course Overview"
    Planning = "Initiation & Planning"
    Development = "Development"
    Testing = "Testing"
    Deployment = "Deployment"
    Other = "Other"

    CAT_CHOICES = [
        (Course_Overview, "Course Overview"),
        (Planning, "Initiation & Planning"),
        (Development, "Development"),
        (Testing, "Testing"),
        (Deployment, "Deployment"),
        (Other, "Other"),
    ]

    title = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        unique=True,
        default=Other,
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # level=models.CharField(max_length=50,default='A')
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Categories"

    @classmethod
    def get_default_pk(cls):
        cat, created = cls.objects.get_or_create(
            title=" ", defaults=dict(description="this is not an cat")
        )
        return cat.pk

    def get_absolute_url(self):
        return reverse("bitraining")

    def __str__(self):
        return self.title


class FeaturedSubCategory(models.Model):
    featuredcategory = models.ForeignKey(
        to=FeaturedCategory,
        on_delete=models.CASCADE,
        default=FeaturedCategory.get_default_pk,
    )
    # category = models.ManyToManyField(Cat, blank=True,related_name='cats')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default="General")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    # doc=models.FileField(default="None",upload_to='training/docs/')
    # link=models.CharField(max_length=100,blank=True, null=True)
    # link_name=models.CharField(max_length=255, default='General')
    is_active = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Subcategories"

    def get_absolute_url(self):
        return reverse("bitraining")

    def __str__(self):
        return self.title


class FeaturedActivity(models.Model):
    # SubCategory = models.ForeignKey(to=SubCategory, on_delete=models.CASCADE,default=SubCategory.get_default_pk)
    featuredsubcategory = models.ManyToManyField(
        FeaturedSubCategory, blank=True, related_name="subcategories_fetured"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "activities"

    def get_absolute_url(self):
        return reverse("bitraining")

    def __str__(self):
        return self.activity_name


class ActivityLinks(models.Model):
    Activity = models.ManyToManyField(
        FeaturedActivity, blank=True, related_name="activity_featured"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    link_name = models.CharField(max_length=255, default="General")
    # description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doc = models.FileField(default="None", upload_to="training/docs/")
    link = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "links"

    def get_absolute_url(self):
        return reverse("bitraining")

    def __str__(self):
        return self.link_name


class UserLevel(models.Model):
    # Levels
    A = "Level A"
    B = "Level B"
    C = "Level C"
    D = "Level D"
    E = "Level E"
    O = "Other"

    LEVEL_CHOICES = [
        (A, "Level A"),
        (B, "Level B"),
        (C, "Level C"),
        (D, "Level D"),
        (E, "Level E"),
        (O, "Other"),
    ]

    level = models.CharField(
        max_length=25,
        choices=LEVEL_CHOICES,
        unique=True,
        default=A,
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # level=models.CharField(max_length=50,default='A')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "levels"

    def get_absolute_url(self):
        return reverse("bitraining")

    def __str__(self):
        return self.level


class DSU(models.Model):
    # Job Category.
    Interview = "Interview"
    BI_Training = "BI Training"
    Job_Support = "Job Support"
    Other = "Other"

    CAT_CHOICES = [
        (Interview, "Interview"),
        (BI_Training, "BI Training"),
        (Job_Support, "Job Support"),
        (Other, "Other"),
    ]
    # Client/Employee
    client = "client"
    Staff = "Staff"
    Other = "Other"

    TYPE_CHOICES = [
        (client, "client"),
        (Staff, "Staff"),
        (Other, "Other"),
    ]
    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default=Other,
    )
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default=Other,
    )
    # category = models.ManyToManyField(FeaturedActivity, blank=True,related_name='activity_featured')
    # category= models.ManyToManyField(User, on_delete=models.CASCADE)
    trained_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(is_employee=True)
        | Q(is_client=True)
        | Q(is_admin=True)
        | Q(is_superuser=True),
    )
    client_name = models.CharField(max_length=255, default="admin")
    task = models.TextField()
    plan = models.TextField()
    challenge = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)
    cohort = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "DSU"

    def get_absolute_url(self):
        return reverse("data:bitraining")

    def __str__(self):
        return self.category


class Job_Tracker(models.Model):
    # Job Status.
    screening_call = "screening call"
    first_interview = "1st interview"
    second_interview = "2nd interview"
    third_interview = "3rd interview"
    Other = "Other"
    STATUS_CHOICES = [
        (screening_call, "screening call"),
        (first_interview, "1st interview"),
        (second_interview, "2nd interview"),
        (third_interview, "3rd interview"),
        (Other, "Other"),
    ]
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=True, null=True)
    recruiter = models.CharField(max_length=100, blank=True, null=True)
    vendor_phone = models.CharField(max_length=100, blank=True, null=True)
    primary_tool = models.CharField(max_length=100, blank=True, null=True)
    secondary_tool = models.CharField(max_length=100, blank=True, null=True)
    job_location = models.CharField(max_length=100, blank=True, null=True)
    offer = models.DecimalField(
        max_digits=10,
        error_messages={
            "name": {" max_length": ("The earning must be between 0 and 4999.99")}
        },
        decimal_places=2,
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="other")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_resume = models.FileField(default="None", upload_to="training/docs/")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "jobs"

    def get_absolute_url(self):
        return reverse("jobtracker")

    def __str__(self):
        return self.position

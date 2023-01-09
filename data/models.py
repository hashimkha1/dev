from django.db.models import Q
from decimal import *
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from data.modelmanager import(
                                InterviewQuerySet,InterviewManager,
                                RoleQuerySet,RoleManager,
                                CategoryManager,SubCategoryManager,ActivityManager

                             )
# User=settings.AUTH_USER_MODEL
from accounts.models import CustomerUser

User = get_user_model()

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

    objects=RoleManager()

    class Meta:
        verbose_name_plural = 'Roles'  

    def uploaded_doc(self):
        if self.doc is None or self.doc == "None":
            return reverse("main:404error")
        else:
            return self.doc

    def get_url(self):
        return reverse("data:question-detail", args=[self.question_type])
    # def __str__(self):
    #     return f'{self.question_type}'


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
    comment = models.TextField()
    doc = models.FileField(default="None", upload_to="Uploads/doc/")
    link = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = InterviewManager()

    class Meta:
        verbose_name_plural = "InterviewUploaded"

    def __str__(self):
        return f"{self.client} upload"


class Training_Responses(models.Model):
    user = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="user_assigned", null=True, blank=True
    )
    question = models.CharField(max_length=200)
    question1 = models.TextField(default='Write Your Reponse')
    is_active = models.BooleanField(default=True)
    doc = models.FileField(default="None", upload_to="Uploads/doc/")
    link = models.CharField(max_length=500,null=True, blank=True)
    comment = models.TextField()
    score = models.PositiveIntegerField(null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Prep_Questions(models.Model):
    company=models.CharField(max_length=100,blank=True, null=True)
    category=models.CharField(max_length=255,blank=True, null=True)
    question=models.CharField(max_length=500,blank=True, null=True)
    date = models.DateTimeField(default=datetime.now,blank=True, null=True)
    response=models.TextField(max_length=1000,blank=True, null=True)
    is_answered=models.BooleanField(default=False,blank=True, null=True)
    is_active=models.BooleanField(default=False,blank=True, null=True)
    is_featured=models.BooleanField(default=False,blank=True, null=True)

    class Meta:
        verbose_name_plural = 'prep_questions'
    
    def __str__(self):
        return f'{self.id} prep_questions'

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

    objects=CategoryManager()

    class Meta:
        verbose_name_plural = "Categories"

    @classmethod
    def get_default_pk(cls):
        cat, created = cls.objects.get_or_create(
            title=" ", defaults=dict(description="this is not an cat")
        )
        return cat.pk

    # def get_absolute_url(self):
    #     return reverse("bitraining")

    def get_url(self):
        return reverse("data:category-detail", args=[self.title])

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

    objects=SubCategoryManager()

    class Meta:
        verbose_name_plural = "Subcategories"

    # def get_absolute_url(self):
        # return reverse('data:subcategory-detail', kwargs={'title': self.title})
    
    def subcat_url(self):
        return reverse("data:subcategory-detail", args=[self.title])

    def __str__(self):
        return self.title


class FeaturedActivity(models.Model):
    # SubCategory = models.ForeignKey(to=SubCategory, on_delete=models.CASCADE,default=SubCategory.get_default_pk)
    featuredsubcategory = models.ManyToManyField(
        FeaturedSubCategory, blank=True, related_name="subcategories_fetured"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=255)
    # slug = models.SlugField(max_length=255, blank=True, default="slug")
    description = models.TextField()
    guiding_question = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.IntegerField(default=1)

    objects=ActivityManager()

    class Meta:
        verbose_name_plural = "activities"
    
    def activity_url(self):
        return reverse("data:activity-detail", args=[self.slug])

    @property
    def question(self):
        if self.guiding_question != None:
            available_question=self.guiding_question
            return available_question

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

    def get_link_url(self):
        return self.link

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

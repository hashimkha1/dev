import calendar,string
import itertools
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from decimal import *
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from management.utils import unique_slug_generator,split_num_str
from django.contrib.auth import get_user_model
from accounts.models import TaskGroups,Department
from data.models import FeaturedCategory,FeaturedSubCategory,FeaturedActivity

# User=settings.AUTH_USER_MODEL
User = get_user_model()

# --------------------------------------


class Training(models.Model):
    class Level(models.IntegerChoices):
        Level_1 = 1
        Level_2 = 2
        Level_3 = 3
        Level_4 = 4
        Level_5 = 5
    presenter = models.ForeignKey(
        User,
        verbose_name=("presenter name"),
        on_delete=models.CASCADE,
        # limit_choices_to={"is_staff": True,"is_client": True, "is_active": True},
        limit_choices_to=Q(is_staff=True)|Q(is_client=True)|Q(is_admin=True) | Q(is_superuser=True) and Q(is_active=True),
        related_name="employee_name")
    department = models.ForeignKey(
        Department,
        verbose_name=("departments"),
        on_delete=models.CASCADE,
        related_name="department_name")
    category = models.ForeignKey(
        FeaturedCategory,
        verbose_name=("categories"),
        on_delete=models.CASCADE,
        related_name="category_name")
    subcategory = models.ForeignKey(
        FeaturedSubCategory,
        verbose_name=("Subcategory"),
        on_delete=models.CASCADE,
        related_name="subcategory_name")
    topic = models.ForeignKey(
        FeaturedActivity,
        verbose_name=("topic"),
        on_delete=models.CASCADE,
        related_name="title")
    level = models.IntegerField(choices=Level.choices)
    session=models.PositiveIntegerField()
    session_link = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(blank=True,null=True)
    description = models.TextField(default='No Comment',null=True, blank=True)
    is_active = models.BooleanField(default=True)
    featured= models.BooleanField(default=True)

# -------------------------------------COMPANY POLICIES---------------------------------------
class Policy(models.Model):
    # Department
    HR = "HR"
    IT = "IT"
    MKT = "Marketing"
    FIN = "Finance"
    SECURITY = "Security"
    MANAGEMENT = "Management"
    HEALTH = "Health"
    Other = "Other"
    DEPARTMENT_CHOICES = [
        (HR, "HR"),
        (IT, "IT"),
        (MKT, "Marketing"),
        (FIN, "Finance"),
        (SECURITY, "Security"),
        (MANAGEMENT, "Management"),
        (HEALTH, "Health"),
        (Other, "Other"),
    ]

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
    DAY_CHOICES = [
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]
    id = models.AutoField(primary_key=True)
    # staff = models.ForeignKey(
    #     User, on_delete=models.RESTRICT, related_name="staff_entry",
    #     limit_choices_to=Q(is_staff=True)|Q(is_admin=True) | Q(is_superuser=True),
    #     default=1
    # )
    staff = models.CharField(max_length=100, null=True, blank=True, default="admin")
    upload_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default=Other,
    )
    day = models.CharField(max_length=25, choices=DAY_CHOICES, default="Sunday")
    description = models.TextField()
    policy_doc = models.FileField(
        upload_to="policy/doc/", default=None, null=True, blank=True
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_internal = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"{self.id} policy"


# ==================================ACTIVITIES====================================
class TaskCategory(models.Model):
    # Tasks Category.
    Meetings = "Meetings"
    Data_Analyis = "Data Analysis"
    Stocks_Options = "Stocks & Options"
    Website = "Website Development"
    Department = "Department"
    Other = "Other"

    CAT_CHOICES = [
        (Meetings, "Meetings"),
        (Data_Analyis, "Data Analysis"),
        (Stocks_Options, "Stocks & Options"),
        (Website, "Website Development"),
        (Department, "Department"),
        (Other, "Other"),
    ]
    title = models.CharField(
        max_length=55,
        choices=CAT_CHOICES,
        unique=True,
        default=Other,
    )

    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # active=models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Task Categories"

    @classmethod
    def get_default_pk(cls):
        cat, created = cls.objects.get_or_create(
            title="Other", defaults=dict(description="this is not an cat")
        )
        return cat.pk


    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return self.title


class TaskQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(featured=True, is_active=True)

    def search(self, query):
        lookups = (
            Q(group__icontains=query)
            | Q(description__icontains=query)
            | Q(description__icontains=query)
            | Q(activity_name__icontains=query)
            | Q(mxearning__icontains=query)
            | Q(submission__icontains=query)
            | Q(employee__email__icontains=query)
        )
        return self.filter(lookups).distinct()


class TaskManager(models.Manager):
    def get_queryset(self):
        # return super(TaskManager, self).get_queryset().filter(is_active=True)
        return TaskQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset()

    """ def featured(self):
        return self.get_queryset().featured() """

    def get_by_pk(self, pk):
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_employee(self, employee):
        qs = self.get_queryset().filter(employee=employee)
        if qs.count() == 1:
            return qs.first()
        return None

    """
    def get_by_slug(self,slug):
        qs=self.get_queryset().filter(slug=slug)
        if qs.count()==1:
            return qs.first()
        return None 
    """

    def search(self, query):
        return self.get_queryset().active().search(query)


class Task(models.Model):
    group = models.CharField(
        verbose_name=_("group"),
        help_text=_("Required"),
        max_length=255,
        default="Group A",
    )
    groupname = models.ForeignKey(
        to=TaskGroups, on_delete=models.CASCADE, default=1
    )
    category = models.ForeignKey(
        to=TaskCategory, on_delete=models.CASCADE, default=TaskCategory.get_default_pk
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="assigned_user",
        limit_choices_to=Q(is_staff=True) & Q(is_active=True),
        # limit_choices_to=Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True)
        # and Q(is_active=True),
        default=999,
    )
    activity_name = models.CharField(
        verbose_name=_("Activity Name"),
        help_text=_("Required"),
        max_length=255,
    )

    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Not Required"),
        default="Add description on this activity",
    )
    # task_date=models.DateField(auto_now_add=Tru, default=)
    slug = models.SlugField(max_length=255, blank=True, default="slug")
    duration = models.PositiveIntegerField(
        # max_digits=3,
        help_text=_("Should be less than Maximum Points assigned"),
        error_messages={
            "name": {" max_length": ("Points must be less than Maximum Points")}
        },
        default=1,
    )
    point = models.DecimalField(
        max_digits=10,
        help_text=_("Should be less than Maximum Points assigned"),
        error_messages={
            "name": {" max_length": ("Points must be less than Maximum Points")}
        },
        decimal_places=2,
    )
    mxpoint = models.DecimalField(
        max_digits=10,
        help_text=_("Maximum 200"),
        error_messages={
            "name": {" max_length": ("The maximum points must be between 0 and 199")}
        },
        decimal_places=2,
    )

    mxearning = models.DecimalField(
        max_digits=10,
        help_text=_("Maximum 4999.99"),
        error_messages={
            "name": {" max_length": ("The earning must be between 0 and 4999.99")}
        },
        decimal_places=2,
    )
    submission = models.DateTimeField(
        help_text=_("Date formart :mm/dd/yyyy"), auto_now=True, editable=True, null=True
    )
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)

    objects = TaskManager()

    @classmethod
    def get_default_pk(cls):
        tak, created = cls.objects.get_or_create(
            title="Other", defaults=dict(description="this is not an task")
        )
        return tak.pk

    @property
    def submitted(self):
        submitted = datetime.date(self.submission)
        return submitted

    @property
    def deadline(self):
        today = datetime.today()
        deadline_date = datetime(
            today.year, today.month, calendar.monthrange(today.year, today.month)[-1]
        )
        deadline = datetime.date(deadline_date)
        return deadline

    @property
    def time_remaining(self):
        today = date.today()
        deadline_date = date(
            today.year, today.month, calendar.monthrange(today.year, today.month)[-1]
        )
        delta = deadline_date - today
        time_remaining = delta.days
        return time_remaining

    @property
    def late_penalty(self):
        if self.submitted > self.deadline:
            return 0.98
        else:
            return 1

    @property
    def task_url(self):
        one_list = ["one on one sessions","one on one","one on one session",]
        job_list =  ["job support","job_support"]
        onelist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in one_list] 
        joblist= [task.lower().translate({ord(c): None for c in string.whitespace}) for task in job_list] 
        activity=self.activity_name.lower().translate({ord(c): None for c in string.whitespace})
        # for i in onelist:
        #     if(i == activity):
        #         return reverse("application:rate")
        #     else:
        #         return reverse("management:new_evidence", args=[self.id])
        for i,j in itertools.zip_longest(onelist,joblist):
            if(i==activity):
                return reverse("application:rate")
            elif(j==activity):
                return reverse("accounts:tracker-list")
            else:
                return reverse("management:new_evidence", args=[self.id])

    @property
    def get_pay(self):
        if self.point > self.mxpoint:
            return 0
        else:
            try:
                Earning = round(Decimal(self.point / self.mxpoint) * self.mxearning, 2)
            except Exception as ZeroDivisionError:
                Earning = 0
            compute_pay = Earning * Decimal(self.late_penalty)
            pay = round(compute_pay, 2)
            return pay

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ("-submission",)

    def get_absolute_url(self):
        return reverse("management:activity-detail", args=[self.slug])

    def __str__(self):
        return self.activity_name

# Adding the evidence table/model
class TaskLinks(models.Model):
    # task = models.ManyToManyField(Task, blank=True,related_name='task_featured')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True),
    )
    link_name = models.CharField(max_length=255, default="General")
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doc = models.FileField(default="None", upload_to="evidence/docs/")
    link = models.CharField(max_length=1000, blank=True, null=True)
    linkpassword = models.CharField(max_length=255, default="No Password Needed")
    is_active = models.BooleanField("Is active", default=True)
    is_featured = models.BooleanField("Is featured", default=False)

    class Meta:
        verbose_name_plural = "Task Reference"

    def get_absolute_url(self):
        return reverse("tasks")

    @property
    def video_linkname(self):
        if self.link_name.startswith("Req"):
            new_link = self.link_name
            number_str=int(split_num_str(new_link))
            return number_str

    @property
    def lowerlinkname(self):
        if self.link_name.startswith("Req"):
            new_link = self.link_name.lower().replace(" ", "")
            return new_link


class TaskHistory(models.Model):
    group = models.CharField(
        verbose_name=_("group"),
        help_text=_("Required"),
        max_length=255,
        default="Group A",
    )
    category = models.ForeignKey(
        to=TaskCategory, on_delete=models.CASCADE, default=TaskCategory.get_default_pk
    )
    # category = models.ManyToManyField(TaskCategory, blank=True)
    employee = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="history_user_assiged",
        default=999,
    )
    activity_name = models.CharField(
        verbose_name=_("Activity Name"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Not Required"),
        default="Add description on this activity",
    )
    # task_date=models.DateField(auto_now_add=Tru, default=)
    slug = models.SlugField(max_length=255, blank=True, default="slug")
    duration = models.PositiveIntegerField(
        # max_digits=3,
        help_text=_("Should be less than Maximum Points assigned"),
        error_messages={
            "name": {" max_length": ("Points must be less than Maximum Points")}
        },
        default=1,
    )
    point = models.DecimalField(
        max_digits=10,
        help_text=_("Should be less than Maximum Points assigned"),
        error_messages={
            "name": {" max_length": ("Points must be less than Maximum Points")}
        },
        decimal_places=2,
    )
    mxpoint = models.DecimalField(
        max_digits=10,
        help_text=_("Maximum 200"),
        error_messages={
            "name": {" max_length": ("The maximum points must be between 0 and 199")}
        },
        decimal_places=2,
    )
    mxearning = models.DecimalField(
        max_digits=10,
        help_text=_("Maximum 4999.99"),
        error_messages={
            "name": {" max_length": ("The earning must be between 0 and 4999.99")}
        },
        decimal_places=2,
    )
    submission = models.DateTimeField(
        help_text=_("Date formart :mm/dd/yyyy"), auto_now=True, editable=True, null=True
    )
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        help_text=_("Date formart :mm/dd/yyyy"), auto_now=True, editable=True, null=True
    )
    objects = TaskManager()

    class Meta:
        verbose_name_plural = "TaskHistory"
        ordering = ["-submission"]

    @property
    def submitted(self):
        submitted = datetime.date(self.submission)
        submitted_date=submitted-relativedelta(days=1)
        return submitted_date

    @property
    def deadline(self):
        today = datetime.today()
        deadline_date = datetime(
            today.year, today.month, calendar.monthrange(today.year, today.month)[-1]
        )
        deadline = datetime.date(deadline_date)
        end_date=deadline-relativedelta(months=1)
        return end_date

    @property
    def time_remaining(self):
        today = date.today()
        deadline_date = date(
            today.year, today.month, calendar.monthrange(today.year, today.month)[-1]
        )
        delta = deadline_date - today
        time_remaining = delta.days
        return time_remaining

    @property
    def late_penalty(self):
        if self.submitted > self.deadline:
            return 0.98
        else:
            return 1

    @property
    def get_pay(self):
        if self.point > self.mxpoint:
            return 0
        else:
            try:
                Earning = round(Decimal(self.point / self.mxpoint) * self.mxearning, 2)
            except Exception as ZeroDivisionError:
                Earning = 0.0
            compute_pay = Decimal(Earning) * Decimal(self.late_penalty)
            pay = round(compute_pay, 2)
            return pay

class Requirement(models.Model):
    # Apps
    Reporting = "Reporting"
    Website = "Website"
    ETL = "ETL"
    Database = "Database"
    Other = "Other"
    # Beneficiary
    Management = "Management"
    Client = "Client"
    Other = "Other"

    # Priority Status
    Critical= "Critical"
    High= "High"
    Medium= "Medium"
    Low= "Low"

    CAT_CHOICES = [
        (Reporting, "Reporting"),
        (ETL, "ETL"),
        (Database, "Database"),
        (Website, "Website"),
        (Other, "Other"),
    ]
    BEN_CHOICES = [
        (Management, "Management"),
        (Client, "Client"),
        (Other, "Other"),
    ]
    STATUS_CHOICES = [
        (Critical, "Critical"),
        (High, "High"),
        (Medium, "Medium"),
        (Low, "Low"),
    ]
    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default=Other,
    )
    requestor = models.CharField(
        max_length=25,
        choices=BEN_CHOICES,
        default=Other,
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default=Low,
    )
    creator = models.ForeignKey(
        User,
        verbose_name=_("creator"),
        related_name="creator",
        null=True,
        blank=True,
        default=1,
        on_delete=models.SET_NULL,
        limit_choices_to=Q(is_active=True)
        and (Q(is_staff=True) |Q(is_client=True) | Q(is_admin=True) | Q(is_superuser=True)),
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        limit_choices_to=Q(is_active=True)
        and (Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True)),
    )
    company = models.CharField(max_length=255, default="CODA")
    created_by = models.CharField(max_length=255, default="admin")
    app = models.CharField(max_length=255, default="Data Analysis")
    duration = models.IntegerField(null=False, default=4)  # how long will it take
    delivery_date = models.DateTimeField(
        default=timezone.now
    )  # When should this be delivered
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    what = models.TextField()  # What is needed?
    why = models.TextField()  # Why do they need it ?
    how = (
        models.TextField()
    )  # how should it be delivered/Which platform or mode of delivery?
    comments = models.TextField(default='No Comment',null=True, blank=True)  # What is needed?
    doc = models.FileField(upload_to="Uploads/Support_Docs/", null=True, blank=True)
    pptlink = models.CharField(max_length=1000,null=True, blank=True)
    videolink = models.CharField(max_length=1000,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_tested = models.BooleanField(default=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Requirements"
        # ordering = ["-created_at","-updated_at"]

    @property
    def doc_url(self):
        if self.doc and hasattr(self.doc, 'url'):
            return self.doc.url
        
    @property
    def active(self):
        if self.is_active is False:
            return "Ready For Testing"
        else:
            return "Not Started"

    def get_absolute_url(self):
        return reverse("management:requirements")

    def __str__(self):
        return self.category

class ProcessJustification(models.Model):
    requirements = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name="Requirement_in_Process",
                                     null=True, blank=True)
    justification = models.CharField(max_length=255, null=True, blank=True)
    crated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


class ProcessBreakdown(models.Model):
    process = models.ForeignKey(ProcessJustification, on_delete=models.CASCADE, related_name="Process_in_breakdown",
                                null=True, blank=True)
    breakdown = models.CharField(max_length=255, null=True, blank=True)
    time = models.PositiveIntegerField(null=True, blank=True)
    Quantity = models.PositiveIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    crated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)




def task_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(task_pre_save_receiver, sender=Task)

class Advertisement(models.Model):
    # Twitter   
    twitter_api_key = models.CharField(max_length=500, null=True, blank=True)
    twitter_api_key_secret = models.CharField(max_length=500, null=True, blank=True)
    twitter_bearer_token = models.CharField(max_length=500, null=True, blank=True)
    twitter_access_token = models.CharField(max_length=500, null=True, blank=True)
    twitter_access_token_secret = models.CharField(
        max_length=500, null=True, blank=True
    )
    # Facebook
    facebook_access_token = models.CharField(max_length=500, null=True, blank=True)
    facebook_page_id = models.CharField(max_length=100, null=True, blank=True)
    page_name = models.CharField(max_length=100, null=True, blank=True)
    post_description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="Uploads/Facebook/", null=True, blank=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # whatsapp
    whatapp_group_name = models.CharField(max_length=100, null=True, blank=True)
    whatapp_group_id = models.CharField(max_length=100, null=True, blank=True)
    whatapp_image_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_description
    
# class Whatsapp(models.Model):
#     # whatsapp
#     product_id = models.CharField(max_length=100, null=True, blank=True)
#     token = models.CharField(max_length=100, null=True, blank=True)
#     screen_id = models.CharField(max_length=500, null=True, blank=True)
#     group_name = models.CharField(max_length=100, null=True, blank=True)
#     group_id = models.CharField(max_length=100, null=True, blank=True)
#     image_url = models.CharField(max_length=500, null=True, blank=True)
#     link = models.CharField(max_length=500, null=True, blank=True)
#     message= models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.group_name
    
class Meetings(models.Model):
    Group = [
        ("clients", "clients"),
        ("internal", "internal"),
        ("external", "external"),
        ("Other", "Other"),
    ]
    class Frequecy(models.IntegerChoices):
        Daily = 1,
        Weekly = 2
        Bi_Weekly = 3
        Monthly = 4
        Yearly = 5
    department=models.ForeignKey(
        to=Department, on_delete=models.CASCADE, default=Department.get_default_pk)
    category = models.ForeignKey(
        to=TaskCategory, on_delete=models.CASCADE
    )
    group = models.CharField(
        max_length=255,
        choices=Group,
        default='Other'
    )
    meeting_topic = models.CharField(max_length=100, null=True, blank=True)
    meeting_id = models.CharField(max_length=100, null=True, blank=True)
    meeting_type = models.CharField(max_length=100, null=True, blank=True)
    meeting_link = models.CharField(max_length=500, null=True, blank=True)
    meeting_description = models.TextField(null=True, blank=True)
    meeting_time = models.TimeField(default=timezone.now)
    frequency = models.IntegerField(choices=Frequecy.choices, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return self.meeting_topic
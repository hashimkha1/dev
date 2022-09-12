import calendar,string
import itertools
from datetime import datetime, date
from decimal import *
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from management.utils import unique_slug_generator
from django.contrib.auth import get_user_model
from accounts.models import TaskGroups

# User=settings.AUTH_USER_MODEL
User = get_user_model()
# --------------------------------------
class Transaction(models.Model):
    # Method of Payment
    Cash = "Cash"
    Mpesa = "Mpesa"
    Check = "Check"
    Other = "Other"

    #  Cost Category.
    Salary = "Salary"
    Health = "Health"
    Transport = "Transport"
    Food_Accomodation = "Food & Accomodation"
    Internet_Airtime = "Internet & Airtime"
    Recruitment = "Recruitment"
    Labour = "Labour"
    Management = "Management"
    Electricity = "Electricity"
    Construction = "Construction"
    Other = "Other"

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
    CAT_CHOICES = [
        (Salary, "Salary"),
        (Health, "Health"),
        (Transport, "Transport"),
        (Food_Accomodation, "Food & Accomodation"),
        (Internet_Airtime, "Internet & Airtime"),
        (Recruitment, "Recruitment"),
        (Labour, "Labour"),
        (Management, "Management"),
        (Electricity, "Electricity"),
        (Construction, "Construction"),
        (Other, "Other"),
    ]
    PAY_CHOICES = [
        (Cash, "Cash"),
        (Mpesa, "Mpesa"),
        (Check, "Check"),
        (Other, "Other"),
    ]
    # id = models.AutoField(primary_key=True,default=99999999)
    sender = models.CharField(max_length=100, null=True, default=None)
    receiver = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    department = models.CharField(max_length=100, default=None)
    type = models.CharField(max_length=100, default=None, null=True)
    activity_date = models.DateTimeField(default=timezone.now)
    receipt_link = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    transaction_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0
    )
    description = models.TextField(max_length=1000, default=None)

    payment_method = models.CharField(
        max_length=25,
        choices=PAY_CHOICES,
        default=Other,
    )

    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default=Other,
    )

    category = models.CharField(
        max_length=100,
        choices=CAT_CHOICES,
        default=Other,
    )

    def get_absolute_url(self):
        return reverse("management:transaction-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.id} Transactions"


# -------------------------------------CASH FLOW MODEL---------------------------------------
class Outflow(models.Model):
    # Method of Payment
    Cash = "Cash"
    Mpesa = "Mpesa"
    Check = "Check"
    Other = "Other"

    #  Cost Category.
    Salary = "Salary"
    Health = "Health"
    Transport = "Transport"
    Food_Accomodation = "Food & Accomodation"
    Internet_Airtime = "Internet & Airtime"
    Recruitment = "Recruitment"
    Labour = "Labour"
    Management = "Management"
    Electricity = "Electricity"
    Construction = "Construction"
    Other = "Other"

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
    CAT_CHOICES = [
        (Salary, "Salary"),
        (Health, "Health"),
        (Transport, "Transport"),
        (Food_Accomodation, "Food & Accomodation"),
        (Internet_Airtime, "Internet & Airtime"),
        (Recruitment, "Recruitment"),
        (Labour, "Labour"),
        (Management, "Management"),
        (Electricity, "Electricity"),
        (Construction, "Construction"),
        (Other, "Other"),
    ]
    PAY_CHOICES = [
        (Cash, "Cash"),
        (Mpesa, "Mpesa"),
        (Check, "Check"),
        (Other, "Other"),
    ]
    employee = models.ForeignKey("accounts.CustomerUser", on_delete=models.CASCADE)
    sender = models.CharField(max_length=100, null=True, default=None)
    receiver = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    department = models.CharField(max_length=100, default=None)
    type = models.CharField(max_length=100, default=None, null=True)
    activity_date = models.DateTimeField(default=timezone.now)
    # receipt_link=models.CharField(max_length=100,blank=True, null=True)
    # upload_receipt=models.FileField(default=None,upload_to='Receipt/doc/')
    qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    transaction_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0
    )
    description = models.TextField(max_length=1000, default=None)

    payment_method = models.CharField(
        max_length=25,
        choices=PAY_CHOICES,
        default=Other,
    )

    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default=Other,
    )

    category = models.CharField(
        max_length=100,
        choices=CAT_CHOICES,
        default=Other,
    )

    def get_absolute_url(self):
        return reverse("management:outflow_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.id} Transactions"


# -------------------------------------CASH FLOW MODEL---------------------------------------


class Inflow(models.Model):
    # Period of Payment
    Weekly = "Weekly"
    Bi_Weekly = "Bi_Weekly"
    Monthly = "Monthly"
    Yearly = "Yearly"

    # Method of Payment
    Cash = "Cash"
    Mpesa = "Mpesa"
    Check = "Check"
    Cashapp = "Cashapp"
    Zelle = "Zelle"
    Venmo = "Venmo"
    Paypal = "Paypal"

    # Category.
    Job_Support = "Job_Support"
    Interview = "Interview"
    Training = "Training"
    Stocks = "Stocks"
    Blockchain = "Blockchain"
    Mentorship = "Mentorship"
    Other = "Other"
    # Task/Activities
    Reporting = "reporting"
    Database = "database"
    Business_Analysis = "Business Analysis"
    ETL = "Data Cleaning"
    Options = "Options"
    Other = "Any Other"

    PERIOD_CHOICES = [
        (Weekly, "Weekly"),
        (Bi_Weekly, "Bi_Weekly"),
        (Monthly, "Monthly"),
        (Yearly, "Yearly"),
    ]

    CAT_CHOICES = [
        (Job_Support, "Job_Support"),
        (Interview, "Interview"),
        (Training, "Training"),
        (Stocks, "Stocks"),
        (Blockchain, "Blockchain"),
        (Mentorship, "Mentorship"),
        (Other, "Other"),
    ]
    TASK_CHOICES = [
        (Reporting, "reporting"),
        (Database, "database"),
        (Business_Analysis, "Business Analysis"),
        (ETL, "Data Cleaning"),
        (Options, "Options"),
        (Other, "Other"),
    ]

    PAY_CHOICES = [
        (Cash, "Cash"),
        (Mpesa, "Mpesa"),
        (Check, "Check"),
        (Cashapp, "Cashapp"),
        (Zelle, "Zelle"),
        (Venmo, "Venmo"),
        (Paypal, "Paypal"),
        (Other, "Other"),
    ]

    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
    )
    task = models.CharField(
        max_length=25,
        choices=TASK_CHOICES,
    )
    method = models.CharField(
        max_length=25,
        choices=PAY_CHOICES,
        default=Other,
    )

    period = models.CharField(
        max_length=25,
        choices=PERIOD_CHOICES,
        default=Other,
    )

    sender = models.ForeignKey("accounts.CustomerUser", on_delete=models.CASCADE)
    receiver = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    transaction_date = models.DateTimeField(default=timezone.now)
    receipt_link = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None
    )
    transaction_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=0
    )
    description = models.TextField(max_length=1000, default=None)

    class Meta:
        ordering = ["transaction_date"]

    def get_absolute_url(self):
        return reverse("management:inflow-detail", kwargs={"pk": self.pk})

    @property
    def end(self):
        # date_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        date_time = self.login_date + datetime.timedelta(hours=0)
        endtime = date_time.strftime("%H:%M")
        return endtime

    @property
    def total_payment(self):
        total = self.amount.objects.aggregate(TOTAL=Sum("amount"))["TOTAL"]
        return total


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
    #     limit_choices_to=Q(is_employee=True)|Q(is_admin=True) | Q(is_superuser=True),
    #     default=1
    # )
    staff = models.CharField(max_length=100, null=True, blank=True, default="admin")
    # last_name = models.CharField(max_length=100, null=True, blank=True)
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

    def __str__(self):
        return f"{self.id} policy"


# ==================================ACTIVITIES====================================
class Tag(models.Model):
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
    # title=models.CharField(max_length=255)
    # slug=models.CharField(max_length=255)
    # thumbnail=models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # active=models.IntegerField(default=1)

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
        to=Tag, on_delete=models.CASCADE, default=Tag.get_default_pk
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="user_assiged",
        limit_choices_to=Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True)
        and Q(is_active=True),
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
        limit_choices_to=Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True),
    )
    link_name = models.CharField(max_length=255, default="General")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doc = models.FileField(default="None", upload_to="evidence/docs/")
    link = models.CharField(max_length=1000, blank=True, null=True)
    linkpassword = models.CharField(max_length=255, default="No Password Needed")
    is_active = models.BooleanField("Is active", default=True)
    is_featured = models.BooleanField("Is featured", default=False)

    class Meta:
        verbose_name_plural = "links"

    def get_absolute_url(self):
        return reverse("tasks")

    def __str__(self):
        return self.link_name


class TaskHistory(models.Model):
    group = models.CharField(
        verbose_name=_("group"),
        help_text=_("Required"),
        max_length=255,
        default="Group A",
    )
    category = models.ForeignKey(
        to=Tag, on_delete=models.CASCADE, default=Tag.get_default_pk
    )
    # category = models.ManyToManyField(Tag, blank=True)
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
    def get_pay(self):
        if self.point > self.mxpoint:
            return 0
        else:
            try:
                Earning = round(Decimal(self.point / self.mxpoint) * self.mxearning, 2)
            except Exception as ZeroDivisionError:
                Earning = 0.0
            compute_pay = Earning * Decimal(self.late_penalty)
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
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        # limit_choices_to={"is_active": True,"is_employee": True,"is_admin": True,"is_superuser": True},
        limit_choices_to=Q(is_active=True)
        and (Q(is_employee=True) | Q(is_admin=True) | Q(is_superuser=True)),
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
    doc = models.FileField(upload_to="Uploads/Support_Docs/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def doc_url(self):
        if self.doc and hasattr(self.doc, 'url'):
            return self.doc.url

    class Meta:
        verbose_name_plural = "Requirements"

    def get_absolute_url(self):
        return reverse("management:requirements")

    def __str__(self):
        return self.category


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

class LBandLS(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    laptop_bonus =  models.FloatField(null=True)
    laptop_service = models.FloatField(null=True)

    def __str__(self):
        return self.user.username


class PayslipConfig(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # configs for loan
    loan_status = models.BooleanField(default=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=20000.00)
    loan_repayment_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.20)

    # configs for laptop service
    laptop_status = models.BooleanField(default=True)
    lb_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    ls_amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    ls_max_limit = models.DecimalField(max_digits=10, decimal_places=2, default=20000.00)

    # configs for retirement package
    rp_starting_period = models.CharField(max_length=10)
    rp_starting_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)
    rp_increment_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.01)
    rp_increment_max_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.05)
    rp_increment_percentage_increment = models.DecimalField(max_digits=5, decimal_places=2, default=0.01)
    rp_increment_percentage_increment_cycle = models.IntegerField(default=12)

    # configs for bonus
    holiday_pay = models.DecimalField(max_digits=10, decimal_places=2, default=3000.00)
    night_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.02)

    # configs for deductions
    computer_maintenance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    food_accommodation = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    health = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    kra_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.30)

    # employee of the month, quarter and year
    eom_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.02)
    eoq_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.02)
    eoy_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.02)


class RetirementPackage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Loan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class LaptopBonus(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class LaptopSaving(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class MonthlyPoints(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    points = models.DecimalField(max_digits=10, decimal_places=2)


class QuarterlyPoints(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    points = models.DecimalField(max_digits=10, decimal_places=2)


class YearlyPoints(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period = models.CharField(max_length=10)
    points = models.DecimalField(max_digits=10, decimal_places=2)


class Payslip(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # month and year of period we are paying
    period = models.CharField(max_length=10)

    # points based on the work the employee done
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # earnings calculated based on points
    earned_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # benefits
    EOM = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    EOQ = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    EOY = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    laptop_bonus = models.OneToOneField(LaptopBonus, on_delete=models.CASCADE)
    holiday_wages = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    night_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # retirement_package is long term benefit and does not affect the net pay
    retirement_package = models.OneToOneField(RetirementPackage, on_delete=models.CASCADE)

    # deductions
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    FA = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    computer_maintenance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    health_care = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    laptop_saving = models.OneToOneField(LaptopSaving, on_delete=models.CASCADE)

    @property
    def get_monthly_benefits(self):
        return (
            'EOM',
            'EOQ',
            'EOY',
            'laptop_bonus',
            'holiday_wages',
            'night_allowance'
        )

    @property
    def get_monthly_deductions(self):
        return (
            'training_loan',
            'FA',
            'computer_maintenance',
            'health_care',
            'laptop_service'
        )

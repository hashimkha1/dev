from datetime import datetime,timedelta
from decimal import *
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from accounts.modelmanager import DepartmentManager
#from management.utils import unique_slug_generator
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
#User = get_user_model()

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


  
class departments(models.Model):
    """Department Table will provide a list of the different departments in CODA"""

    # Department
    BASIC = "Basic"
    HR = "HR Department"
    IT = "IT Department"
    MKT = "Marketing Department"
    FIN = "Finance Department"
    SECURITY = "Security Department"
    MANAGEMENT = "Management Department"
    Project = "Project"
    HEALTH = "Health Department"
    Other = "Other"
    DEPARTMENT_CHOICES = [
        (BASIC, "BASIC Department"),
        (HR, "HR Department"),
        (IT, "IT Department"),
        (MKT, "Marketing Department"),
        (FIN, "Finance Department"),
        (Project, "Project"),
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

    # def get_absolute_url(self):
    #     return reverse('management:department_list', args=[self.slug])
    def __str__(self):
        return self.name


class Transaction(models.Model):
    # Method of Category
    CAT_CHOICES = [
        ("Salary", "Salary"),
        ("Health", "Health"),
        ("Transport", "Transport"),
        ("Food_Accomodation", "Food & Accomodation"),
        ("Internet_Airtime", "Internet & Airtime"),
        ("Recruitment", "Recruitment"),
        ("Labour", "Labour"),
        ("Management", "Management"),
        ("Electricity", "Electricity"),
        ("Construction", "Construction"),
        ("Other", "Other"),
    ]
    # Method of Payment
    PAY_CHOICES = [
        ("Cash", "Cash"),
        ("Mpesa", "Mpesa"),
        ("Check", "Check"),
        ("Other", "Other"),
    ]
    sender = models.ForeignKey(
         CustomerUser,
         verbose_name=_("sender"),
         related_name="sender", 
         null=True, blank=True,
         on_delete=models.SET_NULL,
         limit_choices_to={"is_staff": True, "is_active": True},
         )
    department = models.ForeignKey(
        to=departments, on_delete=models.CASCADE, default=None
        )
    # sender = models.CharField(max_length=100, null=True, default=None)
    receiver = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    # department = models.CharField(max_length=100, default=None)
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
        default="Other",
    )

    category = models.CharField(
        max_length=100,
        choices=CAT_CHOICES,
        default="Other",
    )

    @property
    def total_transactions_amt(self):
        total_transactions_amt = self.amount * self.qty
        return total_transactions_amt
    
    # def get_absolute_url(self):
    #     return reverse("management:transaction-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Transactions"
        ordering = ["-activity_date"]

    def __str__(self):
        return f"{self.id} Transactions"        
  


class Payment_Information(models.Model):
    # id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(
        "accounts.CustomerUser",
        verbose_name=("Client Name"),
        on_delete=models.CASCADE,
        related_name="customer")
    payment_fees=models.IntegerField()
    down_payment=models.IntegerField(default=500)
    student_bonus=models.IntegerField(null=True,blank=True)
    fee_balance=models.IntegerField(default=None)
    plan = models.IntegerField() # assuming service_category id
    subplan = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=100)
    contract_submitted_date = models.DateTimeField(default=timezone.now)
    client_signature = models.CharField(max_length=1000)
    company_rep = models.CharField(max_length=1000)
    client_date = models.CharField(max_length=100, null=True, blank=True)
    rep_date = models.CharField(max_length=100, null=True, blank=True)

    @property
    def student_balance(self):
        try:
            stu_bal = self.payment_fees - (int(self.down_payment) + int(self.student_bonus))
            return stu_bal
        except:
            return redirect('finance:pay')
    @property
    def jobsupport_balance(self):
        try:
            support_bal = self.payment_fees - int(self.down_payment) 
            return support_bal
        except:
            return redirect('finance:pay')



class Payment_History(models.Model):
    # id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomerUser,
        verbose_name=("Client Name"),
        on_delete=models.CASCADE,
        related_name="customer_payment_history")
    payment_fees=models.IntegerField()
    down_payment=models.IntegerField(default=500)
    student_bonus=models.IntegerField(null=True,blank=True)
    fee_balance=models.IntegerField(default=None)
    down_payment = models.IntegerField(default=500)
    student_bonus = models.IntegerField(null=True, blank=True)
    fee_balance = models.IntegerField(default=None)
    plan = models.IntegerField()
    subplan = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=100)
    contract_submitted_date = models.DateTimeField(default=timezone.now)
    client_signature = models.CharField(max_length=1000)
    company_rep = models.CharField(max_length=1000)
    client_date = models.CharField(max_length=100, null=True, blank=True)
    rep_date = models.CharField(max_length=100, null=True, blank=True)  

   
class OverBoughtSold(models.Model):
    symbol = models.CharField(max_length=255,blank=True, null=True)
    description = models.CharField(max_length=255,blank=True, null=True)
    last = models.CharField(max_length=255,blank=True, null=True)
    volume = models.CharField(max_length=255,blank=True, null=True)
    RSI = models.CharField(max_length=255,blank=True, null=True)
    EPS = models.CharField(max_length=255,blank=True, null=True)
    PE = models.CharField(max_length=255,blank=True, null=True)
    rank = models.CharField(max_length=255,blank=True, null=True)
    profit_margins = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    @property
    def condition_integer(self):
        try:
            # Convert to float, round, and then convert to int
            rsi_value = int(round(float(self.RSI)))  
            if rsi_value >= 30:
                return 1  # 'oversold'
            else:
                return 0  # 'overbought'
        except ValueError:
            # Handle any exceptions gracefully
            return -1  #neutral

    
    class Meta:
        verbose_name_plural = "Oversold"

    def __str__(self):
        return self.symbol



class Ticker_Data(models.Model):
    symbol = models.CharField(max_length=255,blank=True, null=True)
    overallrisk =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    sharesshort =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    enterprisetoebitda =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    ebitda =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    quickratio =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    currentratio =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    revenuegrowth =models.DecimalField(max_digits=17, decimal_places=3,blank=True,null=True)
    fetched_date =models.DateField(auto_now_add=True,blank=True,null=True)
    industry = models.CharField(max_length=500,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Option Measures"

    def __str__(self):
        return self.symbol

from django.db import models

class PaymentsInformations(models.Model):
    customer_id = models.IntegerField()
    payment_fees = models.IntegerField()
    down_payment = models.IntegerField(default=500)
    student_bonus = models.IntegerField(null=True)
    fee_balance = models.IntegerField()
    plan = models.IntegerField()
    subplan = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    contract_submitted_date = models.DateField()
    client_signature = models.CharField(max_length=1000)
    company_rep = models.CharField(max_length=1000)
    client_date = models.CharField(max_length=100, null=True)
    rep_date = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"PaymentsInformations for Customer ID: {self.customer_id}"        
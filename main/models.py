from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils.text import slugify
from django.db.models.signals import pre_save
from .utils import unique_slug_generator,slug_pre_save_receiver
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

# from tableauhyperapi import DatabaseName

User = get_user_model()
# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Service(models.Model):
    serial = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(default='training',max_length=254)
    slug = models.SlugField(default='slug',max_length=255)
    description = models.TextField(null=True, blank=True)
    sub_titles = models.TextField(null=True, blank=True)
    # executive_summary = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)

class ServiceCategory(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=Service.objects.get_or_create(serial=1)[0].id)
    name = models.CharField(max_length=254)
    slug = models.SlugField(null=True, blank=True,unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Pricing(models.Model):
    class Contract(models.IntegerChoices):
        One_month = 1
        Two_months = 2
        Three_months = 3
        open = 12
    serial = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,default=1)
    # subcategory = models.CharField(default='Full Course', max_length=200, null=True, blank=True)
    price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    duration =  models.PositiveIntegerField(null=True, blank=True)
    contract_length = models.IntegerField(choices=Contract.choices, default=3)
    is_direct = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    redirect_url_path = models.CharField(max_length=1024, null=True)

    class Meta:
        verbose_name_plural = "Pricing"

    def __str__(self):
        return self.title


class PricingSubPlan(TimeStampedModel):
    my_pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    
    class Meta:
        verbose_name_plural = "PricingSubPlan"

    def __str__(self):
        return self.title + '-' + self.my_pricing.title
# class Pricing(models.Model):
#     class Contract(models.IntegerChoices):
#         One_month = 1
#         Two_months = 2
#         Three_months = 3
#         open = 12
#     serial = models.PositiveIntegerField(null=True, blank=True)
#     title = models.CharField(max_length=254)
#     description = models.TextField(null=True, blank=True)
#     category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE,default=1)
#     # subcategory = models.CharField(default='Full Course', max_length=200, null=True, blank=True)
#     premium_price = models.FloatField(null=True, blank=True)
#     silver_oprice = models.FloatField(null=True, blank=True)
#     price = models.FloatField()
#     discounted_price = models.FloatField(null=True, blank=True)
#     duration =  models.PositiveIntegerField(null=True, blank=True)
#     contract_length = models.IntegerField(choices=Contract.choices, default=3)
#     is_direct = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = "Pricing"

#     def __str__(self):
#         return self.title


class Testimonials(models.Model):
    # asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    writer = models.ForeignKey(
        User,
        verbose_name=("writer name"),
        on_delete=models.CASCADE,
        # limit_choices_to=Q(is_staff=True) |Q(is_client=True) and Q(is_active=True)| Q(is_admin=True) | Q(is_superuser=True),
        limit_choices_to=(Q(is_staff=True) |Q(is_client=True)),
        )
    class Meta:
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:post-detail', kwargs={'pk': self.pk})
    

class Assets(TimeStampedModel):
    name = models.CharField(max_length=200)
    category = models.CharField(default='background',max_length=200,null=True, blank=True)
    image_string = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True,default='background')
    service_image =models.ImageField(null=True, blank=True, upload_to="images/",default='background')

    image_url = models.CharField(max_length=1000, null=True, blank=True,default='background')

    class Meta:
        verbose_name_plural = "Assets"

    @property
    def split_name(self):
        image_1=self.name.split("_")[0]
        image_2=self.name.split("_")[1]
        image_name=image_1,image_2

        return image_name

    def __str__(self):
        return self.name
    
class Plan(models.Model):
    CAT_CHOICES = [
        ("Financial", "Financial"),
        ("Health", "Health"),
        ("Family", "Family"),
        ("Work", "Work"),
        ("Meetings", "Meetings"),
        ("Other", "Other"),
    ]
    GOAL_CHOICES = [
        ("Business", "Business"),
        ("Employment", "Employment"),
        ("Savings", "Savings"),
        ("Insurance", "Insurance"),
        ("Relationship", "Relationship"),
        ("Trips", "Trips"),
        ("Other", "Other"),
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
    STATUS_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default="Other",
    )
    goal = models.CharField(
        max_length=25,
        choices=GOAL_CHOICES,
        default="Other",
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="Low",
    )
    day = models.CharField(
        max_length=25,
        choices=DAY_CHOICES,
        default="Sunday",
    )
    planner = models.ForeignKey(
        User,
        related_name="planner",
        null=True,
        blank=True,
        default=1,
        on_delete=models.SET_NULL,
        limit_choices_to=Q(is_active=True)
        and (Q(is_admin=True) | Q(is_superuser=True)),
    )
    responsible_party = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        limit_choices_to=Q(is_active=True)
        and (Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True)),
    )
    task = models.CharField(max_length=255, default="CODA")
    duration = models.IntegerField(null=False, default=4)  # how long will it take
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    what = models.TextField()  # What is needed?
    why = models.TextField()  # Why do they need it ?
    how = (
        models.TextField()
    )  # how should it be delivered/Which platform or mode of delivery?
    comments = models.TextField(default='No Comment',null=True, blank=True)  # What is needed?
    doc = models.FileField(upload_to="Uploads/Support_Docs/", null=True, blank=True)
    pptlink = models.CharField(max_length=300, default="link",null=True, blank=True)
    videolink = models.CharField(max_length=300, default="Video",null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Plan"
        # ordering = ["-created_at","-updated_at"]

    @property
    def doc_url(self):
        if self.doc and hasattr(self.doc, 'url'):
            return self.doc.url
    @property
    def delivery(self):
        delivery=self.duration + self.created_at
        return delivery

    def get_absolute_url(self):
        return reverse("main:plans")

    def __str__(self):
        return self.goal


class ClientAvailability(models.Model):
    DAY = [
        ("0", "Monday"),
        ("1", "Tuesday"),
        ("2", "Wednesday"),
        ("3", "Thursday"),
        ("4", "Friday"),
        ("5", "Saturday"),
        ("6", "Sunday"),
    ]

    TIME = [
        ("PST", "PST"),
        ("CST", "CST"),
        ("EST", "EST"),
        ("EAT", "EAT"),
    ]

    client = models.ForeignKey(User, related_name="Clint", on_delete=models.CASCADE)
    day = models.CharField(max_length=100, choices=DAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    time_standards = models.CharField(max_length=100, choices=TIME)
    topic = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return str(self.client)
    

class Search(models.Model):
    CAT_CHOICES = [
        ("accounts", "Registration"),
        ("application", "Application"),
        ("finance", "Financial Information"),
        ("management", "Employees Activities"),
        ("data", "Data Analysis"),
        ("getdata", "Automation"),
        ("investing", "Investments"),
        ("main", "General Information"),
        ("projectmanagement", "Field Projects"),
    ]

    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default="Other",
    )

    # subcategories = models.ForeignKey(
    #     ServiceCategory,
    #     on_delete=models.CASCADE,
	# 	default=1
    # )
    searched_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(is_staff=True)
        | Q(is_client=True)
        | Q(is_admin=True)
        | Q(is_superuser=True),
    )
    # subcategory = models.CharField(max_length=255, default="training")
    topic = models.CharField(max_length=255, default="Task")
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Search"

    def get_absolute_url(self):
        return reverse("main:layout")

    def __str__(self):
        return self.question

# models.py
from django.db import models

class Location(models.Model):
    zipcode = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Location")

    def __str__(self):
        return self.state

class Company(TimeStampedModel):
    """Company Table will provide a list of the different company affiliated with CODA"""
    name = models.CharField(max_length=100,null=True, blank=True)
    sector = models.CharField(max_length=100,null=True, blank=True)
    company_address = models.CharField(max_length=100,null=True, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        # default=1,
        null=True, 
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # default=1,
        null=True, 
        blank=True
    )
    sector = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name


class WCAGStandardWebsite(models.Model):
    CAT_CHOICES = [
            ("accounts", "accounts"),
            ("application", "application"),
            ("finance", "finance"),
            ("management", "management"),
            ("data", "data"),
            ("getdata", "getdata"),
            ("investing", "investing"),
            ("main", "main"),
            ("projectmanagement", "projectmanagement"),
    ]
    company  = models.CharField(max_length=500,blank=True,null=True)#coda,safaricom,Google,
    app_name = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default="main",
    )
    page_name    = models.CharField(max_length=500,blank=True,null=True)
    website_url  = models.CharField(max_length=500,blank=True,null=True)
    improvements = models.TextField(blank=True,null=True) 
    # page_file   = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.app_name
        



class WCAGStandard(TimeStampedModel):
    # my_wcag_website = models.ForeignKey(WCAGStandardWebsite, on_delete=models.CASCADE, null=True)
    criteria = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    what_to_test = models.CharField(max_length=255)
    how_to_test = models.TextField()
    user_affected = models.TextField()

    def __str__(self):
        return self.criteria
    
# ==============================PRESAVE SLUG GENERATORS====================================
def testimonials_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator


def servicecategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        if instance.name:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(servicecategory_pre_save_receiver, sender=ServiceCategory)

pre_save.connect(testimonials_pre_save_receiver,sender=Testimonials)

pre_save.connect(slug_pre_save_receiver,sender=Company)

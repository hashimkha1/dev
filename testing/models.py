from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
#User=settings.AUTH_USER_MODEL
User = get_user_model()

class Categories(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    url_slug=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    is_active=models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return self.title
    
class SubCategories(models.Model):
    id=models.AutoField(primary_key=True)
    category_id=models.ForeignKey(Categories,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    url_slug=models.CharField(max_length=255)
    thumbnail=models.FileField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("sub_category_list")
    

'''
class Products(models.Model):
    id=models.AutoField(primary_key=True)
    url_slug=models.CharField(max_length=255)
    subcategories_id=models.ForeignKey(SubCategories,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    product_max_price=models.CharField(max_length=255)
    product_discount_price=models.CharField(max_length=255)
    product_description=models.TextField()
    product_long_description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    added_by_merchant=models.ForeignKey(MerchantUser,on_delete=models.CASCADE)
    in_stock_total=models.IntegerField(default=1)
    is_active=models.IntegerField(default=1)
'''
''' 
class Location(models.Model):
    zip_code = models.IntegerField()
    latitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)


    def save(self, *args, **kwargs):
        r = requests.get(f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&q={self.zip_code}&facet=state&facet=timezone&facet=dst')
        self.latitude = r.json()['records'][0]['fields']['latitude']
        self.longitude = r.json()['records'][0]['fields']['longitude']
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.zip_code)

'''

class Cat(models.Model):
    created_by= models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=255,unique=True)
    level=models.CharField(max_length=50,default='A')
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active=models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Categories"

    @classmethod
    def get_default_pk(cls):
        cat, created = cls.objects.get_or_create(
            title='default cat', defaults=dict(description='this is not an cat'))
        return cat.pk 

    def get_absolute_url(self):
        return reverse("training_test")

    def __str__(self):
        return self.title


class SubCat(models.Model):
    category = models.ForeignKey(to=Cat, on_delete=models.CASCADE,default=Cat.get_default_pk)
    #category = models.ManyToManyField(Cat, blank=True,related_name='cats')
    created_by= models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #doc=models.FileField(default="None",upload_to='training/docs/')
    #link=models.CharField(max_length=100,blank=True, null=True)
    #link_name=models.CharField(max_length=255, default='General')
    is_active=models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Subcategories"

    def get_absolute_url(self):
        return reverse("sublist")

    def __str__(self):
        return self.title


class Links(models.Model):
    subcategory = models.ManyToManyField(SubCat, blank=True,related_name='subcats')
    created_by= models.ForeignKey(User, on_delete=models.CASCADE)
    link_name=models.CharField(max_length=255, default='General')
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    doc=models.FileField(default="None",upload_to='training/docs/')
    link=models.CharField(max_length=100,blank=True, null=True)
    is_active=models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "links"

    def get_absolute_url(self):
        return reverse("sublist")

    def __str__(self):
        return self.link_name

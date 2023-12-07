from django.db import models
from main.models import Assets
# # Create your models here.

class Ads(models.Model):
    message= models.TextField(null=True, blank=True)
    image_name = models.ForeignKey(
        Assets, related_name="message_image", on_delete=models.CASCADE,default=1
    )
    link = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.image_name)


class Whatsapp_Groups(models.Model):
    # types
    TYPE_CHOICES = [
        ("investments", "investments"),
        ("Data Analyis", "data_analysis"),
        ("coda", "coda"),
        ("Job Support", "Job_Support"),
        ("Interview", "Interview"),
        ("Mentorship", "Mentorship"),
        ("other", "Other"),
    ]
    group_name = models.CharField(max_length=100, null=True, blank=True)
    group_id = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="Other",
    )
    # message= models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.group_name
    
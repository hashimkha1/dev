from django.db import models
from main.models import Assets
# # Create your models here.

class Ads(models.Model):
    ad_title = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    company_site = models.CharField(max_length=255, null=True, blank=True)
    meeting_link = models.CharField(max_length=500, null=True, blank=True)
    video_link = models.CharField(max_length=500, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    bulletin= models.TextField(null=True, blank=True)
    message= models.TextField(null=True, blank=True)
    image_name = models.ForeignKey(
        Assets, related_name="message_image", on_delete=models.CASCADE,default=1
    )
    link = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ad_title)


class Whatsapp_Groups(models.Model):
    # types
    TYPE_CHOICES = [
        ("investments", "investments"),
        ("data_analysis", "data_analysis"),
        ("coda", "coda"),
        ("Job_Support", "Job_Support"),
        ("interview", "interview"),
        ("mentorship", "mentorship"),
        ("other", "other"),
    ]
    group_name = models.CharField(max_length=100, null=True, blank=True)
    group_id = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="other",
    )
    # message= models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.group_name
    
from django.db import models
from main.models import Assets
# # Create your models here.

class Ads(models.Model):
    # types
    # investments = "investments"
    # data_analysis = "Data Analyis"
    # coda = "coda"
    # other = "other"
    # TYPE_CHOICES = [
    #     (investments, "investments"),
    #     (data_analysis, "data_analysis"),
    #     (coda, "coda"),
    #     (other, "Other"),
    # ]
    message= models.TextField(null=True, blank=True)
    image_name = models.ForeignKey(
        Assets, related_name="message_image", on_delete=models.CASCADE,default=1
    )
    # image_url = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    # type = models.CharField(
    #     max_length=25,
    #     choices=TYPE_CHOICES,
    #     default=other,
    # )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.group_name
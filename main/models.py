from django.db import models

# Create your models here.
class Picture(models.Model):
    backgroundImage = models.ImageField(default='default.jpg', upload_to='background')

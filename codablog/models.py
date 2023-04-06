from django.db import models
from django.urls import reverse
from django.utils import timezone
from main.models import Assets
from django.contrib.auth import get_user_model
# User=settings.AUTH_USER_MODEL
User = get_user_model()

class Post(models.Model):
    asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codablog:post-detail', kwargs={'pk': self.pk})
    
class Testimonials(models.Model):
    # asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)
    writer = models.ForeignKey(
        User,
        verbose_name=("writer name"),
        on_delete=models.CASCADE,
        # related_name="employee_name"
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codablog:post-detail', kwargs={'pk': self.pk})
from django.db.models.signals import post_save
from .models import Applicant_Profile
from accounts.models import CustomerUser
from django.dispatch import receiver


@receiver(post_save, sender=CustomerUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Applicant_Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomerUser)
def save_profile(sender, instance, **kwargs):
    instance.Applicant_Profile.save()

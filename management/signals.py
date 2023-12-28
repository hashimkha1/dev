from django.db.models.signals import post_save
from django.dispatch import receiver
from data.models import ClientAssessment
from accounts.models import CustomerUser
from django.contrib.auth.models import AbstractUser
from mail.custom_email import send_email
from accounts.utils import generate_random_password


@receiver(post_save, sender=ClientAssessment)
def create_customer_user(sender, instance, created, **kwargs):
 
    if created and not CustomerUser.objects.filter(email=instance.email).exists():
        random_password = generate_random_password(8)
        user = CustomerUser.objects.create(
            username = instance.email,
            gender = None,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            category=CustomerUser.Category.Student,
            sub_category=CustomerUser.SubCategory.Other
        )

        # set password
        user.set_password(random_password)
        user.save()
        subject = "Coda Credential"
        send_email( 
        category=2, #because it is a student
        to_email=(user.email,),
        subject=subject, 
        html_template='email/user_credential.html',
        context={'user': user, 'password': random_password})

# Generated by Django 3.0.7 on 2020-09-17 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_applicant_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='cover',
        ),
    ]

# Generated by Django 3.0.7 on 2020-09-17 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_remove_applicant_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='cover',
        ),
    ]

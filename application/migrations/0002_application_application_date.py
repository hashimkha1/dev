# Generated by Django 3.0.7 on 2020-10-23 22:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

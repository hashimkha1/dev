# Generated by Django 3.2.6 on 2022-02-20 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_policy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='policy_type',
        ),
        migrations.AddField(
            model_name='policy',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

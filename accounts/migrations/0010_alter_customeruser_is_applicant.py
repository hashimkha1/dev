# Generated by Django 3.2.6 on 2022-06-23 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220619_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='is_applicant',
            field=models.BooleanField(default=False, verbose_name='Is applicant'),
        ),
    ]

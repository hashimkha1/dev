# Generated by Django 3.0.7 on 2020-09-17 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0014_auto_20200916_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='last_name',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
    ]

# Generated by Django 3.2.6 on 2023-02-21 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_trainingresponsestracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredsubcategory',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

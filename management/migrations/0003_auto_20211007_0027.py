# Generated by Django 3.2.6 on 2021-10-07 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_activity_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(default='Add description on this activity', help_text='Not Required', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='submission',
            field=models.DateTimeField(auto_now=True, help_text='Date formart :mm/dd/yyyy', null=True),
        ),
    ]

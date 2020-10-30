# Generated by Django 3.0.7 on 2020-10-30 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_inteviewupload_upload_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inteviewupload',
            old_name='interviewdb',
            new_name='SQL',
        ),
        migrations.RenameField(
            model_name='inteviewupload',
            old_name='interviewalteryx',
            new_name='alteryx',
        ),
        migrations.RenameField(
            model_name='inteviewupload',
            old_name='interviewother',
            new_name='other',
        ),
        migrations.RenameField(
            model_name='inteviewupload',
            old_name='interviewtab',
            new_name='tableau',
        ),
        migrations.RemoveField(
            model_name='inteviewupload',
            name='Interviewid',
        ),
        migrations.AddField(
            model_name='inteviewupload',
            name='username',
            field=models.CharField(default='coachofanalytics', max_length=30, null=True),
        ),
    ]

# Generated by Django 3.2.6 on 2022-09-01 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_alter_rated_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='laptop_status',
            field=models.BooleanField(default=True, verbose_name='Is lap_status'),
        ),
        migrations.AlterField(
            model_name='rated',
            name='topic',
            field=models.CharField(choices=[('Alteryx', 'Alteryx'), ('Tableau', 'Tableau'), ('Database', 'Database'), ('Other', 'Other')], default='Other', max_length=255),
        ),
    ]

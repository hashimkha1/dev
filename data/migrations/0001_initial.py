# Generated by Django 4.0.3 on 2022-03-13 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('upload_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('category', models.CharField(choices=[('Project Management', 'Project Management'), ('Business Analyst', 'Business Analysis'), ('Quality Assurance', 'Quality Assurance'), ('User Interface', 'User Experience'), ('Reporting', 'Reporting'), ('ETL', 'ETL'), ('Database', 'Database'), ('Python', 'Python'), ('Other', 'Other')], default='Other', max_length=25)),
                ('question_type', models.CharField(choices=[('introduction', 'introduction'), ('Project Story', 'project story'), ('performance', 'performance'), ('methodology', 'methodology'), ('sdlc', 'sdlc'), ('testing', 'testing'), ('environment', 'environment'), ('resume', 'resume'), ('Other', 'Other')], default='Other', max_length=25)),
                ('doc', models.FileField(default='None', upload_to='Uploads/doc/')),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'InterviewUploaded',
            },
        ),
    ]

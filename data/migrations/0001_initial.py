# Generated by Django 3.2.6 on 2022-01-22 03:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewUpload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('upload_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('category', models.CharField(choices=[('Project Management', 'Project Management'), ('Business Analyst', 'Business Analysis'), ('Quality Assurance', 'Quality Assurance'), ('User Interface', 'User Experience'), ('Reporting', 'Reporting'), ('ETL', 'ETL'), ('Database', 'Database'), ('Python', 'Python'), ('Other', 'Other')], default='Other', max_length=25)),
                ('question_type', models.CharField(choices=[('introduction', 'introduction'), ('Project Story', 'project story'), ('performance', 'performance'), ('methodology', 'methodology'), ('sdlc', 'sdlc'), ('testing', 'testing'), ('environment', 'environment'), ('resume', 'resume'), ('Other', 'Other')], default='Other', max_length=25)),
                ('doc', models.FileField(default='None', upload_to='Uploads/doc/')),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'InterviewUploads',
            },
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('doc_type', models.CharField(blank=True, max_length=100, null=True)),
                ('doc_name', models.CharField(blank=True, max_length=100, null=True)),
                ('doc', models.FileField(upload_to='Uploads/doc/')),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Uploads',
            },
        ),
    ]

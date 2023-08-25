# Generated by Django 3.2.6 on 2023-08-25 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_alter_servicecategory_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female')], default=9999)),
                ('phone', models.CharField(blank=True, default='90001', max_length=100, null=True)),
                ('application_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/doc/')),
                ('type', models.CharField(choices=[('Applicant', 'Applicant'), ('Other', 'Other')], default='Other', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('upload_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('policy_type', models.CharField(choices=[('Leave', 'Leave'), ('Working Hours', 'Working Hours'), ('Working Days', 'Working Days'), ('Unpaid Training', 'Unpaid_Training'), ('Location', 'Location'), ('Other', 'Other')], default='Other', max_length=25)),
                ('description', models.TextField()),
                ('policy_doc', models.FileField(blank=True, default=None, null=True, upload_to='policy/doc/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=254, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=500, null=True)),
                ('section', models.CharField(blank=True, default='A', max_length=2)),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='Application_Profile_pics')),
                ('upload_a', models.FileField(blank=True, null=True, upload_to='Application_Profile/uploads')),
                ('upload_b', models.FileField(blank=True, null=True, upload_to='Application_Profile/uploads')),
                ('upload_c', models.FileField(blank=True, null=True, upload_to='Application_Profile/uploads')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is featured')),
                ('laptop_status', models.BooleanField(default=True, verbose_name='Is lap_status')),
                ('national_id_no', models.CharField(blank=True, max_length=254, null=True)),
                ('id_file', models.ImageField(blank=True, null=True, upload_to='id_files/')),
                ('emergency_name', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_address', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_citizenship', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_national_id_no', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_phone', models.CharField(blank=True, max_length=254, null=True)),
                ('emergency_email', models.CharField(blank=True, max_length=254, null=True)),
                ('account_number', models.CharField(max_length=50)),
                ('account_holder_name', models.CharField(max_length=100)),
                ('bank_name', models.CharField(max_length=200)),
                ('administration_letter', models.TextField()),
                ('handwritten_letter', models.ImageField(upload_to='handwritten_letters/')),
                ('academic_credentials', models.FileField(upload_to='academic_credentials/')),
                ('image2', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile_image', to='main.assets')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reporting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.CharField(blank=True, max_length=50, null=True)),
                ('interview_type', models.CharField(choices=[('Internal Interview', 'Internal Interview'), ('First Interview', 'First Interview'), ('Second Interview', 'Second Interview'), ('Third Interview', 'Third Interview'), ('Other', 'Other')], default='other', max_length=25)),
                ('method', models.CharField(blank=True, choices=[('Direct', 'Direct'), ('Indirect', 'Indirect')], max_length=25, null=True)),
                ('reporting_date', models.DateTimeField(blank=True, null=True, verbose_name='Reporting Date(mm/dd/yyyy)')),
                ('update_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('comment', models.TextField()),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporting_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rated',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('topic', models.CharField(choices=[('Alteryx', 'Alteryx'), ('Tableau', 'Tableau'), ('Database', 'Database'), ('Other', 'Other')], default='Other', max_length=255)),
                ('uploadlinkurl', models.CharField(blank=True, max_length=1000, null=True)),
                ('rating_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('projectDescription', models.BooleanField(default=False)),
                ('requirementsAnalysis', models.BooleanField(default=False)),
                ('development', models.BooleanField(default=False)),
                ('testing', models.BooleanField(default=False)),
                ('deployment', models.BooleanField(default=False)),
                ('totalpoints', models.IntegerField(default=0)),
                ('employeename', models.ForeignKey(blank=True, default=1, limit_choices_to=models.Q(('is_staff', True), ('is_applicant', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='rating_empname', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InteviewUploads',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, null=True)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ppt', models.FileField(default=None, upload_to='Powerpoints/doc/')),
                ('report', models.FileField(default=None, upload_to='Reports/doc/')),
                ('workflow', models.FileField(default=None, upload_to='Workflows/doc/')),
                ('proc', models.FileField(default=None, upload_to='Procedures/doc/')),
                ('other', models.FileField(default=None, upload_to='Others/doc/')),
                ('Applicant', models.ManyToManyField(to='application.Application')),
            ],
        ),
    ]

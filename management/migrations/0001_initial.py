# Generated by Django 3.2.6 on 2022-08-16 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facebook_access_token', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_page_id', models.CharField(blank=True, max_length=100, null=True)),
                ('page_name', models.CharField(blank=True, max_length=100, null=True)),
                ('post_description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Uploads/Facebook/')),
                ('file', models.FileField(blank=True, null=True, upload_to='Uploads/Facebook/')),
                ('link', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('staff', models.CharField(blank=True, default='admin', max_length=100, null=True)),
                ('upload_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.CharField(blank=True, max_length=1000, null=True)),
                ('department', models.CharField(choices=[('HR', 'HR'), ('IT', 'IT'), ('Marketing', 'Marketing'), ('Finance', 'Finance'), ('Security', 'Security'), ('Management', 'Management'), ('Health', 'Health'), ('Other', 'Other')], default='Other', max_length=100)),
                ('day', models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='Sunday', max_length=25)),
                ('description', models.TextField()),
                ('policy_doc', models.FileField(blank=True, default=None, null=True, upload_to='policy/doc/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_internal', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Meetings', 'Meetings'), ('Data Analysis', 'Data Analysis'), ('Stocks & Options', 'Stocks & Options'), ('Website Development', 'Website Development'), ('Department', 'Department'), ('Other', 'Other')], default='Other', max_length=55, unique=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='Group A', help_text='Required', max_length=255, verbose_name='group')),
                ('activity_name', models.CharField(help_text='Required', max_length=255, verbose_name='Activity Name')),
                ('description', models.TextField(default='Add description on this activity', help_text='Not Required', verbose_name='description')),
                ('slug', models.SlugField(blank=True, default='slug', max_length=255)),
                ('duration', models.PositiveIntegerField(default=1, error_messages={'name': {' max_length': 'Points must be less than Maximum Points'}}, help_text='Should be less than Maximum Points assigned')),
                ('point', models.DecimalField(decimal_places=2, error_messages={'name': {' max_length': 'Points must be less than Maximum Points'}}, help_text='Should be less than Maximum Points assigned', max_digits=10)),
                ('mxpoint', models.DecimalField(decimal_places=2, error_messages={'name': {' max_length': 'The maximum points must be between 0 and 199'}}, help_text='Maximum 200', max_digits=10)),
                ('mxearning', models.DecimalField(decimal_places=2, error_messages={'name': {' max_length': 'The earning must be between 0 and 4999.99'}}, help_text='Maximum 4999.99', max_digits=10)),
                ('submission', models.DateTimeField(auto_now=True, help_text='Date formart :mm/dd/yyyy', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=True)),
                ('category', models.ForeignKey(default=management.models.Tag.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='management.tag')),
                ('employee', models.ForeignKey(default=999, limit_choices_to=models.Q(('is_active', True)), on_delete=django.db.models.deletion.RESTRICT, related_name='user_assiged', to=settings.AUTH_USER_MODEL)),
                ('groupname', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.taskgroups')),
            ],
            options={
                'verbose_name_plural': 'Tasks',
                'ordering': ('-submission',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(default=None, max_length=100, null=True)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('type', models.CharField(default=None, max_length=100, null=True)),
                ('activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Other', 'Other')], default='Other', max_length=25)),
                ('department', models.CharField(choices=[('HR Department', 'HR Department'), ('IT Department', 'IT Department'), ('Marketing Department', 'Marketing Department'), ('Finance Department', 'Finance Department'), ('Security Department', 'Security Department'), ('Management Department', 'Management Department'), ('Health Department', 'Health Department'), ('Other', 'Other')], default='Other', max_length=100)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Health', 'Health'), ('Transport', 'Transport'), ('Food & Accomodation', 'Food & Accomodation'), ('Internet & Airtime', 'Internet & Airtime'), ('Recruitment', 'Recruitment'), ('Labour', 'Labour'), ('Management', 'Management'), ('Electricity', 'Electricity'), ('Construction', 'Construction'), ('Other', 'Other')], default='Other', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_api_key', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_api_key_secret', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_bearer_token', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_access_token', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_access_token_secret', models.CharField(blank=True, max_length=500, null=True)),
                ('post_description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Uploads/Twitter/')),
                ('link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_name', models.CharField(default='General', max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doc', models.FileField(default='None', upload_to='evidence/docs/')),
                ('link', models.CharField(blank=True, max_length=1000, null=True)),
                ('linkpassword', models.CharField(default='No Password Needed', max_length=255)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Is featured')),
                ('added_by', models.ForeignKey(limit_choices_to=models.Q(('is_employee', True), ('is_admin', True), ('is_superuser', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.task')),
            ],
            options={
                'verbose_name_plural': 'links',
            },
        ),
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='Group A', help_text='Required', max_length=255, verbose_name='group')),
                ('activity_name', models.CharField(help_text='Required', max_length=255, verbose_name='Activity Name')),
                ('description', models.TextField(default='Add description on this activity', help_text='Not Required', verbose_name='description')),
                ('slug', models.SlugField(blank=True, default='slug', max_length=255)),
                ('duration', models.PositiveIntegerField(default=1, error_messages={'name': {' max_length': 'Points must be less than Maximum Points'}}, help_text='Should be less than Maximum Points assigned')),
                ('point', models.DecimalField(decimal_places=2, error_messages={'name': {' max_length': 'Points must be less than Maximum Points'}}, help_text='Should be less than Maximum Points assigned', max_digits=10)),
                ('mxpoint', models.DecimalField(decimal_places=2, error_messages={'name': {' max_length': 'The maximum points must be between 0 and 199'}}, help_text='Maximum 200', max_digits=10)),
                ('mxearning', models.DecimalField(decimal_places=2, error_messages={'name': {' max_length': 'The earning must be between 0 and 4999.99'}}, help_text='Maximum 4999.99', max_digits=10)),
                ('submission', models.DateTimeField(auto_now=True, help_text='Date formart :mm/dd/yyyy', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True, help_text='Date formart :mm/dd/yyyy', null=True)),
                ('category', models.ForeignKey(default=management.models.Tag.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='management.tag')),
                ('employee', models.ForeignKey(default=999, on_delete=django.db.models.deletion.RESTRICT, related_name='history_user_assiged', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Reporting', 'Reporting'), ('ETL', 'ETL'), ('Database', 'Database'), ('Website', 'Website'), ('Other', 'Other')], default='Other', max_length=25)),
                ('requestor', models.CharField(choices=[('Management', 'Management'), ('Client', 'Client'), ('Other', 'Other')], default='Other', max_length=25)),
                ('company', models.CharField(default='CODA', max_length=255)),
                ('created_by', models.CharField(default='admin', max_length=255)),
                ('app', models.CharField(default='Data Analysis', max_length=255)),
                ('duration', models.IntegerField(default=4)),
                ('delivery_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('what', models.TextField()),
                ('why', models.TextField()),
                ('how', models.TextField()),
                ('doc', models.FileField(blank=True, null=True, upload_to='Uploads/Support_Docs/')),
                ('is_active', models.BooleanField(default=True)),
                ('assigned_to', models.ForeignKey(default=1, limit_choices_to=models.Q(('is_employee', True), ('is_admin', True), ('is_superuser', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Requirements',
            },
        ),
        migrations.CreateModel(
            name='Outflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(default=None, max_length=100, null=True)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('type', models.CharField(default=None, max_length=100, null=True)),
                ('activity_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Other', 'Other')], default='Other', max_length=25)),
                ('department', models.CharField(choices=[('HR Department', 'HR Department'), ('IT Department', 'IT Department'), ('Marketing Department', 'Marketing Department'), ('Finance Department', 'Finance Department'), ('Security Department', 'Security Department'), ('Management Department', 'Management Department'), ('Health Department', 'Health Department'), ('Other', 'Other')], default='Other', max_length=100)),
                ('category', models.CharField(choices=[('Salary', 'Salary'), ('Health', 'Health'), ('Transport', 'Transport'), ('Food & Accomodation', 'Food & Accomodation'), ('Internet & Airtime', 'Internet & Airtime'), ('Recruitment', 'Recruitment'), ('Labour', 'Labour'), ('Management', 'Management'), ('Electricity', 'Electricity'), ('Construction', 'Construction'), ('Other', 'Other')], default='Other', max_length=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Inflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Job_Support', 'Job_Support'), ('Interview', 'Interview'), ('Training', 'Training'), ('Stocks', 'Stocks'), ('Blockchain', 'Blockchain'), ('Mentorship', 'Mentorship'), ('Any Other', 'Other')], max_length=25)),
                ('task', models.CharField(choices=[('reporting', 'reporting'), ('database', 'database'), ('Business Analysis', 'Business Analysis'), ('Data Cleaning', 'Data Cleaning'), ('Options', 'Options'), ('Any Other', 'Other')], max_length=25)),
                ('method', models.CharField(choices=[('Cash', 'Cash'), ('Mpesa', 'Mpesa'), ('Check', 'Check'), ('Cashapp', 'Cashapp'), ('Zelle', 'Zelle'), ('Venmo', 'Venmo'), ('Paypal', 'Paypal'), ('Any Other', 'Other')], default='Any Other', max_length=25)),
                ('period', models.CharField(choices=[('Weekly', 'Weekly'), ('Bi_Weekly', 'Bi_Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Any Other', max_length=25)),
                ('receiver', models.CharField(default=None, max_length=100, null=True)),
                ('phone', models.CharField(default=None, max_length=50, null=True)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receipt_link', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('transaction_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('description', models.TextField(default=None, max_length=1000)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['transaction_date'],
            },
        ),
    ]

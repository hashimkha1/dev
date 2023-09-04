<<<<<<< HEAD
# Generated by Django 3.2.6 on 2023-08-23 13:25
=======
# Generated by Django 3.2.6 on 2023-08-29 09:07
>>>>>>> coda_prod2

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0001_initial'),
    ]

    operations = [
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
            options={
                'verbose_name_plural': 'Policies',
            },
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
            ],
            options={
                'verbose_name_plural': 'Tasks',
                'ordering': ('-submission',),
            },
        ),
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Meetings', 'Meetings'), ('Data Analysis', 'Data Analysis'), ('Stocks & Options', 'Stocks & Options'), ('Website Development', 'Website Development'), ('Department', 'Department'), ('Other', 'Other')], default='Other', max_length=55, unique=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Task Categories',
            },
        ),
        migrations.CreateModel(
            name='Whatsapp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('screen_id', models.CharField(blank=True, max_length=500, null=True)),
                ('group_name', models.CharField(blank=True, max_length=100, null=True)),
                ('group_id', models.CharField(blank=True, max_length=100, null=True)),
                ('image_url', models.CharField(blank=True, max_length=500, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, 'Level 1'), (2, 'Level 2'), (3, 'Level 3'), (4, 'Level 4'), (5, 'Level 5')])),
                ('session', models.PositiveIntegerField()),
                ('session_link', models.CharField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, default='No Comment', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_name', to='data.featuredcategory', verbose_name='categories')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_name', to='accounts.department', verbose_name='departments')),
                ('presenter', models.ForeignKey(limit_choices_to=models.Q(('is_active', True)), on_delete=django.db.models.deletion.CASCADE, related_name='employee_name', to=settings.AUTH_USER_MODEL, verbose_name='presenter name')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory_name', to='data.featuredsubcategory', verbose_name='Subcategory')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title', to='data.featuredactivity', verbose_name='topic')),
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
                ('added_by', models.ForeignKey(limit_choices_to=models.Q(('is_staff', True), ('is_admin', True), ('is_superuser', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.task')),
            ],
            options={
                'verbose_name_plural': 'Task Reference',
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
                ('category', models.ForeignKey(default=management.models.TaskCategory.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='management.taskcategory')),
                ('employee', models.ForeignKey(default=999, on_delete=django.db.models.deletion.RESTRICT, related_name='history_user_assiged', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'TaskHistory',
                'ordering': ['-submission'],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ForeignKey(default=management.models.TaskCategory.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='management.taskcategory'),
        ),
        migrations.AddField(
            model_name='task',
            name='employee',
            field=models.ForeignKey(default=999, limit_choices_to=models.Q(('is_active', True)), on_delete=django.db.models.deletion.RESTRICT, related_name='user_assiged', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='groupname',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.taskgroups'),
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Reporting', 'Reporting'), ('ETL', 'ETL'), ('Database', 'Database'), ('Website', 'Website'), ('Other', 'Other')], default='Other', max_length=25)),
                ('requestor', models.CharField(choices=[('Management', 'Management'), ('Client', 'Client'), ('Other', 'Other')], default='Other', max_length=25)),
                ('status', models.CharField(choices=[('Critical', 'Critical'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Low', max_length=25)),
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
                ('comments', models.TextField(blank=True, default='No Comment', null=True)),
                ('doc', models.FileField(blank=True, null=True, upload_to='Uploads/Support_Docs/')),
                ('pptlink', models.CharField(blank=True, max_length=1000, null=True)),
                ('videolink', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_tested', models.BooleanField(default=True)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(default=1, limit_choices_to=models.Q(('is_staff', True), ('is_admin', True), ('is_superuser', True), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(blank=True, default=1, limit_choices_to=models.Q(('is_staff', True), ('is_client', True), ('is_admin', True), ('is_superuser', True), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name_plural': 'Requirements',
            },
        ),
        migrations.CreateModel(
            name='ProcessJustification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('justification', models.CharField(blank=True, max_length=255, null=True)),
                ('crated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('requirements', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Requirement_in_Process', to='management.requirement')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessBreakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakdown', models.CharField(blank=True, max_length=255, null=True)),
                ('time', models.PositiveIntegerField(blank=True, null=True)),
                ('Quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('total', models.PositiveIntegerField(blank=True, null=True)),
                ('crated_at', models.DateTimeField(auto_now=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Process_in_breakdown', to='management.processjustification')),
            ],
        ),
        migrations.CreateModel(
            name='Meetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_topic', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_id', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_type', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_link', models.CharField(blank=True, max_length=500, null=True)),
                ('meeting_description', models.TextField(blank=True, null=True)),
                ('meeting_time', models.TimeField(default=django.utils.timezone.now)),
                ('frequency', models.IntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Bi Weekly'), (4, 'Monthly'), (5, 'Yearly')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.taskcategory')),
                ('department', models.ForeignKey(default=accounts.models.Department.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
            ],
<<<<<<< HEAD
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Meetings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_topic', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_id', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_type', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_link', models.CharField(blank=True, max_length=500, null=True)),
                ('meeting_description', models.TextField(blank=True, null=True)),
                ('meeting_time', models.TimeField(default=django.utils.timezone.now)),
                ('frequency', models.IntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Bi Weekly'), (4, 'Monthly'), (5, 'Yearly')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('category', models.ForeignKey(default=management.models.TaskCategory.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='management.taskcategory')),
                ('department', models.ForeignKey(default=accounts.models.Department.get_default_pk, on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
            ],
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
=======
>>>>>>> coda_prod2
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_api_key', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_api_key_secret', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_bearer_token', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_access_token', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_access_token_secret', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_access_token', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_page_id', models.CharField(blank=True, max_length=100, null=True)),
                ('page_name', models.CharField(blank=True, max_length=100, null=True)),
                ('post_description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Uploads/Facebook/')),
                ('whatapp_group_name', models.CharField(blank=True, max_length=100, null=True)),
                ('whatapp_group_id', models.CharField(blank=True, max_length=100, null=True)),
                ('whatapp_image_url', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

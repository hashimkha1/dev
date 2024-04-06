# Generated by Django 3.2.6 on 2024-04-06 19:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_value', models.DecimalField(decimal_places=2, default=9999, max_digits=12)),
                ('serial_number', models.CharField(max_length=50, null=True)),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category_type', models.CharField(choices=[('Asset', 'Asset'), ('Liability', 'Liability'), ('Equity', 'Equity')], default='Asset', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Balance Sheet Categories',
                'unique_together': {('name', 'category_type')},
            },
        ),
    ]

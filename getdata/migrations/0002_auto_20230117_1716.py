# Generated by Django 3.2.6 on 2023-01-17 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getdata', '0001_initial'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='stockmarket',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('symbol', models.CharField(max_length=255)),
        #         ('action', models.CharField(max_length=255)),
        #         ('qty', models.PositiveIntegerField()),
        #         ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
        #         ('date', models.DateTimeField()),
        #     ],
        # ),
        migrations.AddField(
            model_name='cashappmail',
            name='amount',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cashappmail',
            name='destination',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

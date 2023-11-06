<<<<<<< HEAD
<<<<<<< HEAD
# Generated by Django 3.2.6 on 2023-08-23 13:20
=======
# Generated by Django 3.2.6 on 2023-08-29 09:03
>>>>>>> coda_prod2
=======
# Generated by Django 3.2.6 on 2023-09-07 13:30
>>>>>>> origin/main_prod

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cost_Basis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('expiration_date', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('qty', models.CharField(blank=True, max_length=255, null=True)),
                ('strike_price', models.CharField(blank=True, max_length=255, null=True)),
                ('open_date', models.CharField(blank=True, max_length=255, null=True)),
                ('cost', models.CharField(blank=True, max_length=255, null=True)),
                ('covered', models.CharField(blank=True, max_length=255, null=True)),
                ('security_number', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'cost_basis',
            },
        ),
        migrations.CreateModel(
            name='covered_calls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('expiry', models.CharField(blank=True, max_length=255, null=True)),
                ('days_to_expiry', models.CharField(blank=True, max_length=255, null=True)),
                ('strike_price', models.CharField(blank=True, max_length=255, null=True)),
                ('mid_price', models.CharField(blank=True, max_length=255, null=True)),
                ('bid_price', models.CharField(blank=True, max_length=255, null=True)),
                ('ask_price', models.CharField(blank=True, max_length=255, null=True)),
<<<<<<< HEAD
                ('implied_volatility_rank', models.CharField(blank=True, max_length=255, null=True)),
=======
                ('rank', models.CharField(blank=True, max_length=255, null=True)),
>>>>>>> origin/main_prod
                ('earnings_date', models.CharField(blank=True, max_length=255, null=True)),
                ('earnings_flag', models.CharField(blank=True, max_length=255, null=True)),
                ('stock_price', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_return', models.CharField(blank=True, max_length=255, null=True)),
                ('annualized_return', models.CharField(blank=True, max_length=255, null=True)),
                ('distance_to_strike', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
<<<<<<< HEAD
=======
                ('on_date', models.CharField(blank=True, max_length=255, null=True)),
>>>>>>> origin/main_prod
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'covered_calls',
            },
        ),
        migrations.CreateModel(
            name='credit_spread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('strategy', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('sell_strike', models.CharField(blank=True, max_length=255, null=True)),
                ('buy_strike', models.CharField(blank=True, max_length=255, null=True)),
                ('expiry', models.CharField(blank=True, max_length=255, null=True)),
                ('premium', models.CharField(blank=True, max_length=255, null=True)),
                ('width', models.CharField(blank=True, max_length=255, null=True)),
                ('prem_width', models.CharField(blank=True, max_length=255, null=True)),
                ('rank', models.CharField(blank=True, max_length=255, null=True)),
                ('earnings_date', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
<<<<<<< HEAD
=======
                ('on_date', models.CharField(blank=True, max_length=255, null=True)),
>>>>>>> origin/main_prod
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'credit_spread',
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='cryptomarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'cryptomarket',
            },
        ),
        migrations.CreateModel(
=======
>>>>>>> origin/main_prod
            name='Investment_rates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('base_amount', models.PositiveIntegerField(blank=True, null=True)),
                ('initial_return', models.PositiveIntegerField(blank=True, null=True)),
                ('increment_rate', models.PositiveIntegerField(blank=True, null=True)),
                ('increment_threshold', models.PositiveIntegerField(blank=True, null=True)),
                ('decrease_threshold', models.PositiveIntegerField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('investment_rate', models.DecimalField(decimal_places=2, default=0.33, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Investment_rates',
            },
        ),
        migrations.CreateModel(
            name='Options_Returns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('expiration_date', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('event', models.CharField(blank=True, max_length=255, null=True)),
                ('qty', models.CharField(blank=True, max_length=255, null=True)),
                ('strike_price', models.CharField(blank=True, max_length=255, null=True)),
                ('open_date', models.CharField(blank=True, max_length=255, null=True)),
                ('closed_date', models.CharField(blank=True, max_length=255, null=True)),
                ('cost', models.CharField(blank=True, max_length=255, null=True)),
                ('LT_GL', models.CharField(blank=True, max_length=255, null=True)),
                ('ST_GL', models.CharField(blank=True, max_length=255, null=True)),
                ('proceeds', models.CharField(blank=True, max_length=255, null=True)),
                ('covered', models.CharField(blank=True, max_length=255, null=True)),
                ('security_number', models.CharField(blank=True, max_length=255, null=True)),
                ('cbm', models.CharField(blank=True, max_length=255, null=True)),
                ('other', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'returns',
            },
        ),
        migrations.CreateModel(
            name='Oversold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('strike_price', models.CharField(blank=True, max_length=255, null=True)),
                ('implied_volatility_rank', models.CharField(blank=True, max_length=255, null=True)),
                ('stock_price', models.CharField(blank=True, max_length=255, null=True)),
                ('expiry', models.CharField(blank=True, max_length=255, null=True)),
                ('earnings_date', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
<<<<<<< HEAD
=======
                ('on_date', models.CharField(blank=True, max_length=255, null=True)),
>>>>>>> origin/main_prod
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'ShortPut',
            },
        ),
        migrations.CreateModel(
            name='ShortPut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('expiry', models.CharField(blank=True, max_length=255, null=True)),
                ('days_to_expiry', models.CharField(blank=True, max_length=255, null=True)),
                ('strike_price', models.CharField(blank=True, max_length=255, null=True)),
                ('mid_price', models.CharField(blank=True, max_length=255, null=True)),
                ('bid_price', models.CharField(blank=True, max_length=255, null=True)),
                ('ask_price', models.CharField(blank=True, max_length=255, null=True)),
                ('implied_volatility_rank', models.CharField(blank=True, max_length=255, null=True)),
                ('earnings_date', models.CharField(blank=True, max_length=255, null=True)),
                ('earnings_flag', models.CharField(blank=True, max_length=255, null=True)),
                ('stock_price', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_return', models.CharField(blank=True, max_length=255, null=True)),
                ('annualized_return', models.CharField(blank=True, max_length=255, null=True)),
                ('distance_to_strike', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
<<<<<<< HEAD
=======
                ('on_date', models.CharField(blank=True, max_length=255, null=True)),
>>>>>>> origin/main_prod
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'ShortPut',
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='stockmarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('qty', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'stockmarket',
=======
            name='Ticker_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('overallrisk', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('sharesshort', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('enterprisetoebitda', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('ebitda', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('quickratio', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('currentratio', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('revenuegrowth', models.DecimalField(blank=True, decimal_places=3, max_digits=17, null=True)),
                ('fetched_date', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Option Measures',
>>>>>>> origin/main_prod
            },
        ),
        migrations.CreateModel(
            name='Investor_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('protected_capital', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_invested', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('positions', models.PositiveIntegerField(blank=True, null=True)),
                ('bi_weekly_returns', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(blank=True, max_length=255, null=True)),
                ('client_signature', models.CharField(blank=True, max_length=255, null=True)),
                ('company_rep', models.CharField(blank=True, max_length=255, null=True)),
                ('contract_date', models.DateField(auto_now_add=True, null=True)),
                ('investor', models.ForeignKey(limit_choices_to={'is_active': True, 'is_client': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Investor_Information',
            },
        ),
        migrations.CreateModel(
            name='Investments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_date', models.DateField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('client', models.ForeignKey(limit_choices_to={'is_active': True, 'is_client': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

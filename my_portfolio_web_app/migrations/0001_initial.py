# Generated by Django 3.1.3 on 2020-12-01 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialInstrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('price_each_quantity', models.IntegerField(default=1)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_my_portfolio_web_app.financialinstrument_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvestmentIndividualAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('security_quantity', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Security Quantity')),
                ('broker', models.CharField(max_length=10)),
                ('ars_commissions', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Commissions ($)')),
                ('usd_commissions', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Commissions (USD)')),
                ('price_amount', models.DecimalField(decimal_places=8, default=0, max_digits=20)),
                ('financial_instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_portfolio_web_app.financialinstrument', verbose_name='Financial Instrument')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_my_portfolio_web_app.transaction_set+', to='contenttypes.contenttype')),
                ('price_unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='price_unit', to='my_portfolio_web_app.financialinstrument')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('financialinstrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.financialinstrument')),
                ('maturity_date', models.DateField(verbose_name='Maturity Date')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.financialinstrument',),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('financialinstrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.financialinstrument')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.financialinstrument',),
        ),
        migrations.CreateModel(
            name='FinancialInstrumentTenderingPayment',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.transaction')),
                ('referenced_financial_instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_portfolio_web_app.financialinstrument')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.transaction', models.Model),
        ),
        migrations.CreateModel(
            name='Inflow',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.transaction')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.transaction',),
        ),
        migrations.CreateModel(
            name='Outflow',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.transaction')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.transaction',),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('financialinstrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.financialinstrument')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.financialinstrument',),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.transaction')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.transaction', models.Model),
        ),
        migrations.CreateModel(
            name='InvestmentPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('individual_accounts', models.ManyToManyField(to='my_portfolio_web_app.InvestmentIndividualAccount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='investmentindividualaccount',
            name='transactions',
            field=models.ManyToManyField(to='my_portfolio_web_app.Transaction'),
        ),
        migrations.CreateModel(
            name='CouponClipping',
            fields=[
                ('financialinstrumenttenderingpayment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.financialinstrumenttenderingpayment')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.financialinstrumenttenderingpayment',),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('trade_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.trade')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.trade',),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('trade_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.trade')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.trade',),
        ),
        migrations.CreateModel(
            name='StockDividend',
            fields=[
                ('financialinstrumenttenderingpayment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.financialinstrumenttenderingpayment')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.financialinstrumenttenderingpayment',),
        ),
    ]
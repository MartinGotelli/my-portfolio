# Generated by Django 3.1.3 on 2022-02-07 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import my_portfolio_web_app.model.my_portfolio_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialInstrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', my_portfolio_web_app.model.my_portfolio_model.UpperCaseCharField(max_length=200, unique=True, verbose_name='Código')),
                ('description', models.CharField(max_length=200, verbose_name='Descripción')),
                ('price_each_quantity', models.PositiveIntegerField(default=1, verbose_name='Precio por Cada')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_my_portfolio_web_app.financialinstrument_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
        ),
        migrations.CreateModel(
            name='InvestmentIndividualAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Descripción')),
                ('authorized_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Usuarios Autorizados')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', my_portfolio_web_app.model.my_portfolio_model.CalendarDateField(verbose_name='Fecha')),
                ('security_quantity', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Cantidad Nominal')),
                ('broker', models.CharField(choices=[('IOL', 'IOL'), ('BALANZ', 'BALANZ')], max_length=10)),
                ('ars_commissions', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Comisiones ($)')),
                ('usd_commissions', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Comisiones (USD)')),
                ('price_amount', models.DecimalField(decimal_places=6, default=0.0, max_digits=20, verbose_name='Precio')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_portfolio_web_app.investmentindividualaccount', verbose_name='Cuenta')),
                ('financial_instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_portfolio_web_app.financialinstrument', verbose_name='Instrumento')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_my_portfolio_web_app.transaction_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
        ),
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('financialinstrument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='my_portfolio_web_app.financialinstrument')),
                ('maturity_date', my_portfolio_web_app.model.my_portfolio_model.CalendarDateField(verbose_name='Fecha de Vencimiento')),
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
                ('referenced_financial_instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_portfolio_web_app.financialinstrument', verbose_name='Instrumento Referencia')),
            ],
            options={
                'abstract': False,
            },
            bases=('my_portfolio_web_app.transaction', models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
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
            bases=('my_portfolio_web_app.transaction', models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
        ),
        migrations.CreateModel(
            name='UserIntegrationConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iol_username', models.CharField(max_length=200, verbose_name='Usuario IOL')),
                ('iol_password', django_cryptography.fields.encrypt(models.CharField(max_length=200, verbose_name='Contraseña IOL'))),
                ('google_sheet_id', models.CharField(max_length=255, verbose_name='ID Google Sheet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
        ),
        migrations.CreateModel(
            name='InvestmentPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Descripción')),
                ('authorized_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Usuarios Autorizados')),
                ('individual_accounts', models.ManyToManyField(to='my_portfolio_web_app.InvestmentIndividualAccount', verbose_name='Cuentas')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, my_portfolio_web_app.model.my_portfolio_model.MyPortfolioModelBehavior),
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
        migrations.AddField(
            model_name='transaction',
            name='price_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='price_unit', to='my_portfolio_web_app.currency', verbose_name='Moneda de Pago'),
        ),
    ]

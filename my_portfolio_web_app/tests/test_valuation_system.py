from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from my_portfolio_web_app.model.financial_instrument import (
    Bond,
    Currency,
    Stock,
    ars,
    usd,
)
from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    Inflow,
    Purchase,
    Sale,
)
from my_portfolio_web_app.model.valuation_system import (
    ValuationSourceFromDictionary,
    ValuationSystem,
)

today = date(2020, 2, 2)
tomorrow = date(2020, 2, 3)
after_tomorrow = date(2020, 2, 4)


class TestValuationSystem(TestCase):
    usd = usd
    eur = Currency(code='EUR', description='Euro')
    meli = Stock(code="MELI", description="MERCADOLIBRE")

    def valuation_system(self):
        return ValuationSystem(ValuationSourceFromDictionary({
            today: {
                self.ay24(): [Measurement(200, self.ars()), Measurement(1.23, self.usd)],
                self.meli: [Measurement(1150, self.ars())]
            },
            tomorrow: {
                self.ay24(): [Measurement(210, self.ars()), Measurement(1.23, self.usd)]
            }
        }))

    def ars_for(self, amount):
        return Measurement(amount, self.ars())

    def usd_for(self, amount):
        return Measurement(amount, self.usd)

    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()
        Currency.objects.create(code='$', description='Pesos')
        Bond.objects.create(code='AY24', description='Bonar 2024', maturity_date=tomorrow)

    @staticmethod
    def ars():
        return Currency.objects.get(code='$')

    @staticmethod
    def ay24():
        return Bond.objects.get(code='AY24')

    def test_creation(self):
        mock_valuation_system = ValuationSystem("source")
        self.assertEqual(mock_valuation_system.source, "source")

    def test_valuate_instrument_on(self):
        self.assertEqual(self.valuation_system().valuate_instrument_on(self.ay24(), self.ars(), today),
                         self.ars_for(200))

    def test_valuate_transaction_on(self):
        account = InvestmentIndividualAccount.objects.create(description='Test account')
        purchase = Purchase.objects.create(date=today, security_quantity=2000, financial_instrument=self.ay24(),
                                           price=self.ars_for(180), broker="IOL", account=account)
        self.assertEqual(self.valuation_system().valuate_transaction_on(purchase, self.ars(), today),
                         self.ars_for(200 * 2000))

    def test_valuate_account_on(self):
        account = InvestmentIndividualAccount.objects.create(description="Martín")
        Inflow.objects.create(date=today, security_quantity=180 * 2000 + 185 * 100 - 1200 * 205,
                              financial_instrument=self.ars(), broker="IOL", account=account)
        Purchase.objects.create(date=today, security_quantity=2000, financial_instrument=self.ay24(),
                                price=self.ars_for(180), broker="IOL", account=account)
        Purchase.objects.create(date=today, security_quantity=100, financial_instrument=self.ay24(),
                                price=self.ars_for(185), broker="IOL", account=account)
        Sale.objects.create(date=today, security_quantity=1200, financial_instrument=self.ay24(),
                            price=self.ars_for(205), broker="IOL", account=account)

        self.assertEqual(self.valuation_system().valuate_account_on(account, self.ars(), today),
                         self.ars_for(200 * (2000 + 100 - 1200)))

    def test_valuate_portfolio_on(self):
        account = InvestmentIndividualAccount.objects.create(description="Martín")
        another_account = InvestmentIndividualAccount.objects.create(description="Pablo")
        portfolio = InvestmentPortfolio.objects.create(description="Portfolio")

        Inflow.objects.create(date=today, security_quantity=180 * 2000 + 185 * 100 - 1200 * 205,
                              financial_instrument=self.ars(), broker="IOL", account=account)
        Purchase.objects.create(date=today, security_quantity=2000, financial_instrument=self.ay24(),
                                price=self.ars_for(180), broker="IOL", account=another_account)
        Purchase.objects.create(date=today, security_quantity=100, financial_instrument=self.ay24(),
                                price=self.ars_for(185), broker="IOL", account=account)
        Sale.objects.create(date=today, security_quantity=1200, financial_instrument=self.ay24(),
                            price=self.ars_for(205), broker="IOL", account=another_account)

        portfolio.individual_accounts.set([account, another_account])

        self.assertEqual(self.valuation_system().valuate_account_on(portfolio, self.ars(), today),
                         self.ars_for(200 * (2000 + 100 - 1200)))

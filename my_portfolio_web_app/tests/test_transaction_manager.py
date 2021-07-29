import datetime

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from my_portfolio_web_app.model.financial_instrument import (
    Bond,
    Currency,
)
from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)
from my_portfolio_web_app.model.measurement import (
    Measurement,
    NullUnit,
)
from my_portfolio_web_app.model.transaction import (
    Purchase,
    Sale,
)
from my_portfolio_web_app.model.transaction_manager import TransactionManager

today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)


class TestTransactionManager(TestCase):
    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()
        Currency.objects.create(code='$', description='Pesos')
        self.one_peso = Measurement(1, self.ars())
        Bond.objects.create(code='AY24', description='Bonar 2024', maturity_date=tomorrow)
        self.account = InvestmentIndividualAccount.objects.create(description='Martín')

    @staticmethod
    def ars():
        return Currency.objects.get(code='$')

    @staticmethod
    def ay24():
        return Bond.objects.get(code='AY24')

    def purchase(self, account):
        return Purchase.objects.create(date=today, security_quantity=5000, financial_instrument=self.ay24(),
                                       price=self.one_peso, broker="IOL", account=account)

    def sale(self, account):
        return Sale.objects.create(date=today, security_quantity=300, financial_instrument=self.ay24(),
                                   price=self.one_peso, broker="IOL", account=account)

    def sale2(self, account):
        return Sale.objects.create(date=today, security_quantity=800, financial_instrument=self.ay24(),
                                   price=self.one_peso, broker="IOL", account=account)

    def tomorrow_purchase(self, account):
        return Purchase.objects.create(date=tomorrow, security_quantity=1000, financial_instrument=self.ay24(),
                                       price=self.one_peso, broker="IOL", account=account)

    def test_creation(self):
        manager = TransactionManager(self.account)
        self.assertEqual(manager.account, self.account)
        self.assertTrue(not manager.transactions)

    def test_manager_dont_update_transactions(self):
        purchase = self.purchase(self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.transactions, [purchase])
        sale = self.sale(self.account)
        new_manager = TransactionManager(self.account)
        self.assertEqual(manager.transactions, [purchase])
        self.assertEqual(new_manager.transactions, [purchase, sale])

    def test_balance_of(self):
        self.purchase(self.account)
        self.sale(self.account)
        self.sale2(self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balance_of_on(self.ay24(), today), 5000 - 300 - 800)

    def test_balance_of_today_is_unaffected_by_tomorrow_purchase(self):
        self.purchase(self.account)
        self.sale(self.account)
        self.sale2(self.account)
        tomorrow_purchase = self.tomorrow_purchase(self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balance_of_on(self.ay24(), today), 5000 - 300 - 800)
        self.assertEqual(manager.balance_of_on(self.ay24(), tomorrow),
                         manager.balance_of_on(self.ay24(), today) + tomorrow_purchase.signed_security_quantity())

    def test_balances_on(self):
        self.purchase(self.account)
        self.sale(self.account)
        self.sale2(self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balances_on(today),
                         Measurement(5000 - 300 - 800, self.ay24()) + Measurement(-5000 + 800 + 300, self.ars()))

    def test_balances_on_with_tomorrow_purchase(self):
        self.purchase(self.account)
        self.sale(self.account)
        self.sale2(self.account)
        self.tomorrow_purchase(self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balances_on(today),
                         Measurement(5000 - 300 - 800, self.ay24()) + Measurement(-5000 + 800 + 300, self.ars()))
        self.assertEqual(manager.balances_on(tomorrow),
                         Measurement(5000 - 300 - 800 + 1000, self.ay24()) + Measurement(-5000 + 800 + 300 - 1000,
                                                                                         self.ars()))

    def test_balances_on_with_closed_financial_instrument(self):
        self.purchase(self.account)
        self.sale(self.account)
        self.sale2(self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balances_on(today),
                         Measurement(5000 - 300 - 800, self.ay24()) + Measurement(-5000 + 800 + 300, self.ars()))
        self.assertEqual(manager.balances_on(after_tomorrow), Measurement(-5000 + 800 + 300, self.ars()))

    def test_balances_on_by_broker(self):
        Purchase.objects.create(date=today, security_quantity=5000, financial_instrument=self.ay24(),
                                price=self.one_peso, broker="IOL", ars_commissions=0.75, account=self.account)
        Purchase.objects.create(date=today, security_quantity=1500, financial_instrument=self.ay24(),
                                price=self.one_peso, broker="BALANZ", ars_commissions=0.25, account=self.account)
        Sale.objects.create(date=today, security_quantity=300, financial_instrument=self.ay24(), price=self.one_peso,
                            broker="IOL", ars_commissions=0.1, account=self.account)
        Sale.objects.create(date=today, security_quantity=800, financial_instrument=self.ay24(), price=self.one_peso,
                            broker="BALANZ", ars_commissions=0.2, account=self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balances_on(today),
                         Measurement(5000 + 1500 - 300 - 800, self.ay24()) + Measurement(
                             -5000 - 1500 + 800 + 300 - 0.75 - 0.25 - 0.1 - 0.2, self.ars()))
        self.assertEqual(manager.balances_on(today, "IOL"),
                         Measurement(5000 - 300, self.ay24()) + Measurement(-5000 + 300 - 0.75 - 0.1, self.ars()))
        self.assertEqual(manager.balances_on(today, "BALANZ"),
                         Measurement(1500 - 800, self.ay24()) + Measurement(-1500 + 800 - 0.25 - 0.2, self.ars()))

    def test_balances_on_without_transactions(self):
        manager = TransactionManager(self.account)
        self.assertEqual(manager.balances_on(today, "VIOL"), Measurement(0, NullUnit()))

    def test_registered_transactions(self):
        iol_purchase = self.purchase(self.account)
        balanz_purchase = Purchase.objects.create(date=today, security_quantity=5000, financial_instrument=self.ay24(),
                                                  price=self.one_peso, broker="BALANZ", account=self.account)
        manager = TransactionManager(self.account)
        self.assertEqual(manager.registered_transactions(), [iol_purchase, balanz_purchase])
        self.assertEqual(manager.registered_transactions("IOL"), [iol_purchase])
        self.assertEqual(manager.registered_transactions("BALANZ"), [balanz_purchase])

    def test_registered_transactions_for_portfolio(self):
        portfolio = InvestmentPortfolio.objects.create(description='Portfolio')
        another_account = InvestmentIndividualAccount.objects.create(description='Pablo')
        portfolio.individual_accounts.add(self.account)
        portfolio.individual_accounts.add(another_account)
        transactions = [self.purchase(self.account), self.purchase(another_account), self.sale(another_account)]
        manager = TransactionManager(portfolio)
        self.assertEqual(manager.account, portfolio)
        self.assertTrue(manager.transactions, transactions)

    def test_balances_on_for_portfolio(self):
        portfolio = InvestmentPortfolio.objects.create(description='Portfolio')
        another_account = InvestmentIndividualAccount.objects.create(description='Pablo')
        portfolio.individual_accounts.add(self.account)
        portfolio.individual_accounts.add(another_account)
        transactions = [self.purchase(self.account), self.purchase(another_account), self.sale(another_account)]
        manager = TransactionManager(portfolio)
        self.assertEqual(manager.account, portfolio)
        self.assertTrue(manager.transactions, transactions)
        self.assertEqual(manager.balances_on(today),
                         Measurement(5000 * 2 - 300, self.ay24()) + Measurement(-5000 * 2 + 300, self.ars()))
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
import datetime

from my_portfolio_web_app.model.financial_instrument import Bond, Currency
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount, InvestmentPortfolio
from my_portfolio_web_app.model.measurement import Measurement, NullUnit
from my_portfolio_web_app.model.transaction import Purchase, Sale

today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)


class TestInvestmentAccount(TestCase):

    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()
        Currency.objects.create(code='$', description='Pesos')
        one_peso = Measurement(1, self.ars())
        Bond.objects.create(code='AY24', description='Bonar 2024', maturity_date=tomorrow)
        ay24 = self.ay24()
        Purchase.objects.create(date=today, security_quantity=5000, financial_instrument=ay24, price=one_peso,
                                broker="IOL")
        Sale.objects.create(date=today, security_quantity=300, financial_instrument=ay24, price=one_peso, broker="IOL")
        Sale.objects.create(date=today, security_quantity=800, financial_instrument=ay24, price=one_peso, broker="IOL")
        Purchase.objects.create(date=today, security_quantity=5000, financial_instrument=ay24, price=one_peso,
                                broker="BALANZ")
        Purchase.objects.create(date=tomorrow, security_quantity=1000, financial_instrument=ay24, price=one_peso,
                                broker="IOL")
        Purchase.objects.create(date=today, security_quantity=5000, financial_instrument=ay24, price=one_peso,
                                broker="IOL", ars_commissions=0.75)
        Purchase.objects.create(date=today, security_quantity=1500, financial_instrument=ay24, price=one_peso,
                                broker="BALANZ", ars_commissions=0.25)
        Sale.objects.create(date=today, security_quantity=300, financial_instrument=ay24, price=one_peso, broker="IOL",
                            ars_commissions=0.1)
        Sale.objects.create(date=today, security_quantity=800, financial_instrument=ay24, price=one_peso,
                            broker="BALANZ", ars_commissions=0.2)

        InvestmentIndividualAccount.objects.create(description="Martín")
        InvestmentIndividualAccount.objects.create(description="Pablo")

    @staticmethod
    def ars():
        return Currency.objects.get(code='$')

    @staticmethod
    def ay24():
        return Bond.objects.get(code='AY24')

    @staticmethod
    def purchase():
        return Purchase.objects.get(security_quantity=5000, ars_commissions=0, broker='IOL')

    @staticmethod
    def sale():
        return Sale.objects.get(security_quantity=800, ars_commissions=0)

    @staticmethod
    def sale2():
        return Sale.objects.get(security_quantity=300, ars_commissions=0)

    @staticmethod
    def balanz_purchase():
        return Purchase.objects.get(security_quantity=5000, broker='BALANZ')

    @staticmethod
    def tomorrow_purchase():
        return Purchase.objects.get(security_quantity=1000, ars_commissions=0)

    @staticmethod
    def purchase_with_commissions():
        return Purchase.objects.get(security_quantity=5000, ars_commissions=0.75)

    @staticmethod
    def purchase2_with_commissions():
        return Purchase.objects.get(security_quantity=1500, ars_commissions=0.25)

    @staticmethod
    def sale_with_commissions():
        return Sale.objects.get(security_quantity=300, ars_commissions=0.1)

    @staticmethod
    def sale2_with_commissions():
        return Sale.objects.get(security_quantity=800, ars_commissions=0.2)

    @staticmethod
    def account():
        return InvestmentIndividualAccount.objects.get(description='Martín')

    @staticmethod
    def another_account():
        return InvestmentIndividualAccount.objects.get(description='Pablo')


class TestInvestmentIndividualAccount(TestInvestmentAccount):
    def test_creation(self):
        self.assertEqual(self.account().description, "Martín")
        self.assertTrue(not self.account().registered_transactions())

    def test_add_transaction(self):
        self.assertTrue(not self.account().registered_transactions())
        self.account().add_transaction(self.purchase())
        self.assertIn(self.purchase(), self.account().registered_transactions())

    def test_balance_of(self):
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.assertEqual(self.account().balance_of_on(self.ay24(), today), 5000 - 300 - 800)

    def test_balance_of_today_is_unaffected_by_tomorrow_purchase(self):
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.account().add_transaction(self.tomorrow_purchase())
        self.assertEqual(self.account().balance_of_on(self.ay24(), today), 5000 - 300 - 800)
        self.assertEqual(self.account().balance_of_on(self.ay24(), tomorrow), self.account().balance_of_on(
            self.ay24(), today) + self.tomorrow_purchase().signed_security_quantity())

    def test_sale_in_short(self):
        one_peso = Measurement(1, self.ars())
        another_sale = Sale(date=today, security_quantity=3000, financial_instrument=self.ay24(), price=one_peso,
                            broker="IOL")
        another_sale2 = Sale(date=today, security_quantity=4000, financial_instrument=self.ay24(), price=one_peso,
                             broker="IOL")
        another_sale.save()
        another_sale2.save()
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(another_sale)
        self.assertEqual(self.account().balance_of_on(self.ay24(), today), 2000)
        with self.assertRaises(Exception):
            self.account().add_transaction(another_sale2)
        another_sale.delete()
        another_sale2.delete()

    def test_balances_on(self):
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.assertEqual(self.account().balances_on(today),
                         Measurement(5000 - 300 - 800, self.ay24()) + Measurement(-5000 + 800 + 300, self.ars()))

    def test_balances_on_with_tomorrow_purchase(self):
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.account().add_transaction(self.tomorrow_purchase())
        self.assertEqual(self.account().balances_on(today),
                         Measurement(5000 - 300 - 800, self.ay24()) + Measurement(-5000 + 800 + 300, self.ars()))
        self.assertEqual(self.account().balances_on(tomorrow),
                         Measurement(5000 - 300 - 800 + 1000, self.ay24()) + Measurement(-5000 + 800 + 300 - 1000,
                                                                                         self.ars()))

    def test_balances_on_with_closed_financial_instrument(self):
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.assertEqual(self.account().balances_on(today),
                         Measurement(5000 - 300 - 800, self.ay24()) + Measurement(-5000 + 800 + 300, self.ars()))
        self.assertEqual(self.account().balances_on(after_tomorrow),
                         Measurement(-5000 + 800 + 300, self.ars()))

    def test_balances_on_by_broker(self):
        self.account().add_transaction(self.purchase_with_commissions())
        self.account().add_transaction(self.purchase2_with_commissions())
        self.account().add_transaction(self.sale_with_commissions())
        self.account().add_transaction(self.sale2_with_commissions())
        self.assertEqual(self.account().balances_on(today),
                         Measurement(5000 + 1500 - 300 - 800, self.ay24()) + Measurement(
                             -5000 - 1500 + 800 + 300 - 0.75 - 0.25 - 0.1 - 0.2, self.ars()))
        self.assertEqual(self.account().balances_on(today, "IOL"),
                         Measurement(5000 - 300, self.ay24()) + Measurement(-5000 + 300 - 0.75 - 0.1, self.ars()))
        self.assertEqual(self.account().balances_on(today, "BALANZ"),
                         Measurement(1500 - 800, self.ay24()) + Measurement(-1500 + 800 - 0.25 - 0.2, self.ars()))

    def test_balances_on_by_broker_without_transactions(self):
        self.assertEqual(self.account().balances_on(today, "VIOL"), Measurement(0, NullUnit()))

    def test_registered_transactions(self):
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.balanz_purchase())
        self.assertEqual(self.account().registered_transactions(), self.account().registered_transactions())
        self.assertEqual(self.account().registered_transactions("IOL"), [self.purchase()])
        self.assertEqual(self.account().registered_transactions("BALANZ"), [self.balanz_purchase()])


class TestInvestmentPortfolio(TestInvestmentAccount):
    
    def setUp(self):
        super().setUp()
        InvestmentPortfolio.objects.create(description="Martín Portfolio")

    @staticmethod
    def portfolio():
        return InvestmentPortfolio.objects.get(description='Martín Portfolio')

    def tearDown(self):
        self.portfolio().delete()
        super().tearDown()

    def test_creation(self):
        self.portfolio().individual_accounts.add(self.account())
        self.assertEqual(self.portfolio().description, "Martín Portfolio")
        self.assertIn(self.account(), self.portfolio().individual_accounts.all())

    def test_balance_of_with_one_account(self):
        self.portfolio().individual_accounts.add(self.account())
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.assertEqual(self.account().balance_of_on(self.ay24(), today), 5000 - 300 - 800)
        self.assertEqual(self.portfolio().balance_of_on(self.ay24(), today), 5000 - 300 - 800)

    def test_balance_of_with_two_account(self):
        self.portfolio().individual_accounts.add(self.account())
        self.portfolio().individual_accounts.add(self.another_account())
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.another_account().add_transaction(self.purchase())
        self.assertEqual(self.account().balance_of_on(self.ay24(), today), 5000 - 300 - 800)
        self.assertEqual(self.another_account().balance_of_on(self.ay24(), today), 5000)
        self.assertEqual(self.portfolio().balance_of_on(self.ay24(), today), 5000 - 300 - 800 + 5000)

    def test_balances_on(self):
        self.portfolio().individual_accounts.add(self.account())
        self.portfolio().individual_accounts.add(self.another_account())
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.another_account().add_transaction(self.purchase())
        self.assertEqual(self.portfolio().balances_on(today),
                         Measurement(5000 + 5000 - 300 - 800, self.ay24()) + Measurement(-5000 - 5000 + 800 + 300,
                                                                                         self.ars()))

    def test_balances_on_with_tomorrow_purchase(self):
        self.portfolio().individual_accounts.add(self.account())
        self.portfolio().individual_accounts.add(self.another_account())
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.another_account().add_transaction(self.purchase())
        self.another_account().add_transaction(self.tomorrow_purchase())
        self.assertEqual(self.portfolio().balances_on(today),
                         Measurement(5000 + 5000 - 300 - 800, self.ay24()) + Measurement(-5000 - 5000 + 800 + 300,
                                                                                         self.ars()))
        self.assertEqual(self.portfolio().balances_on(tomorrow),
                         Measurement(5000 + 5000 - 300 - 800 + 1000, self.ay24()) + Measurement(
                             -5000 - 5000 + 800 + 300 - 1000, self.ars()))

    def test_balances_on_with_closed_financial_instrument(self):
        self.portfolio().individual_accounts.add(self.account())
        self.portfolio().individual_accounts.add(self.another_account())
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.sale())
        self.account().add_transaction(self.sale2())
        self.another_account().add_transaction(self.purchase())
        self.assertEqual(self.portfolio().balances_on(today),
                         Measurement(5000 + 5000 - 300 - 800, self.ay24()) + Measurement(-5000 - 5000 + 800 + 300,
                                                                                         self.ars()))
        self.assertEqual(self.portfolio().balances_on(after_tomorrow), Measurement(-5000 - 5000 + 800 + 300, self.ars()))

    def test_balances_on_by_broker(self):
        self.portfolio().individual_accounts.add(self.account())
        self.portfolio().individual_accounts.add(self.another_account())
        self.account().add_transaction(self.purchase_with_commissions())
        self.account().add_transaction(self.purchase2_with_commissions())
        self.account().add_transaction(self.sale_with_commissions())
        self.account().add_transaction(self.sale2_with_commissions())
        self.another_account().add_transaction(self.purchase_with_commissions())
        self.another_account().add_transaction(self.sale2_with_commissions())
        self.assertEqual(self.portfolio().balances_on(today),
                         Measurement(5000 * 2 + 1500 - 300 - 800 * 2, self.ay24()) + Measurement(
                             -5000 * 2 - 1500 + 800 * 2 + 300 - 0.75 * 2 - 0.25 - 0.1 - 0.2 * 2, self.ars()))
        self.assertEqual(self.portfolio().balances_on(today, "IOL"),
                         Measurement(5000 * 2 - 300, self.ay24()) + Measurement(-5000 * 2 + 300 - 0.75 * 2 - 0.1,
                                                                                self.ars()))
        self.assertEqual(self.portfolio().balances_on(today, "BALANZ"),
                         Measurement(1500 - 800 * 2, self.ay24()) + Measurement(-1500 + 800 * 2 - 0.25 - 0.2 * 2,
                                                                                self.ars()))

    def test_registered_transactions(self):
        self.portfolio().individual_accounts.add(self.account())
        self.portfolio().individual_accounts.add(self.another_account())
        self.account().add_transaction(self.purchase())
        self.account().add_transaction(self.balanz_purchase())
        self.another_account().add_transaction(self.balanz_purchase())
        self.assertEqual(self.portfolio().registered_transactions(),
                         self.account().registered_transactions() + self.another_account().registered_transactions())
        self.assertEqual(self.portfolio().registered_transactions("IOL"), [self.purchase()])
        self.assertEqual(self.portfolio().registered_transactions("BALANZ"),
                         [self.balanz_purchase(), self.balanz_purchase()])

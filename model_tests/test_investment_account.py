import unittest
from model import investment_account, financial_instrument, transaction
import datetime

from model.measurement import BagMeasurement, Measurement

euro = financial_instrument.Currency('EUR', 'Euro')
one_euro = Measurement(1, euro)
today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)
ay24 = financial_instrument.Bond('AY24', 'Bonar 2024', tomorrow)


class TestInvestmentIndividualAccount(unittest.TestCase):

    def test_creation(self):
        account = investment_account.InvestmentIndividualAccount("Martín")
        self.assertEqual(account.description, "Martín")
        self.assertTrue(not account.transactions)

    def test_add_transaction(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        self.assertTrue(not account.transactions)
        account.add_transaction(purchase)
        self.assertIn(purchase, account.transactions)

    def test_balance_of(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)

    def test_balance_of_today_is_unaffected_by_tomorrow_purchase(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        tomorrow_purchase = transaction.Purchase(tomorrow, 2000, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        account.add_transaction(tomorrow_purchase)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)
        self.assertEqual(account.balance_of_on(ay24, tomorrow), account.balance_of_on(
            ay24, today) + tomorrow_purchase.signed_security_quantity())

    def test_sale_in_short(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 3000, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 4000, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        self.assertEqual(account.balance_of_on(ay24, today), 2000)
        with self.assertRaises(Exception):
            account.add_transaction(sale2)

    def test_balances_on(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balances_on(today),
                         Measurement(5000 - 300 - 800, ay24) + Measurement(-5000 + 800 + 300, euro))

    def test_balances_on_with_tomorrow_purchase(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        tomorrow_purchase = transaction.Purchase(tomorrow, 1000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        account.add_transaction(tomorrow_purchase)
        self.assertEqual(account.balances_on(today),
                         Measurement(5000 - 300 - 800, ay24) + Measurement(-5000 + 800 + 300, euro))
        self.assertEqual(account.balances_on(tomorrow),
                         Measurement(5000 - 300 - 800 + 1000, ay24) + Measurement(-5000 + 800 + 300 - 1000, euro))

    def test_balances_on_with_closed_financial_instrument(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balances_on(today),
                         Measurement(5000 - 300 - 800, ay24) + Measurement(-5000 + 800 + 300, euro))
        self.assertEqual(account.balances_on(after_tomorrow),
                         Measurement(-5000 + 800 + 300, euro))

    def test_balances_on_by_broker(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL", one_euro * 0.75)
        purchase2 = transaction.Purchase(today, 1500, ay24, one_euro, "BALANZ", one_euro * 0.25)
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL", one_euro * 0.1)
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "BALANZ", one_euro * 0.2)
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(purchase2)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balances_on(today), Measurement(5000 + 1500 - 300 - 800, ay24) + Measurement(
            -5000 - 1500 + 800 + 300 - 0.75 - 0.25 - 0.1 - 0.2, euro))
        self.assertEqual(account.balances_on(today, "IOL"),
                         Measurement(5000 - 300, ay24) + Measurement(-5000 + 300 - 0.75 - 0.1, euro))
        self.assertEqual(account.balances_on(today, "BALANZ"),
                         Measurement(1500 - 800, ay24) + Measurement(-1500 + 800 - 0.25 - 0.2, euro))


class TestInvestmentPortfolio(unittest.TestCase):

    def test_creation(self):
        account = investment_account.InvestmentIndividualAccount("Martín")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account])
        self.assertEqual(portfolio.description, "Martín Portfolio")
        self.assertIn(account, portfolio.individual_accounts)

    def test_balance_of_with_one_account(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account])
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)
        self.assertEqual(portfolio.balance_of_on(ay24, today), 5000 - 300 - 800)

    def test_balance_of_with_two_account(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        another_account = investment_account.InvestmentIndividualAccount("Pablo")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account, another_account])
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        another_account.add_transaction(purchase)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)
        self.assertEqual(another_account.balance_of_on(ay24, today), 5000)
        self.assertEqual(portfolio.balance_of_on(ay24, today), 5000 - 300 - 800 + 5000)

    def test_balances_on(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        another_account = investment_account.InvestmentIndividualAccount("Pablo")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account, another_account])
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        another_account.add_transaction(purchase)
        self.assertEqual(portfolio.balances_on(today),
                         Measurement(5000 + 5000 - 300 - 800, ay24) + Measurement(-5000 - 5000 + 800 + 300, euro))

    def test_balances_on_with_tomorrow_purchase(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        tomorrow_purchase = transaction.Purchase(tomorrow, 1000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        another_account = investment_account.InvestmentIndividualAccount("Pablo")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account, another_account])
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        another_account.add_transaction(purchase)
        another_account.add_transaction(tomorrow_purchase)
        self.assertEqual(portfolio.balances_on(today),
                         Measurement(5000 + 5000 - 300 - 800, ay24) + Measurement(-5000 - 5000 + 800 + 300, euro))
        self.assertEqual(portfolio.balances_on(tomorrow),
                         Measurement(5000 + 5000 - 300 - 800 + 1000, ay24) + Measurement(
                             -5000 - 5000 + 800 + 300 - 1000, euro))

    def test_balances_on_with_closed_financial_instrument(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        another_account = investment_account.InvestmentIndividualAccount("Pablo")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account, another_account])
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        another_account.add_transaction(purchase)
        self.assertEqual(portfolio.balances_on(today),
                         Measurement(5000 + 5000 - 300 - 800, ay24) + Measurement(-5000 - 5000 + 800 + 300, euro))
        self.assertEqual(portfolio.balances_on(after_tomorrow), Measurement(-5000 - 5000 + 800 + 300, euro))

    def test_balances_on_by_broker(self):
        purchase = transaction.Purchase(today, 5000, ay24, one_euro, "IOL", one_euro * 0.75)
        purchase2 = transaction.Purchase(today, 1500, ay24, one_euro, "BALANZ", one_euro * 0.25)
        sale = transaction.Sale(today, 300, ay24, one_euro, "IOL", one_euro * 0.1)
        sale2 = transaction.Sale(today, 800, ay24, one_euro, "BALANZ", one_euro * 0.2)
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(purchase2)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        another_account = investment_account.InvestmentIndividualAccount("Pablo")
        another_account.add_transaction(purchase)
        another_account.add_transaction(sale2)
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account, another_account])
        self.assertEqual(portfolio.balances_on(today), Measurement(5000 * 2 + 1500 - 300 - 800 * 2, ay24) + Measurement(
            -5000 * 2 - 1500 + 800 * 2 + 300 - 0.75 * 2 - 0.25 - 0.1 - 0.2 * 2, euro))
        self.assertEqual(portfolio.balances_on(today, "IOL"),
                         Measurement(5000 * 2 - 300, ay24) + Measurement(-5000 * 2 + 300 - 0.75 * 2 - 0.1, euro))
        self.assertEqual(portfolio.balances_on(today, "BALANZ"),
                         Measurement(1500 - 800 * 2, ay24) + Measurement(-1500 + 800 * 2 - 0.25 - 0.2 * 2, euro))


if __name__ == '__main__':
    unittest.main()

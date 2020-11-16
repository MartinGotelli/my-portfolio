import unittest
from model import investment_account, financial_instrument, transaction
import datetime

euro = financial_instrument.Currency('EUR', 'Euro')
today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
ay24 = financial_instrument.Bond('AY24', 'Bonar 2024', tomorrow)


class TestInvestmentIndividualAccount(unittest.TestCase):

    def test_creation(self):
        account = investment_account.InvestmentIndividualAccount("Martín")
        self.assertEqual(account.description, "Martín")
        self.assertTrue(not account.transactions)

    def test_add_transaction(self):
        purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        self.assertTrue(not account.transactions)
        account.add_transaction(purchase)
        self.assertIn(purchase, account.transactions)

    def test_balance_of(self):
        purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, 1, euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, 1, euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)

    def test_balance_of_today_is_unaffected_by_tomorrow_purchase(self):
        purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, 1, euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, 1, euro, "IOL")
        tomorrow_purchase = transaction.Purchase(tomorrow, 2000, ay24, 1, euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        account.add_transaction(tomorrow_purchase)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)
        self.assertEqual(account.balance_of_on(ay24, tomorrow), account.balance_of_on(
            ay24, today) + tomorrow_purchase.signed_security_quantity())

    def test_sale_in_short(self):
        purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
        sale = transaction.Sale(today, 3000, ay24, 1, euro, "IOL")
        sale2 = transaction.Sale(today, 4000, ay24, 1, euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(sale)
        self.assertEqual(account.balance_of_on(ay24, today), 2000)
        with self.assertRaises(Exception):
            account.add_transaction(sale2)


class TestInvestmentPortfolio(unittest.TestCase):

    def test_creation(self):
        account = investment_account.InvestmentIndividualAccount("Martín")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account])
        self.assertEqual(portfolio.description, "Martín Portfolio")
        self.assertIn(account, portfolio.individual_accounts)

    def test_balance_of_with_one_account(self):
        purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, 1, euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, 1, euro, "IOL")
        account = investment_account.InvestmentIndividualAccount("Martín")
        portfolio = investment_account.InvestmentPortfolio("Martín Portfolio", [account])
        account.add_transaction(purchase)
        account.add_transaction(sale)
        account.add_transaction(sale2)
        self.assertEqual(account.balance_of_on(ay24, today), 5000 - 300 - 800)
        self.assertEqual(portfolio.balance_of_on(ay24, today), 5000 - 300 - 800)

    def test_balance_of_with_two_account(self):
        purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
        sale = transaction.Sale(today, 300, ay24, 1, euro, "IOL")
        sale2 = transaction.Sale(today, 800, ay24, 1, euro, "IOL")
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


'''
def test_balances_on(self):
    purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
    sale = transaction.Sale(today, 300, ay24, 1, euro, "IOL")
    sale2 = transaction.Sale(today, 800, ay24, 1, euro, "IOL")
    account = investment_account.InvestmentIndividualAccount("Martín")
    account.add_transaction(purchase)
    account.add_transaction(sale)
    account.add_transaction(sale2)
    balances = account.balances_on(today)
    self.assertEqual(len(balances), 1)
    self.assertEqual(balances[0].financial_instrument, ay24)
    self.assertEqual(balances[0].value, 3900)

def test_purchases_of_on(self):
    purchase = transaction.Purchase(today, 5000, ay24, 1, euro, "IOL")
    sale = transaction.Sale(today, 300, ay24, 1, euro, "IOL")
    tomorrow_purchase = transaction.Purchase(tomorrow, 2000, ay24, 1, euro, "IOL")
    account = investment_account.InvestmentIndividualAccount("Martín")
    account.add_transaction(purchase)
    account.add_transaction(sale)
    account.add_transaction(tomorrow_purchase)
    self.assertIn(purchase, account.purchases_of_on(ay24, today))
    self.assertNotIn(tomorrow_purchase,
                     account.purchases_of_on(ay24, today))
    self.assertNotIn(sale, account.purchases_of_on(ay24, today))
    self.assertIn(purchase, account.purchases_of_on(ay24, tomorrow))
    self.assertIn(tomorrow_purchase,
                  account.purchases_of_on(ay24, tomorrow))
    self.assertNotIn(sale, account.purchases_of_on(ay24, tomorrow))
    '''

if __name__ == '__main__':
    unittest.main()

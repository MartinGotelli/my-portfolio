import datetime

from django.test import TestCase

from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)

today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)


class TestInvestmentAccount(TestCase):

    def setUp(self):
        super().setUp()
        InvestmentIndividualAccount.objects.create(description="Martín")
        InvestmentIndividualAccount.objects.create(description="Pablo")

    @staticmethod
    def account():
        return InvestmentIndividualAccount.objects.get(description='Martín')

    @staticmethod
    def another_account():
        return InvestmentIndividualAccount.objects.get(description='Pablo')


class TestInvestmentIndividualAccount(TestInvestmentAccount):
    def test_creation(self):
        self.assertEqual(self.account().description, "Martín")

    def test_accounts(self):
        self.assertEquals(self.account().accounts(), [self.account()])


class TestInvestmentPortfolio(TestInvestmentAccount):

    def setUp(self):
        super().setUp()
        InvestmentPortfolio.objects.create(description="Martín Portfolio")

    @staticmethod
    def portfolio():
        return InvestmentPortfolio.objects.get(description='Martín Portfolio')

    def test_creation(self):
        self.assertEqual(self.portfolio().description, "Martín Portfolio")

    def test_accounts(self):
        self.assertEqual(self.portfolio().accounts(), set())
        self.portfolio().individual_accounts.add(self.account())
        self.assertEqual(self.portfolio().accounts(), {self.account()})
        self.portfolio().individual_accounts.add(self.another_account())
        self.assertEqual(self.portfolio().accounts(), {self.account(), self.another_account()})

import datetime

from django.contrib.auth.models import User
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
        mock_user = User.objects.create(username='mock')
        martin_account = InvestmentIndividualAccount.objects.create(description="Martín")
        martin_account.authorized_users.add(mock_user)
        pablo_account = InvestmentIndividualAccount.objects.create(description="Pablo")
        pablo_account.authorized_users.add(mock_user)

    @staticmethod
    def account():
        return InvestmentIndividualAccount.objects.get(description='Martín')

    @staticmethod
    def another_account():
        return InvestmentIndividualAccount.objects.get(description='Pablo')

    @staticmethod
    def mock_user():
        return User.objects.get(username='mock')


class TestInvestmentIndividualAccount(TestInvestmentAccount):
    def test_creation(self):
        self.assertEqual(self.account().description, "Martín")

    def test_accounts(self):
        self.assertEquals(self.account().accounts(), [self.account()])

    def test_by_user(self):
        self.assertEquals(InvestmentIndividualAccount.by_user(self.mock_user()),
                          [self.account(), self.another_account()])
        self.assertEquals(InvestmentIndividualAccount.by_user(self.mock_user()),
                          list(InvestmentIndividualAccount.objects.all()))

        another_user = User.objects.create(username='other')
        self.assertEquals(InvestmentIndividualAccount.by_user(self.mock_user()),
                          [self.account(), self.another_account()])
        self.assertEquals(InvestmentIndividualAccount.by_user(another_user), [])

        yet_another_account = InvestmentIndividualAccount.objects.create(description="Yetti")
        self.assertEquals(list(InvestmentIndividualAccount.objects.all()),
                          [self.account(), self.another_account(), yet_another_account])
        self.assertEquals(InvestmentIndividualAccount.by_user(another_user), [])

        yet_another_account.authorized_users.add(another_user)
        self.assertEquals(InvestmentIndividualAccount.by_user(another_user), [yet_another_account])


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

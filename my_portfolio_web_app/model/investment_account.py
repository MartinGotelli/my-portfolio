from django.db.models import (
    CharField,
    ManyToManyField,
)

from my_portfolio_web_app.model.my_portfolio_model import MyPortfolioModel


class InvestmentIndividualAccount(MyPortfolioModel):
    description = CharField(max_length=200, verbose_name='Descripción')

    @classmethod
    def class_name(cls):
        return 'account'

    def __repr__(self):
        return 'Cuenta ' + self.description

    def accounts(self):
        return [self]


class InvestmentPortfolio(MyPortfolioModel):
    description = CharField(max_length=200, verbose_name='Descripción')
    individual_accounts = ManyToManyField(InvestmentIndividualAccount, verbose_name='Cuentas')

    @classmethod
    def class_name(cls):
        return 'portfolio'

    def __repr__(self):
        return 'Portfolio ' + self.description + '\nCon cuentas: '  # + ', '.join(
        # [str(account) for account in self.individual_accounts.all()])

    def accounts(self):
        return self.individual_accounts.all()

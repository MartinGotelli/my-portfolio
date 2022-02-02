from django.contrib.auth.models import User
from django.db.models import (
    CharField,
    ManyToManyField,
)

from my_portfolio_web_app.model.my_portfolio_model import MyPortfolioModel


class InvestmentIndividualAccount(MyPortfolioModel):
    description = CharField(max_length=200, verbose_name='Descripción')
    authorized_users = ManyToManyField(User, verbose_name='Usuarios Autorizados')

    @classmethod
    def class_name(cls):
        return 'account'

    @classmethod
    def by_user(cls, user: User):
        all_objects = cls.objects.all()
        if user.is_superuser:
            return list(all_objects)
        else:
            return [element for element in all_objects if user in element.authorized_users.all()]

    def __repr__(self):
        return 'Cuenta ' + self.description

    def accounts(self):
        return [self]


class InvestmentPortfolio(MyPortfolioModel):
    description = CharField(max_length=200, verbose_name='Descripción')
    individual_accounts = ManyToManyField(InvestmentIndividualAccount, verbose_name='Cuentas')
    authorized_users = ManyToManyField(User, verbose_name='Usuarios Autorizados')

    @classmethod
    def class_name(cls):
        return 'portfolio'

    @classmethod
    def by_user(cls, user: User):
        all_objects = cls.objects.all()
        if user.is_superuser:
            return list(all_objects)
        else:
            return [account for account in all_objects if user in account.authorized_users.all()]

    def __repr__(self):
        return 'Portfolio ' + self.description + '\nCon cuentas: '  # + ', '.join(
        # [str(account) for account in self.individual_accounts.all()])

    def accounts(self):
        return set(self.individual_accounts.all())

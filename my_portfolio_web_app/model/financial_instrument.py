from abc import abstractmethod

from django.db.models import CharField, IntegerField, DateField

from my_portfolio_web_app.model.my_portfolio_model import MyPortfolioPolymorphicModel


class FinancialInstrument(MyPortfolioPolymorphicModel):
    code = CharField(max_length=200)
    description = CharField(max_length=200)
    price_each_quantity = IntegerField(default=1)

    def __eq__(self, obj):
        return isinstance(obj, FinancialInstrument) and self.code == obj.code

    def __hash__(self):
        return hash(self.code)

    def __ne__(self, obj):
        return not self == obj

    def __repr__(self):
        return self.code + ' - ' + self.description

    @staticmethod
    @abstractmethod
    def is_currency(): pass

    @abstractmethod
    def is_alive_on(self, date): pass


class Currency(FinancialInstrument):
    @staticmethod
    def is_currency(): return True

    def is_alive_on(self, date): return True


class Bond(FinancialInstrument):
    maturity_date = DateField('Maturity Date')

    @staticmethod
    def is_currency(): return False

    def is_alive_on(self, date): return date <= self.maturity_date


class Stock(FinancialInstrument):
    @staticmethod
    def is_currency(): return False

    def is_alive_on(self, date): return True


ars = Currency(code="$", description="Pesos")
usd = Currency(code="USD", description="Dólares")

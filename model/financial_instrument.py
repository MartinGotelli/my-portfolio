from abc import abstractmethod


class FinancialInstrument:
    def __init__(self, code, description, price_each_quantity=1):
        self.code = code
        self.description = description
        self.price_each_quantity = price_each_quantity

    def __eq__(self, obj):
        return self.code == obj.code

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
    def __init__(self, code, description, maturity_date, price_each_quantity=1):
        super().__init__(code, description, price_each_quantity)
        self.maturity_date = maturity_date

    @staticmethod
    def is_currency(): return False

    def is_alive_on(self, date): return date <= self.maturity_date


class Stock(FinancialInstrument):
    @staticmethod
    def is_currency(): return False

    def is_alive_on(self, date): return True